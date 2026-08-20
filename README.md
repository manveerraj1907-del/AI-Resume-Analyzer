# AI Resume Analyzer

An AI-powered resume analysis and candidate screening application built using **Python, Streamlit, and Google Gemini AI**.

The application helps analyze resumes, identify relevant skills and experience, compare candidates with job requirements, and generate AI-powered recruitment insights.

## 📌 Project Overview

Recruiters often need to review a large number of resumes for a single job opening. Manually comparing candidates can be time-consuming and may make it difficult to consistently evaluate different resumes.

**AI Resume Analyzer** is designed to assist with this process.

Users can provide a job description and upload candidate resumes in PDF format. The application extracts the resume content and uses Google Gemini AI to analyze the candidate against the provided job requirements.

The system can provide information such as:

* Candidate details
* Relevant skills
* Missing skills
* Experience analysis
* Education analysis
* Project analysis
* Overall candidate score
* Professional summary
* Recruitment recommendation

> **Important:** The application is designed as an AI-assisted screening tool. Final hiring decisions should always be made by a qualified human recruiter.

---

## ✨ Features

### 📄 Resume Upload

* Upload resumes in PDF format
* Support multiple candidate resumes
* Extract text from uploaded PDF files

### 🤖 AI Resume Analysis

Google Gemini AI is used to analyze the extracted resume information.

The system evaluates candidates based on the provided job requirements.

### 🎯 Candidate Matching

Candidates can be evaluated according to:

* Required skills
* Relevant experience
* Education
* Projects
* Overall suitability

### 📊 Candidate Scoring

The application can generate scores for different areas, including:

* Overall Score
* Skills Score
* Experience Score
* Education Score
* Projects Score

### 🔍 Skill Analysis

The system identifies:

* Matching skills
* Missing skills
* Relevant technical abilities
* Candidate strengths

### 📝 AI-Generated Summary

The application generates a professional summary of the candidate based on their resume.

### 🏆 Recruitment Recommendation

The AI provides a recommendation based on how closely the candidate matches the job requirements.

---

## 🧠 How It Works

The application follows this workflow:

```text
Job Description
       ↓
Upload Candidate Resumes
       ↓
Extract Resume Text
       ↓
Send Resume + Job Requirements to AI
       ↓
Google Gemini Analysis
       ↓
Calculate Candidate Evaluation
       ↓
Generate Scores & Insights
       ↓
Recruiter Reviews Results
```

---

## 🛠️ Technologies Used

| Technology       | Purpose                      |
| ---------------- | ---------------------------- |
| Python           | Application development      |
| Streamlit        | Web application interface    |
| Google Gemini AI | AI-powered resume analysis   |
| PyPDF2           | PDF text extraction          |
| Pandas           | Data processing              |
| HTML/CSS         | User interface customization |

---

## 📂 Project Structure

```text
AI-Resume-Analyzer/
│
├── .devcontainer/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── other project files
```

### Main Files

**`main.py`**

Contains the main Streamlit application, resume processing, AI analysis, and user interface.

**`requirements.txt`**

Contains the Python libraries required to run the application.

**`README.md`**

Contains project documentation and setup instructions.

**`.gitignore`**

Prevents unnecessary or sensitive files from being uploaded to GitHub.

---



## ☁️ Streamlit Deployment

The application can be deployed using Streamlit Community Cloud.

General deployment process:

```text
GitHub Repository
       ↓
Connect Repository to Streamlit
       ↓
Select main.py
       ↓
Add GEMINI_API_KEY to Secrets
       ↓
Deploy
       ↓
Live Web Application
```

For deployment, make sure the repository contains:

```text
main.py
requirements.txt
```

and that your API key is configured in the deployment's **Secrets** section.

---

## 📊 Example Analysis

For a candidate applying for a Python Developer position, the application can evaluate areas such as:

```text
Candidate
    ↓
Skills
    ├── Python
    ├── SQL
    ├── Streamlit
    └── Machine Learning

Experience
    ↓
Relevant Experience

Education
    ↓
Academic Qualification

Projects
    ↓
Relevant Projects

Final Evaluation
    ↓
Overall Score
    ↓
Recommendation
```

---

## 🎯 Intended Use

The project can be useful for:

* Recruitment assistance
* Resume screening
* Candidate comparison
* HR technology demonstrations
* AI/ML academic projects
* Learning Generative AI
* Learning Streamlit
* Demonstrating AI-powered applications

---

## 🔒 Responsible AI

This project is intended to **assist recruiters**, not replace them.

AI-generated results may contain errors or biases. Candidate evaluations should therefore be reviewed by a human before making employment-related decisions.

The application should not be used as the sole basis for hiring or rejecting a candidate.

---

## 🚀 Future Improvements

Possible future improvements include:

* 📈 Candidate ranking dashboard
* 📊 Advanced analytics
* 👥 Recruiter dashboard
* 📑 Downloadable candidate reports
* 🔎 Advanced job-to-resume matching
* 🧠 Improved AI evaluation
* 📬 Candidate management system
* 🔐 User authentication
* 💾 Database integration
* 📱 Improved mobile interface
* 🌐 Multi-job management
* 📋 Interview question generation
* 📊 Candidate comparison charts

---

## 📸 Application Screenshots

Screenshots of the application can be added here.

Example:

```text
screenshots/
├── home.png
├── resume-upload.png
├── analysis.png
└── candidate-results.png
```

Then add them to this README using:

```markdown
![Application Home](screenshots/home.png)
```

---

## 🎓 Project Purpose

This project demonstrates how **Generative AI can be integrated with a web application to assist with resume analysis and candidate screening**.

It combines:

**Python + Streamlit + PDF Processing + Google Gemini AI**

to create an end-to-end AI-powered application.

---

## 👨‍💻 Author

Developed as an AI-powered resume analysis project using Python and Streamlit.

---

## ⭐ Project

If you find this project useful or interesting, consider giving the repository a ⭐.


