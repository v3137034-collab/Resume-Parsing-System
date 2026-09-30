"""Module 2: Extract structured information from resume text."""
import re

SKILLS = [
    "python", "java", "javascript", "c++", "c#", "sql", "html", "css", "react",
    "angular", "django", "flask", "node.js", "pandas", "numpy", "scikit-learn",
    "tensorflow", "machine learning", "deep learning", "nlp", "git", "github",
    "docker", "aws", "linux", "mongodb", "mysql", "postgresql", "excel",
    "rest api", "data analysis", "data structures", "algorithms", "oop",
]
DEGREES = [
    "b.tech", "btech", "b.e", "b.sc", "bsc", "bca", "bachelor",
    "m.tech", "mtech", "m.sc", "msc", "mca", "mba", "master", "phd", "diploma",
]
SECTION_HEADINGS = {
    "summary": ["summary", "objective", "profile", "about"],
    "skills": ["skills", "technical skills", "technologies"],
    "education": ["education", "academics", "qualification"],
    "experience": ["experience", "work history", "employment", "internship"],
    "projects": ["projects", "academic projects"],
    "certifications": ["certifications", "certificates", "achievements"],
}

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s-]?)?(?:\d[\s-]?){9,11}\d")
LINK_RE = re.compile(r"(?:https?://)?(?:www\.)?(?:linkedin\.com|github\.com)/[\w./-]+", re.I)
EXP_RE = re.compile(r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)", re.I)


def find_skills(text: str) -> list:
    text = text.lower()
    return [s for s in SKILLS
            if re.search(r"(?<![\w+#])" + re.escape(s) + r"(?![\w+#])", text)]


def find_sections(lines: list) -> list:
    """A section counts as present if a short line matches a known heading."""
    found = []
    for name, keys in SECTION_HEADINGS.items():
        for line in lines:
            clean = line.lower().strip(" :-")
            if len(clean.split()) <= 3 and clean in keys:
                found.append(name)
                break
    return found


def find_name(lines: list):
    for line in lines[:5]:
        if EMAIL_RE.search(line) or any(c.isdigit() for c in line):
            continue
        if 1 < len(line.split()) <= 4:
            return line.title()
    return None


def parse_resume(text: str) -> dict:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    email, phone = EMAIL_RE.search(text), PHONE_RE.search(text)
    years = [float(y) for y in EXP_RE.findall(text)]
    return {
        "name": find_name(lines),
        "email": email.group() if email else None,
        "phone": phone.group().strip() if phone else None,
        "links": sorted(set(LINK_RE.findall(text))),
        "skills": find_skills(text),
        "education": [l for l in lines if any(d in l.lower() for d in DEGREES)],
        "experience_years": max(years) if years else None,
        "sections_found": find_sections(lines),
        "word_count": len(text.split()),
    }
