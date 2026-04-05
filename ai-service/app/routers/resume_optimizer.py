"""
Router for Resume Optimizer API endpoints.

Endpoints:
- POST /api/v1/resume/optimize - Optimize resume for job description
"""

from fastapi import APIRouter, HTTPException, status
import logging

from app.schemas.resume_optimizer import OptimizeResumeRequest, OptimizeResumeResponse
from app.services.resume_optimizer_service import ResumeOptimizerService

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/resume",
    tags=["resume"],
    responses={
        400: {"description": "Invalid input"},
        500: {"description": "Internal server error"},
    }
)

# Initialize service
resume_optimizer_service = ResumeOptimizerService(llm_client=None)


@router.post(
    "/optimize",
    response_model=OptimizeResumeResponse,
    status_code=status.HTTP_200_OK,
    summary="Optimize Resume",
    description="Optimize a resume to better match a job description using ATS best practices."
)
async def optimize_resume(request: OptimizeResumeRequest) -> OptimizeResumeResponse:
    """
    Optimize a resume to match a job description.

    This endpoint analyzes a job description and resume, then provides:
    - An optimized version of the resume
    - An ATS match score (0-100)
    - Missing keywords from the job description
    - Specific improvement suggestions

    Optimization Rules:
    - No invented experience
    - Only rephrasing of existing information
    - Strong action verbs
    - Relevant keyword integration
    - ATS-friendly formatting

    Args:
        request: OptimizeResumeRequest with job_description and resume_text

    Returns:
        OptimizeResumeResponse with optimized resume and suggestions

    Raises:
        HTTPException: If input is invalid or processing fails
    """
    try:
        logger.info(
            f"Optimizing resume for job description "
            f"(job_len={len(request.job_description)}, "
            f"resume_len={len(request.resume_text)})"
        )

        # Optimize resume
        result = resume_optimizer_service.optimize_resume(
            request.job_description,
            request.resume_text
        )

        logger.info(
            f"Successfully optimized resume. "
            f"ATS Score: {result.ats_score}, "
            f"Missing keywords: {len(result.missing_keywords)}, "
            f"Suggestions: {len(result.suggestions)}"
        )

        return result

    except ValueError as e:
        logger.warning(f"Invalid input: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error optimizing resume: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error optimizing resume. Please try again."
        )


@router.post(
    "/compare",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Compare Resumes",
    description="Compare original and optimized resumes to show improvements."
)
async def compare_resumes(
    original_resume: str,
    optimized_resume: str
) -> dict:
    """
    Compare original and optimized resumes.

    Shows metrics like:
    - Strong verbs added
    - Metrics/numbers added
    - Length changes
    - Formatting improvements

    Args:
        original_resume: Original resume text
        optimized_resume: Optimized resume text

    Returns:
        Comparison metrics
    """
    try:
        if not original_resume or len(original_resume.strip()) < 50:
            raise ValueError("Original resume must be at least 50 characters")
        if not optimized_resume or len(optimized_resume.strip()) < 50:
            raise ValueError("Optimized resume must be at least 50 characters")

        comparison = resume_optimizer_service.compare_resumes(
            original_resume,
            optimized_resume
        )

        return {
            "comparison": comparison,
            "message": "Comparison completed successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error comparing resumes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error comparing resumes"
        )


@router.get(
    "/health",
    response_model=dict,
    summary="Health Check",
    description="Check if resume optimizer service is operational"
)
async def health_check() -> dict:
    """Check service health."""
    return {
        "status": "healthy",
        "service": "resume_optimizer",
        "version": "1.0.0"
    }

