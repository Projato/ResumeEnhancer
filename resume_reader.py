from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import pdfplumber


SupportedExt = Literal[".txt", ".pdf"]


@dataclass
class ResumeDocument:
    path: Path
    ext: SupportedExt
    text: str


def read_resume(path: str | Path) -> ResumeDocument:
    #Read a resume from .txt or .pdf and return extracted text.
    p = Path(path)

    if not p.exists():
        raise FileNotFoundError(f"Resume file not found: {p}")

    ext = p.suffix.lower()
    if ext not in (".txt", ".pdf"):
        raise ValueError(f"Unsupported file type: {ext}. Use .txt or .pdf")

    if ext == ".txt":
        text = _read_txt(p)
        return ResumeDocument(path=p, ext=".txt", text=text)

    text = _read_pdf(p)
    return ResumeDocument(path=p, ext=".pdf", text=text)


def _read_txt(path: Path) -> str:
    # utf-8 first, fallback to cp1252 for some Windows-saved resumes
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw = path.read_text(encoding="cp1252", errors="replace")

    return _normalize_text(raw)


def _read_pdf(path: Path) -> str:
    chunks: list[str] = []

    # pdfplumber works only for text-based PDFs (not scanned images)
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text() or ""
            page_text = page_text.strip()
            if page_text:
                chunks.append(page_text)

    text = "\n\n".join(chunks)
    return _normalize_text(text)


def _normalize_text(text: str) -> str:
    """
    Light cleanup so downstream parsing is easier.
    Keep it conservative (don't destroy formatting).
    """
    # Normalize newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove excessive trailing spaces per line
    lines = [ln.rstrip() for ln in text.split("\n")]

    # Remove *some* repeated blank lines (keep at most 1 blank line)
    cleaned: list[str] = []
    blank_streak = 0
    for ln in lines:
        if ln.strip() == "":
            blank_streak += 1
            if blank_streak <= 1:
                cleaned.append("")
        else:
            blank_streak = 0
            cleaned.append(ln)

    return "\n".join(cleaned).strip()