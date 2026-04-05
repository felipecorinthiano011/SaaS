from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    jobDescription: str = Field(..., min_length=20)
    resumeText: str = Field(..., min_length=20)


class AnalyzeResponse(BaseModel):
    atsScore: int
    extractedKeywords: list[str]
    optimizedResume: str
    gapSummary: str

