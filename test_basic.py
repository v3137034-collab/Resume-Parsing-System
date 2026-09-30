import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from resume_parser import parse_resume
from ats_checker import check_ats

with open(os.path.join(ROOT, "data", "sample_resume.txt"), encoding="utf-8") as f:
    TEXT = f.read()


class TestResumeSystem(unittest.TestCase):
    def setUp(self):
        self.parsed = parse_resume(TEXT)

    def test_contact_details(self):
        self.assertEqual(self.parsed["email"], "rahul.sharma@example.com")
        self.assertIsNotNone(self.parsed["phone"])

    def test_name_and_skills(self):
        self.assertEqual(self.parsed["name"], "Rahul Sharma")
        self.assertIn("python", self.parsed["skills"])

    def test_ats_score_range(self):
        result = check_ats(self.parsed, TEXT, "Python Django Kubernetes")
        self.assertTrue(0 <= result["ats_score"] <= 100)

    def test_missing_keyword_detected(self):
        result = check_ats(self.parsed, TEXT, "We need Python and Angular")
        self.assertIn("angular", result["missing_keywords"])


if __name__ == "__main__":
    unittest.main()
