import re
import unicodedata

# 🧼 Sanitize JD text before cleaning
def sanitize_text(text):
    text = text.replace('\u00a0', ' ')  # Replace non-breaking space
    text = unicodedata.normalize('NFKD', text)  # Normalize ligatures & accents
    text = ''.join(c for c in text if ord(c) < 128)  # Remove non-ASCII
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    return text

# 🔡 Final clean: lowercase and remove special chars
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize spaces
    return text

# 🎯 Main JD skill extractor
def extract_jd_skills(jd_text):
    jd_text = sanitize_text(jd_text)         # Sanitize first
    jd_text = clean_text(jd_text)            # Then clean

    # Load predefined skills from file
    with open('skills.txt', 'r') as f:
        predefined_skills = [line.strip().lower() for line in f if line.strip()]

    found_skills = []
    for skill in predefined_skills:
        skill_pattern = clean_text(skill)  # Also clean multi-word skills
        pattern = r'\b' + re.escape(skill_pattern) + r'\b'

        # For multi-word skills: use substring match
        if ' ' in skill_pattern:
            if skill_pattern in jd_text:
                found_skills.append(skill)
        else:
            if re.search(pattern, jd_text):
                found_skills.append(skill)

    return found_skills
