"""Module 3: ATS (Applicant Tracking System) compatibility scoring.

Total score = 100
  Keyword match with job description ... 40
  Section completeness ................. 20
  Contact information .................. 15
  Length & formatting .................. 15
  Measurable achievements .............. 10
"""
import re
from resume_parser import find_skills

REQUIRED_SECTIONS = ["summary", "skills", "education", "experience", "projects"]
STOPWORDS = set("""a an the and or of to in for with on at by is are be as we you our your
will this that from it their they have has must should looking required experience
knowledge good strong work team ability skills candidate role job years""".split())


def jd_keywords(jd_text: str) -> list:
    """Known skills found in the JD; falls back to frequent words."""
    skills = find_skills(jd_text)
    if skills:
        return skills
    words = [w for w in re.findall(r"[a-z+#.]{3,}", jd_text.lower()) if w not in STOPWORDS]
    return sorted(set(words), key=words.count, reverse=True)[:10]


def check_ats(parsed: dict, resume_text: str, jd_text: str = "") -> dict:
    score, tips, breakdown = 0, [], {}

    # 1. Keyword match (40)
    if jd_text.strip():
        keys = jd_keywords(jd_text)
        lower = resume_text.lower()
        matched = [k for k in keys if k in lower]
        missing = [k for k in keys if k not in lower]
        pts = round(40 * len(matched) / len(keys)) if keys else 0
        if missing:
            tips.append("Add missing keywords (if you truly have them): " + ", ".join(missing))
    else:
        matched, missing = parsed["skills"], []
        pts = min(40, len(matched) * 4)
        tips.append("No job description given - keyword score based on number of skills found.")
    breakdown["keyword_match"] = pts
    score += pts

    # 2. Sections (20)
    present = parsed["sections_found"]
    pts = round(20 * len([s for s in REQUIRED_SECTIONS if s in present]) / len(REQUIRED_SECTIONS))
    for s in REQUIRED_SECTIONS:
        if s not in present:
            tips.append(f"Add a clearly labelled '{s.title()}' section.")
    breakdown["sections"] = pts
    score += pts

    # 3. Contact info (15)
    pts = 0
    for field, p, msg in [("email", 6, "Add an email address."),
                          ("phone", 5, "Add a phone number."),
                          ("links", 4, "Add LinkedIn/GitHub links.")]:
        if parsed[field]:
            pts += p
        else:
            tips.append(msg)
    breakdown["contact_info"] = pts
    score += pts

    # 4. Length & formatting (15)
    pts = 0
    wc = parsed["word_count"]
    if 250 <= wc <= 800:
        pts += 8
    else:
        tips.append(f"Resume has {wc} words; aim for 250-800 (about 1 page for freshers).")
    if re.search(r"^\s*[-•*▪]", resume_text, re.M):
        pts += 4
    else:
        tips.append("Use bullet points for projects and experience.")
    if parsed["name"]:
        pts += 3
    else:
        tips.append("Put your full name on the first line.")
    breakdown["length_formatting"] = pts
    score += pts

    # 5. Measurable achievements (10)
    numbers = re.findall(r"\d+\s*%|\b\d{2,}\b|\$\s?\d+", resume_text)
    pts = 10 if len(numbers) >= 3 else (5 if numbers else 0)
    if pts < 10:
        tips.append("Quantify achievements (e.g. 'improved accuracy by 15%').")
    breakdown["achievements"] = pts
    score += pts

    grade = "Excellent" if score >= 80 else "Good" if score >= 60 else "Needs improvement"
    return {"ats_score": score, "grade": grade, "breakdown": breakdown,
            "matched_keywords": matched, "missing_keywords": missing, "suggestions": tips}
