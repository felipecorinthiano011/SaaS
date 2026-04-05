# AI Service (FastAPI + LangChain)

## Purpose

Advanced resume analysis using:
- **LangChain** for intelligent prompt chaining
- **OpenAI API** for NLP/LLM capabilities
- **pdfplumber** for PDF parsing
- **python-docx** for DOCX parsing

## Project Structure

```
app/
├── routers/              # API route handlers
│   └── analysis.py       # /analyze endpoint
├── services/             # Business logic
│   └── resume_analysis_service.py  # LangChain-based analysis
├── schemas/              # Pydantic request/response models
│   └── analysis.py       # AnalyzeRequest, AnalyzeResponse
├── utils/                # Utility functions
│   ├── file_parser.py    # PDF/DOCX parsing
│   └── ats_calculator.py # ATS score calculation
├── ai_prompts/           # LLM prompt templates
│   └── analysis_prompts.py
├── core/                 # Configuration
│   └── config.py         # Settings and env vars
└── main.py              # FastAPI app initialization
```

## Features

### 1. Extract ATS Keywords
- Analyzes job description using LLM
- Extracts technical skills, soft skills, certifications, required experience
- Returns structured keyword data

### 2. Analyze Resume
- Compares resume against extracted keywords
- Identifies matched and missing keywords
- Calculates detailed ATS score

### 3. Optimize Resume
- Generates ATS-friendly version
- Incorporates missing keywords naturally
- Improves formatting and impact

### 4. Generate Suggestions
- Provides actionable improvement recommendations
- Prioritizes by impact and effort
- Categorizes suggestions (Skills, Experience, etc.)

## API Endpoints

### POST /api/v1/analyze

**Request:**
```json
{
  "jobDescription": "Senior Java Developer with Spring Boot...",
  "resumeText": "I am a Java developer with 5 years..."
}
```

**Response:**
```json
{
  "atsScore": 78,
  "extractedKeywords": {
    "technical_keywords": ["Java", "Spring Boot", "PostgreSQL", ...],
    "soft_skills": ["Leadership", "Communication", ...],
    "certifications": ["AWS Solutions Architect", ...],
    "required_experience": ["Microservices", "Docker", ...]
  },
  "matchedKeywords": ["Java", "Spring Boot", ...],
  "missingKeywords": ["Kubernetes", "Docker", ...],
  "optimizedResume": "Enhanced resume text with better formatting and keyword incorporation...",
  "suggestions": [
    {
      "category": "Skills",
      "suggestion": "Add Kubernetes certification",
      "priority": "high",
      "impact": "Would improve ATS match by 15%"
    },
    ...
  ],
  "gapSummary": "Your resume is missing container orchestration experience..."
}
```

## Setup

### Prerequisites
- Python 3.11+
- OpenAI API key

### Installation

```powershell
cd ai-service

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create `.env` file:
```dotenv
AI_OPENAI_API_KEY=sk-...
AI_LLM_NAME=gpt-4o-mini
AI_DEBUG=false
```

Or set environment variables:
```powershell
$env:AI_OPENAI_API_KEY="sk-..."
$env:AI_LLM_NAME="gpt-4o-mini"
```

### Run Locally

```powershell
uvicorn app.main:app --reload --port 8000
```

## Testing

```powershell
# Run tests
python -m pytest -v

# Run with coverage
python -m pytest --cov=app tests/
```

## Dependencies

- **fastapi** - Web framework
- **langchain** - LLM orchestration
- **langchain-openai** - OpenAI integration
- **openai** - OpenAI API client
- **pdfplumber** - PDF text extraction
- **python-docx** - DOCX file parsing
- **pydantic** - Data validation
- **uvicorn** - ASGI server

## Advanced Features

### Prompt Engineering
Each analysis step uses specialized prompts in `app/ai_prompts/`:
- **Extract Keywords** - Extracts 50+ keywords from job description
- **Analyze Resume** - Identifies strengths, weaknesses, gaps
- **Optimize Resume** - Improves ATS compatibility
- **Generate Suggestions** - Creates prioritized action items

### File Parsing
Supports both PDF and DOCX resume formats:
- PDFs: Uses pdfplumber for reliable text extraction
- DOCX: Uses python-docx for accurate parsing
- Automatic format detection

### ATS Score Calculation
Comprehensive scoring:
- Keyword matching (40%)
- Formatting/Structure (20%)
- Content quality (40%)
- Range: 0-100

## Next Steps

1. Add file upload support (receive PDF/DOCX directly)
2. Implement caching for repeated analyses
3. Add batch analysis capability
4. Implement usage tracking and rate limiting
5. Add webhook support for async processing
6. Support for multiple LLM providers

## Troubleshooting

**OpenAI API errors:**
- Verify `AI_OPENAI_API_KEY` is set correctly
- Check API key has required permissions
- Ensure account has credits

**PDF parsing errors:**
- Ensure PDF is not password-protected
- Check file is not corrupted
- Try re-exporting from source application

**JSON parsing errors:**
- Model may be returning non-JSON
- Increase temperature or adjust prompt
- Check token limits aren't being exceeded

