"""Resume Parsing System with ATS Score - command line entry point.

Examples:
  python main.py data/sample_resume.txt
  python main.py data/sample_resume.txt --jd data/sample_job_description.txt
  python main.py my_resume.pdf --jd job.txt --json
"""
import argparse
import json

from file_reader import read_resume
from resume_parser import parse_resume
from ats_checker import check_ats


def print_report(parsed: dict, ats: dict):
    line = "=" * 50
    print(f"{line}\n RESUME PARSING REPORT\n{line}")
    print(f"Name       : {parsed['name']}")
    print(f"Email      : {parsed['email']}")
    print(f"Phone      : {parsed['phone']}")
    print(f"Links      : {', '.join(parsed['links']) or '-'}")
    print(f"Skills     : {', '.join(parsed['skills']) or '-'}")
    print(f"Education  : {'; '.join(parsed['education']) or '-'}")
    print(f"Experience : {parsed['experience_years']} years")
    print(f"Sections   : {', '.join(parsed['sections_found']) or '-'}")
    print(f"\n{line}\n ATS COMPATIBILITY\n{line}")
    print(f"Score: {ats['ats_score']}/100  ({ats['grade']})")
    for k, v in ats["breakdown"].items():
        print(f"  - {k.replace('_', ' ').title():<20}{v}")
    print(f"Matched keywords: {', '.join(ats['matched_keywords']) or '-'}")
    print(f"Missing keywords: {', '.join(ats['missing_keywords']) or '-'}")
    if ats["suggestions"]:
        print("\nSuggestions:")
        for s in ats["suggestions"]:
            print(f"  * {s}")


def main():
    ap = argparse.ArgumentParser(description="Resume parser with ATS score")
    ap.add_argument("resume", help="path to .txt, .pdf or .docx resume")
    ap.add_argument("--jd", help="path to job description .txt (optional)")
    ap.add_argument("--json", action="store_true", help="print JSON instead of report")
    args = ap.parse_args()

    text = read_resume(args.resume)
    jd = open(args.jd, encoding="utf-8").read() if args.jd else ""
    parsed = parse_resume(text)
    ats = check_ats(parsed, text, jd)

    if args.json:
        print(json.dumps({"parsed": parsed, "ats": ats}, indent=2))
    else:
        print_report(parsed, ats)


if __name__ == "__main__":
    main()
