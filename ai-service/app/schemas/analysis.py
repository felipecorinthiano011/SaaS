from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    jobDescription: str = Field(..., min_length=20)
    resumeText: str = Field(..., min_length=20)


class KeywordsData(BaseModel):
    technical_keywords: list[str] = Field(default_factory=list)
    soft_skills: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    required_experience: list[str] = Field(default_factory=list)


class Suggestion(BaseModel):
    category: str
    suggestion: str
    priority: str
    impact: str


class AnalyzeResponse(BaseModel):
    atsScore: int
    extractedKeywords: KeywordsData
    matchedKeywords: list[str]
    missingKeywords: list[str]
    optimizedResume: str
    suggestions: list[Suggestion]
    gapSummary: str

