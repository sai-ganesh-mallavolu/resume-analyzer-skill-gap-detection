# AI Resume Analyzer with Skill Gap Detection

A lightweight resume analysis web application that allows users to upload a resume in PDF or DOCX format and compare it with a job description.

This project uses Python and Flask to extract resume text, identify relevant skills, calculate a text similarity score, and highlight skills that are mentioned in the job description but missing from the resume.

The main goal of this project is to help job seekers understand how closely their resume matches a particular job description and identify areas where they can improve their skills.

## Overview

Applying for jobs can be challenging when it is difficult to understand whether a resume matches the requirements of a specific role.

This project provides a simple interface where users can upload their resumes and paste a job description. The application extracts the text, identifies skills using a predefined skill list, and compares the resume with the job description using TF-IDF-style text vectorization and cosine similarity.

It also identifies missing skills to help users understand which job-related skills are not detected in their resumes.

## Features

- Upload resumes in PDF and DOCX formats
- Extract text from PDF documents using pdfplumber
- Extract text from DOCX documents using python-docx
- Identify skills using a predefined list of keywords
- Compare resumes with job descriptions
- Calculate a resume match percentage using cosine similarity
- Detect missing skills based on the job description
- Calculate a skill gap percentage
- Display analysis results through a simple web interface
- Separate HTML templates and CSS styling
- Handle basic input validation and unsupported file formats

## How It Works

The application follows a simple resume analysis workflow:

```text
Upload Resume
      ↓
Extract Resume Text
      ↓
Enter Job Description
      ↓
Identify Resume Skills
      ↓
Identify Job Description Skills
      ↓
Compare Resume and Job Description
      ↓
Calculate Similarity Score
      ↓
Find Missing Skills
      ↓
Display Analysis Results
```

## Tech Stack

### Frontend

- HTML
- CSS
- Jinja2 Templates

### Backend

- Python
- Flask

### Text Processing and Analysis

- pdfplumber
- python-docx
- Scikit-learn
- CountVectorizer
- Cosine Similarity
- Custom skill keyword matching

### Development Tools

- Visual Studio Code
- Git
- GitHub
- Python Virtual Environment

## Project Structure

```text
Resume-Analyzer/
│
├── app.py
├── skills.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── uploads/
│
└── README.md
```

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- pip
- Git
- A code editor such as Visual Studio Code

### Clone the Repository

Clone the project repository:

```bash
git clone <your-repository-url>
```

Navigate to the project directory:

```bash
cd Resume-Analyzer
```

### Create a Virtual Environment

Create a virtual environment to manage project dependencies:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

Install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

### Run the Application

Start the Flask application:

```bash
python app.py
```

The application will run locally at:

```text
http://127.0.0.1:5000/
```

Open this address in your browser to use the Resume Analyzer.

## Using the Application

1. Open the application in your browser.
2. Paste the job description into the text area.
3. Upload your resume in PDF or DOCX format.
4. Click **Analyze Resume**.
5. The application extracts text from the uploaded resume.
6. It identifies the skills found in the resume and job description.
7. It calculates the similarity score and identifies missing skills.
8. The results are displayed on the page.

## Resume Analysis

### Resume Match Score

The application uses CountVectorizer and cosine similarity to calculate how similar the resume text is to the job description.

The score is displayed as a percentage to provide a quick indication of textual similarity.

### Skill Extraction

The application checks the extracted resume text and job description against a predefined list of skills maintained in `skills.py`.

The detected skills are displayed for comparison.

### Skill Gap Detection

The application compares the skills detected in the resume with those detected in the job description.

Skills found in the job description but not detected in the resume are listed as missing skills.

### Skill Gap Percentage

The skill gap percentage is calculated using the number of missing detected skills divided by the total number of detected job description skills.

If no skills are detected in the job description, the skill gap percentage is set to zero.

## Example

Suppose a job description mentions the following skills:

- Python
- SQL
- Flask
- Machine Learning

If the uploaded resume contains Python and SQL but does not contain Flask or Machine Learning, the application can identify Flask and Machine Learning as missing skills, provided they are included in the predefined skill list.

This helps the user identify skills that may need more attention when preparing for the role.

## Current Limitations

The current version is a lightweight implementation designed to demonstrate basic resume matching and skill gap detection.

Currently:

- Skill extraction depends on a predefined keyword list.
- Skills may not be detected when they are written using different terms or abbreviations.
- The match score measures textual similarity, not an official ATS score.
- The application does not understand the full context of every skill mention.
- Scanned PDFs without extractable text may not work correctly.
- The analysis depends on the quality of the uploaded resume and job description.
- The current version does not use a trained machine learning model to predict hiring outcomes.

## Future Improvements

Some possible improvements include:

- Improve skill recognition using NLP techniques.
- Add support for more resume formats.
- Provide suggestions for improving resume content.
- Recommend learning resources for missing skills.
- Improve resume matching using semantic embeddings.
- Add resume section analysis for education, projects, and experience.
- Improve file validation and upload security.
- Create a downloadable resume analysis report.
- Deploy the application online so users can access it from anywhere.

## What I Learned

Building this project helped me gain practical experience in Python programming, web development, and text analysis.

Through this project, I worked with:

- Flask application development
- PDF and DOCX text extraction
- Text preprocessing
- Skill keyword matching
- CountVectorizer
- Cosine similarity
- Basic similarity score calculation
- Set operations for identifying missing skills
- HTML templates and backend integration
- Python dependency management

The project also helped me understand how text comparison techniques can be applied to a practical problem faced by job seekers.

## Project Status

The current version implements the core resume analysis workflow, including document text extraction, keyword-based skill detection, text similarity scoring, and missing skill identification.

The application can be extended with more advanced NLP techniques, semantic matching, improved resume recommendations, and online deployment.

## Author

**Mallavolu Sai Ganesh**

Email:mallavolusaiganesh@gmail.com

---

Built with Python, Flask, and Scikit-learn.
