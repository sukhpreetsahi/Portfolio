"""Reusable text preprocessing helpers for policy-document analysis.

The public portfolio version contains no policy data. Supply documents at runtime
from a source you are authorised to process.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable


CHUNK_SIZE = 250
CHUNK_OVERLAP = 75
MIN_CHUNK_SIZE = 50
LARGE_SECTION_THRESHOLD = 350


def remove_table_of_contents(text: str) -> str:
    """Remove obvious table-of-contents lines containing dot/dash leaders."""
    lines = text.splitlines()
    cleaned: list[str] = []
    for line in lines:
        if re.search(r"[.\-_]{4,}\s*\d{1,3}\s*$", line):
            continue
        if re.search(r"^[\s.\-_]{4,}\d{0,3}\s*$", line):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def clean_text(text: str) -> str:
    """Normalise whitespace while retaining readable text."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Create overlapping word-based chunks."""
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    words = text.split()
    step = chunk_size - overlap
    chunks: list[str] = []
    for start in range(0, len(words), step):
        chunk = words[start : start + chunk_size]
        if len(chunk) >= MIN_CHUNK_SIZE:
            chunks.append(" ".join(chunk))
    return chunks


def adaptive_split(text: str) -> list[str]:
    """Keep short sections intact and chunk large sections."""
    if len(text.split()) <= LARGE_SECTION_THRESHOLD:
        return [text.strip()] if text.strip() else []
    return chunk_text(text)


def build_chunk_records(text: str, source_file: str = "input") -> list[dict]:
    """Turn extracted text into metadata records suitable for embedding."""
    cleaned = clean_text(remove_table_of_contents(text))
    segments = adaptive_split(cleaned)
    return [
        {
            "chunk_id": f"{i:03d}",
            "source_file": source_file,
            "text": segment,
            "word_count": len(segment.split()),
        }
        for i, segment in enumerate(segments)
    ]


def extract_pdf_text(pdf_path: str | Path) -> str:
    """Extract text from a PDF using PyMuPDF.

    PDF files are deliberately not included in this repository.
    """
    import fitz

    full_text: list[str] = []
    with fitz.open(pdf_path) as document:
        for page in document:
            text = page.get_text("text")
            if text and text.strip():
                full_text.append(text)
    return "\n".join(full_text)


def process_pdf(pdf_path: str | Path) -> list[dict]:
    """Extract, clean and chunk one authorised PDF input."""
    path = Path(pdf_path)
    return build_chunk_records(extract_pdf_text(path), path.name)
