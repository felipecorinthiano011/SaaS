# ATS Keywords Extraction Service

## Overview

The ATS Keywords Extraction Service analyzes job descriptions and extracts keywords that Applicant Tracking Systems (ATS) look for. Keywords are organized into four categories:

- **Skills**: Technical and professional skills (Java, Python, System Design, etc.)
- **Technologies**: Frameworks, platforms, databases (Spring Boot, AWS, PostgreSQL, etc.)
- **Tools**: Software tools and applications (Git, Docker, Jenkins, etc.)
- **Soft Skills**: Soft skills and competencies (Leadership, Communication, Problem Solving, etc.)

## Architecture

The service follows **Clean Architecture** principles:

```
┌─────────────────────────────────────────────────────┐
│                   API Layer (FastAPI)               │
│              routers/keywords.py                    │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│              Application Logic                       │
│      services/ats_keywords_service.py               │
│  - extract_keywords()                               │
│  - extract_and_analyze()                            │
│  - _extract_with_llm()                              │
│  - _extract_with_regex()                            │
└─────────────────┬───────────────────────────────────┘
                  │
          ┌───────┴────────┐
          │                │
┌─────────▼──────┐ ┌──────▼──────────────┐
│  Utility Layer │ │  Data Models        │
├────────────────┤ ├─────────────────────┤
│  ats_keyword_  │ │ schemas/ats_keywords│
│  utils.py      │ │ .py                 │
│                │ │                     │
│ - extract_     │ │ - ATSKeywords       │
│   keywords_    │ │ - ATSKeywords       │
│   regex()      │ │   Response          │
│                │ │ - ATSKeywords       │
│ - categorize_  │ │   Request           │
│   keywords_    │ │                     │
│   heuristic()  │ │                     │
│                │ │                     │
│ - remove_      │ │                     │
│   duplicates_  │ │                     │
│   preserve_    │ │                     │
│   order()      │ │                     │
│                │ │                     │
│ - get_most_    │ │                     │
│   common_      │ │                     │
│   keywords()   │ │                     │
└────────────────┘ └─────────────────────┘
```

## Key Components

### 1. ATSKeywordsService (`services/ats_keywords_service.py`)

**Main responsibility**: Extract keywords from job descriptions

**Key methods**:

```python
class ATSKeywordsService:
    def extract_keywords(self, job_description: str) -> ATSKeywordsResponse
    def extract_and_analyze(
        self, 
        job_description: str, 
        resume_text: Optional[str] = None
    ) -> dict
```

**Features**:
- Supports both LLM-based and regex-based extraction
- Automatic fallback if LLM fails
- Deduplication and categorization
- Optional resume matching

**Dependency Injection**: Takes optional LLM client, can work without it

### 2. Data Schemas (`schemas/ats_keywords.py`)

```python
class ATSKeywordsRequest(BaseModel):
    job_description: str

class ATSKeywordsResponse(BaseModel):
    skills: list[str]
    technologies: list[str]
    tools: list[str]
    soft_skills: list[str]
```

### 3. Utility Functions (`utils/ats_keyword_utils.py`)

**Functions**:

- `extract_keywords_regex()` - Extract keywords using regex patterns
- `categorize_keywords_heuristic()` - Categorize keywords by type
- `remove_duplicates_preserve_order()` - Deduplicate while preserving order
- `get_most_common_keywords()` - Find most frequent keywords

### 4. LLM Prompts (`ai_prompts/ats_keywords_prompts.py`)

Two prompts provided:
- `EXTRACT_ATS_KEYWORDS_PROMPT` - Main extraction prompt
- `EXTRACT_ATS_KEYWORDS_FALLBACK_PROMPT` - Simple fallback prompt

### 5. API Router (`routers/keywords.py`)

**Endpoints**:

```
POST /api/v1/keywords/extract
POST /api/v1/keywords/extract-with-matching
GET  /api/v1/keywords/health
```

## Usage

### Basic Extraction

```python
from app.services.ats_keywords_service import ATSKeywordsService

# Create service
service = ATSKeywordsService(llm_client=None)

# Extract keywords
job_description = "Senior Java Developer with Spring Boot experience..."
keywords = service.extract_keywords(job_description)

# Access results
print(keywords.skills)        # ["Java", "System Design", ...]
print(keywords.technologies)  # ["Spring Boot", "Docker", ...]
print(keywords.tools)         # ["Git", "Jenkins", ...]
print(keywords.soft_skills)   # ["Leadership", "Communication", ...]
```

### With Resume Matching

