def match_score(resume_skills, jd_skills):
    # Normalize skills: lowercase and remove duplicate whitespace
    resume_skills = [s.lower().strip() for s in resume_skills if s.strip()]
    jd_skills = [s.lower().strip() for s in jd_skills if s.strip()]
    
    matched = set(resume_skills).intersection(set(jd_skills))
    
    # Avoid division by zero
    score = (len(matched) / len(set(jd_skills)) * 100) if jd_skills else 0
    
    return round(score, 2), list(matched)
