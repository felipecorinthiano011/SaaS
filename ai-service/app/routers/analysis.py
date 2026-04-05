"""Analysis router with LangChain-powered endpoints."""

import logging
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.services.resume_analysis_service import ResumeAnalysisService
from app.utils.file_parser import extract_resume_text

router = APIRouter(prefix="/api/v1", tags=["analysis"])
logger = logging.getLogger(__name__)


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze job description and resume using LangChain and OpenAI.

    Returns comprehensive analysis with:
    - ATS score
    - Extracted keywords
    - Matched/missing keywords
    - Optimized resume
    - Suggestions for improvement
    """
    try:
        service = ResumeAnalysisService()
        result = service.analyze_resume(
            job_description=payload.jobDescription,
            resume_text=payload.resumeText,
        )

        # Convert snake_case to camelCase for response
        return AnalyzeResponse(
            atsScore=result.get("ats_score", 0),
            extractedKeywords=result.get("extracted_keywords", {}),
            matchedKeywords=result.get("matched_keywords", []),
            missingKeywords=result.get("missing_keywords", []),
            optimizedResume=result.get("optimized_resume", ""),
            suggestions=result.get("suggestions", []),
            gapSummary=result.get("gap_summary", ""),
        )

    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Analysis failed: {str(e)}"
        )


@router.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    """
    Extract plain text from an uploaded PDF or DOCX resume file.

    Returns:
        JSON with `text` (extracted text) and `filename` fields.
    """
    try:
        logger.info(f"Received file: {file.filename}, content-type: {file.content_type}, size: {file.size}")

        text = extract_resume_text(file)

        if not text or not text.strip():
            logger.warning(f"Warning: No text extracted from {file.filename}")
            return {"text": "", "filename": file.filename}

        logger.info(f"Successfully extracted {len(text)} characters from {file.filename}")
        return {"text": text, "filename": file.filename}
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Text extraction failed for {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Text extraction failed: {str(e)}")


