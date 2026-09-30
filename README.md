# Resume Parsing System with ATS Score Checker

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A beginner-friendly Python project that **parses resumes** (TXT / PDF / DOCX) into
structured data and gives an **ATS (Applicant Tracking System) score out of 100**
with suggestions to improve the resume.

## Features
- Extracts name, email, phone, LinkedIn/GitHub links, skills, education, experience
- Detects resume sections (Summary, Skills, Education, Experience, Projects...)
- ATS score with breakdown and improvement tips
- Compares the resume against a job description (matched / missing keywords)
- Report view or JSON output
- Unit tests included

## Quick Start

```bash
# 1. Clone
git clone https://github.com/<your-username>/resume-parsing-system.git
cd resume-parsing-system

# 2. (Optional) virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install (only needed for PDF / DOCX)
pip install -r requirements.txt

# 4. Run
python main.py data/sample_resume.txt
python main.py data/sample_resume.txt --jd data/sample_job_description.txt
python main.py my_resume.pdf --jd job.txt --json

# 5. Test
python -m unittest discover -s tests
```

## Sample Output
```
Score: 88/100  (Excellent)
  - Keyword Match       36
  - Sections            20
  - Contact Info        15
  - Length Formatting   7
  - Achievements        10
Matched keywords: python, sql, django, machine learning, git, docker, aws, rest api
Missing keywords: linux
```

## Project Structure
```
resume-parsing-system/
├── main.py              # CLI entry point
├── file_reader.py       # reads TXT / PDF / DOCX
├── resume_parser.py     # information extraction
├── ats_checker.py       # ATS scoring
├── data/                # sample resume + job description
├── tests/               # unit tests
├── docs/
│   ├── DOCUMENTATION.md # full project documentation
│   └── GITHUB_GUIDE.md  # how to push to GitHub
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Documentation
- [Full documentation](docs/DOCUMENTATION.md)
- [GitHub push guide](docs/GITHUB_GUIDE.md)

## License
MIT
