"""Analysis router with LangChain-powered endpoints."""

import logging
from fastapi import APIRouter, HTTPException

from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.services.resume_analysis_service import ResumeAnalysisService

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

