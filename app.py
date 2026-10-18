
from flask import Flask, render_template, request, redirect, url_for
import pdfplumber
from docx import Document
from skills import skills_list
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Extract text from PDF
def extract_text_from_pdf(path):
    text = ""

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "

    return text.lower()


# Extract text from DOCX
def extract_text_from_docx(path):
    doc = Document(path)
    text = " ".join(para.text for para in doc.paragraphs)
    return text.lower()


# Extract skills
def extract_skills(text):
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text:
            found_skills.append(skill)

    return sorted(set(found_skills))


# Calculate text similarity
def calculate_similarity(resume, jd):
    vectorizer = CountVectorizer()
    matrix = vectorizer.fit_transform([resume, jd])

    similarity = cosine_similarity(matrix)[0][1]
    return round(similarity * 100, 2)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        jd = request.form.get("job_description", "").strip()
        file = request.files.get("resume")

        if not jd:
            return render_template(
                "index.html",
                error="Please enter a job description."
            )

        if not file or not file.filename:
            return render_template(
                "index.html",
                error="Please upload a resume."
            )

        filename = secure_filename(file.filename)
        extension = os.path.splitext(filename)[1].lower()

        if extension not in [".pdf", ".docx"]:
            return render_template(
                "index.html",
                error="Please upload a PDF or DOCX file."
            )

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        try:
            file.save(filepath)

            if extension == ".pdf":
                resume_text = extract_text_from_pdf(filepath)
            else:
                resume_text = extract_text_from_docx(filepath)

        except Exception:
            return render_template(
                "index.html",
                error="Unable to read this file. Please try another PDF or DOCX."
            )

        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

        if not resume_text.strip():
            return render_template(
                "index.html",
                error="No readable text found in the resume."
            )

        # Extract skills
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd.lower())

        # Find missing skills
        missing_skills = sorted(set(jd_skills) - set(resume_skills))

        # Calculate similarity
        try:
            score = calculate_similarity(resume_text, jd.lower())
        except ValueError:
            score = 0.0

        # Calculate skill gap
        if jd_skills:
            skill_gap = round(
                len(missing_skills) / len(jd_skills) * 100, 2
            )
        else:
            skill_gap = 0

        result = {
            "resume_skills": resume_skills,
            "job_description_skills": jd_skills,
            "missing_skills": missing_skills,
            "score": score,
            "ats_score": score,
            "skill_gap": skill_gap
        }

        # Render results for this response only.
        # A refresh sends a new GET request and clears everything.
        return render_template(
            "index.html",
            result=result,
            job_description=jd
        )

    # Fresh page load / refresh: empty form and no results
    return render_template("index.html", result=None, job_description="")


if __name__ == "__main__":
    app.run(debug=True)
