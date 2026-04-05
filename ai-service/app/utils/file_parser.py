"""Utility functions for parsing resume files."""

import json
from typing import Optional

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    from docx import Document
except ImportError:
    Document = None


def parse_pdf(file_path: str) -> str:
    """Extract text from PDF file."""
    if not pdfplumber:
        raise ImportError("pdfplumber is not installed. Install with: pip install pdfplumber")

    text = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return "\n".join(text)
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")


def parse_docx(file_path: str) -> str:
    """Extract text from DOCX file."""
    if not Document:
        raise ImportError("python-docx is not installed. Install with: pip install python-docx")

    text = []
    try:
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text)
        return "\n".join(text)
    except Exception as e:
        raise ValueError(f"Failed to parse DOCX: {str(e)}")


def parse_resume_file(file_path: str, file_name: str) -> str:
    """Parse resume file (PDF or DOCX) and extract text."""
    file_name_lower = file_name.lower()

    if file_name_lower.endswith('.pdf'):
        return parse_pdf(file_path)
    elif file_name_lower.endswith('.docx') or file_name_lower.endswith('.doc'):
        return parse_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_name}. Only PDF and DOCX are supported.")


def extract_json_from_text(text: str) -> dict:
    """Extract JSON object from text response."""
    # Find first { and last } in the text
    start_idx = text.find('{')
    end_idx = text.rfind('}') + 1

    if start_idx == -1 or end_idx == 0:
        raise ValueError("No JSON object found in response")

    json_str = text[start_idx:end_idx]
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {str(e)}")


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    # Remove extra whitespace
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)

