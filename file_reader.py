"""Module 1: Read text out of TXT, PDF and DOCX resumes."""
from pathlib import Path


def read_resume(path: str) -> str:
    p = Path(path)
    ext = p.suffix.lower()
    if ext == ".txt":
        return p.read_text(encoding="utf-8", errors="ignore")
    if ext == ".pdf":
        from pypdf import PdfReader
        return "\n".join(page.extract_text() or "" for page in PdfReader(str(p)).pages)
    if ext == ".docx":
        from docx import Document
        return "\n".join(par.text for par in Document(str(p)).paragraphs)
    raise ValueError(f"Unsupported file type '{ext}'. Use .txt, .pdf or .docx")
