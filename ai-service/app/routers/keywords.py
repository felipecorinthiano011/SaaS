"""
Router for ATS Keywords Extraction API endpoints.

Endpoints:
- POST /api/v1/keywords/extract - Extract keywords from job description
"""

from fastapi import APIRouter, HTTPException, status
import logging

from app.schemas.ats_keywords import ATSKeywordsRequest, ATSKeywordsResponse
from app.services.ats_keywords_service import ATSKeywordsService

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/keywords",
    tags=["keywords"],
    responses={
        400: {"description": "Invalid input"},
        500: {"description": "Internal server error"},
    }
)

# Initialize service (no LLM client for now - will be added later)
ats_keywords_service = ATSKeywordsService(llm_client=None)


@router.post(
    "/extract",
    response_model=ATSKeywordsResponse,
    status_code=status.HTTP_200_OK,
    summary="Extract ATS Keywords",
    description="Extract ATS keywords from a job description. Returns keywords organized by category."
)
async def extract_keywords(request: ATSKeywordsRequest) -> ATSKeywordsResponse:
    """
    Extract ATS keywords from a job description.

    This endpoint analyzes a job description and extracts keywords that an
    Applicant Tracking System (ATS) would look for. Keywords are categorized into:
    - **skills**: Technical and professional skills
    - **technologies**: Frameworks, platforms, databases
    - **tools**: Software tools and applications
    - **soft_skills**: Soft skills and competencies

    Args:
        request: ATSKeywordsRequest with job_description

    Returns:
        ATSKeywordsResponse with categorized keywords

    Raises:
        HTTPException: If input is invalid or processing fails
    """
    try:
        logger.info(f"Extracting keywords from job description (length: {len(request.job_description)})")

        # Extract keywords
        keywords = ats_keywords_service.extract_keywords(request.job_description)

        logger.info(f"Successfully extracted keywords: {len(keywords.skills)} skills, "
                   f"{len(keywords.technologies)} technologies, "
                   f"{len(keywords.tools)} tools, "
                   f"{len(keywords.soft_skills)} soft skills")

        return keywords

    except ValueError as e:
        logger.warning(f"Invalid input: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error extracting keywords: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error extracting keywords from job description"
        )


@router.post(
    "/extract-with-matching",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Extract Keywords and Match with Resume",
    description="Extract keywords and optionally match them against a resume text."
)
async def extract_and_match(
    job_description: str,
    resume_text: str = None
) -> dict:
    """
    Extract keywords and optionally match against resume.

    Args:
        job_description: Job description text
        resume_text: Optional resume text for keyword matching

    Returns:
        Dictionary with extracted keywords and optional matching results

    Raises:
        HTTPException: If input is invalid
    """
    try:
        if not job_description or len(job_description.strip()) < 50:
            raise ValueError("Job description must be at least 50 characters")

        logger.info("Extracting keywords with optional resume matching")

        result = ats_keywords_service.extract_and_analyze(
            job_description,
            resume_text
        )

        return result

    except ValueError as e:
        logger.warning(f"Invalid input: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in extraction with matching: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing keywords"
        )


# Health check endpoint for this router
@router.get(
    "/health",
    response_model=dict,
    summary="Health Check",
    description="Check if keywords service is operational"
)
async def health_check() -> dict:
    """Check service health."""
    return {
        "status": "healthy",
        "service": "ats_keywords",
        "version": "1.0.0"
    }

