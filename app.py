from flask import Flask, render_template, request
import pdfplumber
from docx import Document
from skills import skills_list
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Extracting text from PDF
def extract_text_from_pdf(path):
    text = ""

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "

    return text.lower()


# Extracting text from DOCX
def extract_text_from_docx(path):
    text = ""
    doc = Document(path)

    for para in doc.paragraphs:
        text += para.text + " "

    return text.lower()


# Extract skills
def extract_skills(text):
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text:
            found_skills.append(skill)

    return list(set(found_skills))


# Calculate match score
def calculate_similarity(resume, jd):
    text = [resume, jd]

    cv = CountVectorizer()
    matrix = cv.fit_transform(text)

    similarity = cosine_similarity(matrix)[0][1]

    return round(similarity * 100, 2)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}

    if request.method == 'POST':
        jd = request.form.get('job_description', '').strip()
        file = request.files.get('resume')

        if not jd:
            return "Please enter a job description."

        if not file or not file.filename:
            return "Please upload a resume."

        filename = file.filename.lower()

        if filename.endswith('.pdf'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            resume_text = extract_text_from_pdf(filepath)

        elif filename.endswith('.docx'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            resume_text = extract_text_from_docx(filepath)

        else:
            return "Unsupported file format. Please upload a PDF or DOCX file."

        # Extract skills
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd.lower())

        # Find missing skills
        missing_skills = list(set(jd_skills) - set(resume_skills))

        # Calculate similarity score
        score = calculate_similarity(resume_text, jd.lower())

        # Calculate skill gap percentage
        if jd_skills:
            skill_gap = round(
                (len(missing_skills) / len(jd_skills)) * 100, 2
            )
        else:
            skill_gap = 0

        # Results for the HTML template
        result = {
            "resume_skills": resume_skills,
            "jd_skills": jd_skills,
            "job_description_skills": jd_skills,
            "missing_skills": missing_skills,
            "score": score,
            "ats_score": score,
            "skill_gap": skill_gap
        }

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)