```python
job_description = "Senior Java Developer with Spring Boot..."
resume_text = "I am a Java developer with 5 years experience..."

result = service.extract_and_analyze(job_description, resume_text)

# Returns
{
    "keywords": {
        "skills": [...],
        "technologies": [...],
        "tools": [...],
        "soft_skills": [...]
    },
    "total_keywords": 28,
    "matched": {
        "skills": ["Java"],
        "technologies": ["Spring Boot"],
        "tools": [],
        "soft_skills": []
    }
}
```

### API Usage

```bash
# Extract keywords
curl -X POST http://localhost:8000/api/v1/keywords/extract \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Senior Java Developer with Spring Boot experience..."
  }'

# Response
{
  "skills": ["Java", "Spring Boot", "System Design"],
  "technologies": ["Spring Boot", "Docker", "PostgreSQL"],
  "tools": ["Git", "Jenkins"],
  "soft_skills": ["Leadership", "Communication"]
}
```

## Extraction Methods

### Method 1: LLM-Based (When LangChain Client Available)

**Advantages**:
- More intelligent categorization
- Better understanding of context
- Can handle complex requirements

**Disadvantages**:
- Requires API calls
- Slower
- Cost associated

**Process**:
1. Format prompt with job description
2. Call LLM (OpenAI/Claude)
3. Parse JSON response
4. Validate and deduplicate

### Method 2: Regex-Based (Fallback)

**Advantages**:
- Fast and deterministic
- No external dependencies
- Works offline

**Disadvantages**:
- Less intelligent categorization
- Pattern-based heuristics
- May miss context-specific keywords

**Process**:
1. Extract candidates with regex
2. Find most common keywords
3. Categorize using heuristic patterns
4. Deduplicate and organize

## Testing

Comprehensive test suite included:

```bash
# Run all tests
python -m pytest tests/test_ats_keywords_service.py -v

# Run specific test
python -m pytest tests/test_ats_keywords_service.py::TestATSKeywordsService::test_extract_keywords_valid_input -v
```

**Test Coverage**:
- Utility function tests (regex, categorization, deduplication)
- Service unit tests (extraction, validation)
- Integration tests (full workflows)
- Real-world test cases (various job descriptions)

## Configuration

### Settings (core/config.py)

```python
# Already defined
minimum_keyword_count: int = 20  # Minimum keywords to extract
```

## Integration with Backend

The extracted keywords can be used by the backend for:

1. **ATS Score Calculation**: Compare resume keywords with job keywords
2. **Resume Optimization**: Suggest keywords to add
3. **Job Matching**: Find resumes matching job requirements
4. **Candidate Search**: Search candidates by extracted keywords

## Performance

- **Regex-based extraction**: ~10-50ms
- **LLM-based extraction**: ~1-5 seconds (depends on API)
- **Memory usage**: Minimal (~1-5MB)
- **Scalability**: Can process multiple concurrent requests

## Error Handling

The service includes robust error handling:

```python
# Invalid input
ValueError: "Job description must be at least 50 characters long"

# LLM failure (automatic fallback)
logger.warning(f"LLM extraction failed, falling back to regex: {error}")

# JSON parsing failure
ValueError: "Failed to parse LLM response"
```

## Future Enhancements

1. **Caching**: Cache job description analysis results
2. **Weighting**: Add importance weights to keywords
3. **Multi-language**: Support job descriptions in multiple languages
4. **Custom categories**: Allow user-defined keyword categories
5. **Trend analysis**: Track keyword trends over time
6. **Benchmark**: Compare with industry standards

## File Structure

```
ai-service/
├── app/
│   ├── services/
│   │   └── ats_keywords_service.py      ← Main service
│   ├── schemas/
│   │   └── ats_keywords.py              ← Data models
│   ├── routers/
│   │   └── keywords.py                  ← API endpoints
│   ├── utils/
│   │   └── ats_keyword_utils.py         ← Utility functions
│   └── ai_prompts/
│       └── ats_keywords_prompts.py      ← LLM prompts
├── tests/
│   └── test_ats_keywords_service.py     ← Test suite
└── ATS_KEYWORDS_SERVICE.md              ← This file
```

## Dependencies

```
fastapi              ← API framework
pydantic             ← Data validation
langchain (optional) ← LLM integration
openai (optional)    ← LLM provider
```

All dependencies already in `requirements.txt`

## References

- OpenAI Documentation: https://platform.openai.com/docs
- LangChain Documentation: https://python.langchain.com
- ATS Keyword Optimization: https://www.indeed.com/career-advice/resumes-cover-letters/how-ats-works

