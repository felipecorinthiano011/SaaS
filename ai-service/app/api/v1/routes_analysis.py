from fastapi import APIRouter

from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.services.analysis_service import AnalysisService

router = APIRouter()
analysis_service = AnalysisService()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    result = analysis_service.analyze(
        job_description=payload.jobDescription, resume_text=payload.resumeText
    )
    return AnalyzeResponse(**result)
