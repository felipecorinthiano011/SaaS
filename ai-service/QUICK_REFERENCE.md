# Quick Reference - Resume Text Extraction

## Main Function

```python
from app.utils.file_parser import extract_resume_text

# Extract and clean resume text in one call
clean_text = extract_resume_text(file)
```

## What It Does

1. **Accepts** → PDF, DOCX, or file-like objects
2. **Extracts** → Raw text from the file
3. **Cleans** → Removes sensitive/formatting data
4. **Returns** → AI-ready plain text

## Automatically Removes

✅ Email addresses  
✅ Phone numbers  
✅ URLs and web links  
✅ LinkedIn/GitHub/Twitter profiles  
✅ Page numbers  
✅ Headers/footers with separators  
✅ Extra whitespace  

## Usage Examples

### Example 1: File Path
```python
text = extract_resume_text("path/to/resume.pdf")
```

### Example 2: Path Object
```python
from pathlib import Path
text = extract_resume_text(Path("resume.docx"))
```

### Example 3: FastAPI Upload
```python
from fastapi import UploadFile

@app.post("/resume/upload")
async def upload_resume(file: UploadFile):
    resume_text = extract_resume_text(file)
    # Now use resume_text for analysis
```

### Example 4: With Error Handling
```python
try:
    text = extract_resume_text("resume.pdf")
except ValueError as e:
    print(f"Parsing error: {e}")
except ImportError as e:
    print(f"Missing library: {e}")
```

## Real-World Example

### Input Resume
```
JOHN DOE
john.doe@example.com | (555) 123-4567
linkedin.com/in/johndoe | github.com/johndoe

SENIOR DEVELOPER
Page 1
====================

5+ years Java/Spring Boot experience
```

### Output (Clean Text)
```
JOHN DOE
SENIOR DEVELOPER
5+ years Java/Spring Boot experience
```

## Supported Formats

| Format | Extension | Status |
|--------|-----------|--------|
| PDF | .pdf | ✅ |
| Word | .docx | ✅ |
| Word (Old) | .doc | ✅ |

## Integration with AI Service

```python
from app.utils.file_parser import extract_resume_text

# Get clean text
resume_text = extract_resume_text(uploaded_file)

# Send to AI service for analysis
analysis = ai_service.analyze(
    job_description=job_desc,
    resume_text=resume_text  # Clean, privacy-safe text
)
```

## Other Useful Functions

```python
from app.utils.file_parser import clean_text, extract_json_from_text

# Clean already-extracted text
cleaned = clean_text(raw_text)

# Extract JSON from LLM responses
result = extract_json_from_text('{"ats_score": 85} ...')
```

## Documentation

- **Full Guide**: `RESUME_TEXT_EXTRACTION.md`
- **Tests**: `tests/test_file_parser.py`
- **Implementation Details**: `IMPLEMENTATION_SUMMARY.md`

