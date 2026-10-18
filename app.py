
from flask import Flask, render_template, request, redirect, url_for, session
import pdfplumber
from docx import Document
from skills import skills_list
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.utils import secure_filename
import re
import os

app = Flask(__name__)

# Use an environment variable for the production secret key
app.secret_key = os.environ.get("SECRET_KEY", "local-development-secret-key")

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Extract text from PDF
def extract_text_from_pdf(path):
    text = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

    return " ".join(text).lower()


# Extract text from DOCX
def extract_text_from_docx(path):
    doc = Document(path)
    text = " ".join(para.text for para in doc.paragraphs)
    return text.lower()


# Normalize text for more reliable skill matching
def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.]+", " ", text)
    return f" {text} "


# Extract skills using word/phrase boundaries
def extract_skills(text):
    normalized_text = normalize_text(text)
    found_skills = []

    for skill in skills_list:
        normalized_skill = normalize_text(skill).strip()

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(normalized_skill)
            + r"(?![a-z0-9])"
        )

        if re.search(pattern, normalized_text):
            found_skills.append(skill)

    return sorted(set(found_skills))


# Calculate text similarity
def calculate_similarity(resume, jd):
    vectorizer = CountVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform([resume, jd])
    similarity = cosine_similarity(matrix)[0][1]

    return round(similarity * 100, 2)


# Calculate skill match percentage
def calculate_skill_match(resume_skills, jd_skills):
    if not jd_skills:
        return 0.0

    matched_skills = set(resume_skills) & set(jd_skills)

    return round(
        len(matched_skills) / len(set(jd_skills)) * 100,
        2
    )


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        # Clear any previous analysis result
        session.pop("result", None)

        jd = request.form.get("job_description", "").strip()
        file = request.files.get("resume")

        if not jd:
            return render_template(
                "index.html",
                error="Please enter a job description.",
                result=None,
                job_description=""
            )

        if not file or not file.filename:
            return render_template(
                "index.html",
                error="Please upload a resume.",
                result=None,
                job_description=""
            )

        filename = secure_filename(file.filename)

        if not filename:
            return render_template(
                "index.html",
                error="Invalid filename. Please select another file.",
                result=None,
                job_description=""
            )

        extension = os.path.splitext(filename)[1].lower()

        if extension not in [".pdf", ".docx"]:
            return render_template(
                "index.html",
                error="Please upload a PDF or DOCX file.",
                result=None,
                job_description=""
            )

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        try:
            file.save(filepath)

            if extension == ".pdf":
                resume_text = extract_text_from_pdf(filepath)
            else:
                resume_text = extract_text_from_docx(filepath)

        except Exception:
            return render_template(
                "index.html",
                error="Unable to read this file. Please try another PDF or DOCX.",
                result=None,
                job_description=""
            )

        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

        if not resume_text.strip():
            return render_template(
                "index.html",
                error="No readable text found in the resume.",
                result=None,
                job_description=""
            )

        # Extract skills
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd)

        # Find missing skills
        missing_skills = sorted(
            set(jd_skills) - set(resume_skills)
        )

        # Calculate skill match
        skill_match = calculate_skill_match(
            resume_skills,
            jd_skills
        )

        # Calculate skill gap
        if jd_skills:
            skill_gap = round(
                len(missing_skills) / len(set(jd_skills)) * 100,
                2
            )
        else:
            skill_gap = 0.0

        # Calculate text similarity
        try:
            text_similarity = calculate_similarity(
                resume_text,
                jd
            )
        except ValueError:
            text_similarity = 0.0

        # Combined score
        if jd_skills:
            score = round(
                (skill_match * 0.80)
                + (text_similarity * 0.20),
                2
            )
        else:
            score = text_similarity

        result = {
            "resume_skills": resume_skills,
            "job_description_skills": jd_skills,
            "missing_skills": missing_skills,
            "skill_match": skill_match,
            "text_similarity": text_similarity,
            "ats_score": score,
            "skill_gap": skill_gap
        }

        # Store the result temporarily for the next GET request
        session["result"] = result

        # Redirect prevents the browser from resubmitting the form
        return redirect(url_for("index"), code=303)

    # GET request: display result once, then remove it from session
    result = session.pop("result", None)

    return render_template(
        "index.html",
        result=result,
        job_description=""
    )


if __name__ == "__main__":
    app.run(debug=True)
