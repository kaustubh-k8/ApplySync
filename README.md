#  SkillSync — AI-Powered Resume to JD Matching Tool

**SkillSync** is an intelligent NLP-powered web app that scans resumes, extracts key skills, and matches them against job descriptions to calculate a job fit score.

It’s designed for recruiters, job seekers, and career platforms — streamlining resume screening with real-world accuracy and instant feedback.


## Features

- Upload a resume in PDF format  
- Paste or type or upload (pdf) a Job Description (JD)  
- Extracts skills using NLP and regex  
- Matches resume skills to JD skills  
- Calculates a visual match score  
- Shows matched and missing skills  
- Download result as PDF report  
- Handles noisy PDFs from Word, Canva, etc


---
## Why This Project?

In today's market, it's not just about listing your skills, it's about showing relevance to the job. This project simulates real-world recruitment logic, handles dirty resume data, and shows practical application of Python, NLP, and regex.


## How It Works

1. Resume PDF is parsed using `spaCy` NLP to extract skills
2. JD is analyzed using regex-based matching from a dynamic list in `skills.txt`
3. Overlapping skills are matched → a score is generated
4. Matched vs Missing skills shown visually
5. User can download a report as PDF

---

##  Sample Inputs

### Sample JD (`sample_jd.txt`):

We are seeking a passionate AI-Embedded Systems Engineer to join our dynamic R&D team.

Responsibilities:
- Design and deploy microcontroller-based AI systems
- Strong Python, C++, and SQL required
- Experience with RTOS, Flask, React, and Power BI
- Excellent communication and teamwork


### Sample Resume (`sample_resume.pdf`):
- Contains skillsets like Python, Power BI, SQL, RTOS, communication, etc.

---

##  How to Run Locally

### 1. Clone the Repo
```
git clone https://github.com/your-username/AI-Resume-Scanner.git
cd AI-Resume-Scanner
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Run the App
```
streamlit run app.py
```

---

## Folder Structure
```
├── app.py                  # Streamlit frontend
├── resume_parser.py        # Extracts skills from resume
├── jd_parser.py            # Extracts skills from JD
├── matcher.py              # Matching logic
├── skills.txt              # Master list of skills
├── sample_resume.pdf       # Sample for testing
├── sample_jd.txt           # Sample job description
├── requirements.txt
└── README.md
```

---

## Tech Stack
- Python
- Streamlit
- spaCy
- Regex
- PDFplumber / PyPDF2

---

## Screenshots (add these after upload)
- Upload & JD input
- Match result
- PDF download button

---

## Credits
Built by **Kaustubh**






