# Resume Text Extraction Module

## Overview

The `file_parser.py` module provides functions for extracting and cleaning text from resume files (PDF and DOCX formats). It's designed to prepare resume text for AI processing by removing sensitive information and formatting artifacts.

## Features

### 1. **File Format Support**
- **PDF** - Uses `pdfplumber` for reliable text extraction from PDF documents
- **DOCX** - Uses `python-docx` for accurate parsing of Word documents

### 2. **Text Cleaning**

The `clean_text()` function automatically removes:
- ✅ Email addresses (e.g., john.doe@example.com)
- ✅ Phone numbers in various formats (e.g., (555) 123-4567, +1-555-123-4567)
- ✅ URLs and web links (http, https, www, ftp)
- ✅ Social profile URLs (LinkedIn, GitHub, Twitter)
- ✅ Page numbers and headers/footers
- ✅ Separator lines (dashes, equals signs, asterisks)
- ✅ Extra whitespace and formatting

### 3. **AI-Ready Output**
Returns clean, plain text optimized for:
- LLM processing (OpenAI, Claude, etc.)
- Text analysis algorithms
- Information extraction pipelines

## Functions

### `extract_resume_text(file) -> str`

**Main function** - Extracts and cleans text from a resume file.

**Parameters:**
- `file`: File input (str path, Path object, or file-like object with `.filename` attribute)

**Returns:**
- `str`: Clean plain text from the resume

**Raises:**
- `ValueError`: If file format is unsupported or parsing fails
- `ImportError`: If required libraries are not installed

**Example:**
```python
from app.utils.file_parser import extract_resume_text

# From file path
clean_text = extract_resume_text("resume.pdf")

# From Path object
from pathlib import Path
clean_text = extract_resume_text(Path("resume.docx"))

# From file-like object (FastAPI UploadFile)
clean_text = extract_resume_text(uploaded_file)
```

### `clean_text(text: str) -> str`

**Cleans** raw text by removing emails, links, phone numbers, extra whitespace, and headers.

**Parameters:**
- `text`: Raw text to clean

**Returns:**
- `str`: Clean text suitable for AI processing

**Example:**
```python
from app.utils.file_parser import clean_text

raw_text = "JOHN DOE john@example.com (555) 123-4567..."
cleaned = clean_text(raw_text)
# Output: "JOHN DOE..."
```

### `parse_resume_file(file_path: str, file_name: str) -> str`

**Parses** resume file (PDF or DOCX) and extracts raw text.

**Parameters:**
- `file_path`: Path to the file
- `file_name`: Name of the file (used for format detection)

**Returns:**
- `str`: Raw extracted text

### `parse_pdf(file_path: str) -> str`

**Extracts** text from PDF files using pdfplumber.

**Parameters:**
- `file_path`: Path to the PDF file

**Returns:**
- `str`: Text content from all pages

### `parse_docx(file_path: str) -> str`

**Extracts** text from DOCX files using python-docx.

**Parameters:**
- `file_path`: Path to the DOCX file

**Returns:**
- `str`: Text content from all paragraphs

### `extract_json_from_text(text: str) -> dict`

**Extracts** JSON object from text (useful for parsing LLM responses).

**Parameters:**
- `text`: Text containing JSON

**Returns:**
- `dict`: Parsed JSON object

**Example:**
```python
from app.utils.file_parser import extract_json_from_text

text = 'Here is analysis: {"ats_score": 85, "keywords": ["Java"]} and more'
result = extract_json_from_text(text)
# Output: {"ats_score": 85, "keywords": ["Java"]}
```

## Usage in Backend API

### Integration with FastAPI Resume Upload Endpoint

```python
from fastapi import UploadFile, File
from app.utils.file_parser import extract_resume_text

@app.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    # Extract and clean text
    resume_text = extract_resume_text(file)
    
    # Store or send to AI service
    return {
        "status": "success",
        "text_length": len(resume_text),
        "preview": resume_text[:200]
    }
```

### Integration with Job Analysis Workflow

```python
from app.utils.file_parser import extract_resume_text, clean_text

def analyze_resume_for_job(resume_file, job_description):
    # Extract resume text
    resume_text = extract_resume_text(resume_file)
    
    # Send to AI service for analysis
    analysis = ai_service.analyze(
        job_description=job_description,
        resume_text=resume_text
    )
    
    return analysis
```

## Supported File Formats

| Format | Extension | Library | Status |
|--------|-----------|---------|--------|
| PDF | `.pdf` | pdfplumber | ✅ Supported |
| Word | `.docx` | python-docx | ✅ Supported |
| Word (Legacy) | `.doc` | python-docx | ✅ Supported |
| Text | `.txt` | - | ❌ Not recommended |

## Text Cleaning Examples

### Before and After

**Before:**
```
JOHN ANDERSON
john.anderson@gmail.com | (415) 555-0123
linkedin.com/in/johnanderson | github.com/janderson

SENIOR SOFTWARE ENGINEER
Page 1

================================================

10+ years of experience building web applications
```

**After:**
```
JOHN ANDERSON
SENIOR SOFTWARE ENGINEER
10+ years of experience building web applications
```

## Regex Patterns Used

| Pattern | Purpose |
|---------|---------|
| `\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z\|a-z]{2,}\b` | Email addresses |
| `http[s]?://(?:[a-zA-Z]\|[0-9]\|[$-_@.&+]\|[!*\\(\\),]\|(?:%[0-9a-fA-F][0-9a-fA-F]))+` | HTTP/HTTPS URLs |
| `www\.[a-zA-Z0-9-]+\.[a-zA-Z]{2,}` | WWW URLs |
| `\b(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b` | Phone numbers |
| `linkedin\.com/in/[^\s]+` | LinkedIn profiles |
| `github\.com/[^\s]+` | GitHub profiles |
| `[-\s]*page\s+\d+[-\s]*` | Page numbers |

## Dependencies

```
pdfplumber==0.11.2      # PDF text extraction
python-docx==0.8.11     # DOCX file parsing
```

## Performance Considerations

- **PDF Parsing**: Efficient for most resumes; handles multi-page documents
- **DOCX Parsing**: Fast parsing of Word documents
- **Text Cleaning**: All regex operations are optimized for performance
- **Memory Usage**: Suitable for file sizes up to 10MB

## Error Handling

The module provides clear error messages for common issues:

```python
try:
    text = extract_resume_text("resume.txt")
except ValueError as e:
    print(f"Error: {e}")  # "Unsupported file format: resume.txt"

try:
    text = extract_resume_text("corrupted.pdf")
except ValueError as e:
    print(f"Error: {e}")  # "Failed to parse PDF: ..."
```

## Testing

Run the included test suite:

```bash
# Using pytest
python -m pytest tests/test_file_parser.py -v

# Or the test script
python test_file_parser.py
```

Test coverage includes:
- Email removal
- URL/link removal
- Phone number removal
- Page number/separator removal
- Extra whitespace cleanup
- JSON extraction
- Comprehensive realistic resume cleaning

## Future Enhancements

- [ ] Support for RTF format
- [ ] OCR for scanned resume images
- [ ] Language detection and multi-language support
- [ ] Resume section detection (Experience, Skills, etc.)
- [ ] Resume structure preservation option
- [ ] Batch processing support

