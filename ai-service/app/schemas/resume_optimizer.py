"""Pydantic schemas for ATS resume optimization."""

from pydantic import BaseModel, Field


class OptimizeResumeRequest(BaseModel):
    """Request model for resume optimization."""
    job_description: str = Field(..., min_length=50, description="Job description to match against")
    resume_text: str = Field(..., min_length=50, description="Original resume text")


class Suggestion(BaseModel):
    """Optimization suggestion."""
    category: str = Field(description="Category: Skills, Formatting, Keywords, Content, etc.")
    suggestion: str = Field(description="Specific actionable suggestion")
    priority: str = Field(description="Priority: high, medium, low")
    rationale: str = Field(description="Why this suggestion improves ATS match")


class OptimizeResumeResponse(BaseModel):
    """Response model for resume optimization."""
    ats_score: int = Field(description="ATS match score (0-100)")
    missing_keywords: list[str] = Field(description="Keywords from job not found in resume")
    optimized_resume: str = Field(description="ATS-optimized resume text")
    suggestions: list[Suggestion] = Field(description="Improvement suggestions prioritized by impact")

    class Config:
        json_schema_extra = {
            "example": {
                "ats_score": 78,
                "missing_keywords": ["Kubernetes", "Docker", "CI/CD"],
                "optimized_resume": "JOHN DOE\n\nSenior Software Engineer\n\nProfessional Summary\n...",
                "suggestions": [
                    {
                        "category": "Skills",
                        "suggestion": "Add Docker and Kubernetes experience to skills section",
                        "priority": "high",
                        "rationale": "These are core requirements in the job description and currently missing"
                    }
                ]
            }
        }

