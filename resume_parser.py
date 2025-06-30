import spacy
import pdfplumber
import re
import unicodedata  # Needed for Unicode normalization

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# 🧼 Sanitize raw PDF text
def sanitize_pdf_text(text):
    text = text.replace('\u00a0', ' ')  # Replace non-breaking space
    text = unicodedata.normalize('NFKD', text)  # Normalize ligatures & accents
    text = ''.join(c for c in text if ord(c) < 128)  # Remove non-ASCII
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    return text

# 🔡 Clean and normalize
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize extra spaces
    return text

# 📄 Extract text from PDF and sanitize it
def extract_text_from_pdf(path):
    with pdfplumber.open(path) as pdf:
        text = ''
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    # 🧼 Sanitize raw text
    text = sanitize_pdf_text(text)
    return text

# 🧠 Extract matching skills using skills.txt (multi-word aware)
def extract_skills(text):
    text = clean_text(text)

    # Load skills from file
    with open("skills.txt", "r") as f:
        skills_keywords = [line.strip().lower() for line in f if line.strip()]

    found = []
    for skill in skills_keywords:
        skill_cleaned = clean_text(skill)

        if ' ' in skill_cleaned:
            # Substring match for multi-word skills
            if skill_cleaned in text:
                found.append(skill)
        else:
            # Word boundary match for single-word skills
            pattern = r'\b' + re.escape(skill_cleaned) + r'\b'
            if re.search(pattern, text):
                found.append(skill)

    return found
