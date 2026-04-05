# AI Service (FastAPI)

## Purpose

Handles job/resume text analysis:

- ATS keyword extraction
- Resume vs job matching
- ATS score estimation
- Optimized resume draft generation

## Structure

- `app/api/` HTTP routes
- `app/services/` core analysis logic
- `app/schemas/` request/response contracts
- `app/core/` settings and infrastructure concerns

## Run locally

```powershell
cd ai-service
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Test

```powershell
cd ai-service
python -m pytest
```

