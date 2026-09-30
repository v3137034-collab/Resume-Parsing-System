# Resume Parsing System with ATS Score Checker - Documentation

## 1. Introduction
Companies use Applicant Tracking Systems (ATS) to automatically screen resumes.
Many good resumes get rejected because they lack keywords, clear sections or
proper formatting. This project parses a resume, converts it into structured
data, and estimates its ATS-friendliness.

## 2. Problem Statement
Manually reading hundreds of resumes is slow and inconsistent, and candidates
do not know why their resumes fail automated screening. The project provides an
automated way to extract resume data and evaluate ATS compatibility.

## 3. Objectives
1. Read resumes in TXT, PDF and DOCX formats.
2. Extract key candidate details.
3. Score the resume against a job description.
4. Provide suggestions to improve the resume.

## 4. Scope
- Works on text-based resumes in English.
- Command-line tool; rule-based (no machine learning).
- Scanned image PDFs are not supported.

## 5. Requirements
| Item | Requirement |
|---|---|
| Language | Python 3.8+ |
| Standard libraries | `re`, `argparse`, `json`, `pathlib`, `unittest` |
| External (optional) | `pypdf` (PDF), `python-docx` (DOCX) |
| OS | Windows / Linux / macOS |

## 6. System Architecture
```
            +-----------------+
 Resume --> |  file_reader.py | --> raw text
            +-----------------+
                     |
                     v
            +------------------+      +-------------------+
            | resume_parser.py | ---> |  structured data  |
            +------------------+      +-------------------+
                                               |
 Job description ---------------------+        v
                                      +--> +----------------+
                                           | ats_checker.py | --> score + tips
                                           +----------------+
                                                    |
                                                    v
                                               main.py (report / JSON)
```

## 7. Module Description

### 7.1 file_reader.py
`read_resume(path)` detects the extension and returns plain text.
PDF uses `pypdf.PdfReader`, DOCX uses `python-docx`, TXT uses `pathlib`.

### 7.2 resume_parser.py
| Function | Purpose |
|---|---|
| `find_name(lines)` | first short line without digits/email in the top 5 lines |
| `find_skills(text)` | matches text against the `SKILLS` list using regex word boundaries |
| `find_sections(lines)` | detects headings like Skills, Education, Projects |
| `parse_resume(text)` | returns a dictionary with all extracted fields |

Regular expressions used: email, phone, LinkedIn/GitHub links, "N years" experience.

### 7.3 ats_checker.py
| Function | Purpose |
|---|---|
| `jd_keywords(jd_text)` | skills found in the job description (falls back to frequent words) |
| `check_ats(parsed, text, jd)` | calculates score, breakdown, matched/missing keywords and suggestions |

### 7.4 main.py
Parses command-line arguments, runs the pipeline, prints the report or JSON.

## 8. ATS Scoring Algorithm
```
keyword_score  = 40 * matched_keywords / total_jd_keywords
section_score  = 20 * present_required_sections / 5
contact_score  = email(6) + phone(5) + links(4)
format_score   = length 250-800 words (8) + bullet points (4) + name found (3)
achievement    = 10 if >=3 numbers/percentages, 5 if 1-2, else 0
total          = sum of the above (max 100)
```
Grade: >=80 Excellent, 60-79 Good, <60 Needs improvement.
If no job description is supplied, keyword score = min(40, skills_found x 4).

## 9. Output Format (JSON)
```json
{
  "parsed": {
    "name": "Rahul Sharma",
    "email": "rahul.sharma@example.com",
    "phone": "+91 98765 43210",
    "links": ["github.com/rahulsharma"],
    "skills": ["python", "sql"],
    "education": ["B.Tech in Computer Engineering, 2024"],
    "experience_years": 1.0,
    "sections_found": ["summary", "skills"],
    "word_count": 155
  },
  "ats": {
    "ats_score": 88,
    "grade": "Excellent",
    "breakdown": {"keyword_match": 36, "sections": 20, "contact_info": 15,
                  "length_formatting": 7, "achievements": 10},
    "matched_keywords": ["python"],
    "missing_keywords": ["linux"],
    "suggestions": ["Add missing keywords (if you truly have them): linux"]
  }
}
```

## 10. Installation and Usage

### Step-by-step
1. Install Python 3.8+ and verify: `python --version`
2. Download or clone the project and open a terminal in its folder.
3. (Optional) create a virtual environment:
   `python -m venv venv` then activate it
   (`venv\Scripts\activate` on Windows, `source venv/bin/activate` on Linux/macOS).
4. Install dependencies: `pip install -r requirements.txt`
5. Run the sample: `python main.py data/sample_resume.txt`
6. Run with a job description: `python main.py data/sample_resume.txt --jd data/sample_job_description.txt`
7. Use your own resume: `python main.py path/to/resume.pdf --jd path/to/job.txt`
8. Get JSON: add `--json`
9. Run tests: `python -m unittest discover -s tests`

### Command-line options
| Option | Description |
|---|---|
| `resume` | path to .txt / .pdf / .docx file (required) |
| `--jd FILE` | job description text file (optional) |
| `--json` | print JSON instead of the report |

## 11. Testing
| Test | Checks |
|---|---|
| `test_contact_details` | email and phone extracted |
| `test_name_and_skills` | name and "python" skill found |
| `test_ats_score_range` | score always between 0 and 100 |
| `test_missing_keyword_detected` | missing JD keyword is reported |

## 12. Limitations
- Fixed skill and degree lists (edit `SKILLS` and `DEGREES` to extend).
- Heuristic name detection; multi-column PDFs may extract in wrong order.
- The ATS score is an estimate, not the result of a real ATS.
- English only.

## 13. Future Enhancements
- spaCy named-entity recognition for names and organisations
- OCR (pytesseract) for scanned resumes
- TF-IDF and cosine similarity for semantic job matching
- Streamlit / Flask web interface
- Database and ranking of multiple resumes

## 14. Conclusion
The project demonstrates text extraction, regular expressions, rule-based
scoring and modular design in Python, and gives candidates practical feedback
to make resumes more ATS-friendly.

## 15. References
- Python documentation: https://docs.python.org/3/
- pypdf: https://pypdf.readthedocs.io
- python-docx: https://python-docx.readthedocs.io
- Git and GitHub docs: https://docs.github.com
