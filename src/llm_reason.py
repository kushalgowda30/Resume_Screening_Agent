import re

def analyze_resume(resume_text, jd_text):

    resume_words = set(re.findall(r"\b[a-zA-Z+#.]+\b", resume_text.lower()))
    jd_words = set(re.findall(r"\b[a-zA-Z+#.]+\b", jd_text.lower()))

    matched = sorted(list(resume_words & jd_words))
    missing = sorted(list(jd_words - resume_words))

    matched_skills = matched[:10]
    missing_skills = missing[:10]

    suggestions = []

    if missing_skills:
        suggestions.append("Add missing technical skills mentioned in the Job Description.")
        suggestions.append("Include relevant project experience.")
        suggestions.append("Use keywords from the Job Description.")
    else:
        suggestions.append("Resume strongly matches the Job Description.")

    return {
        "matched": matched_skills,
        "missing": missing_skills,
        "suggestions": suggestions
    }