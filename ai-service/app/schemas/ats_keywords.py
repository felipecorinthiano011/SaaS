"""Pydantic schemas for ATS keyword extraction."""

from pydantic import BaseModel, Field


class ATSKeywordsRequest(BaseModel):
    """Request model for ATS keyword extraction."""
    job_description: str = Field(..., min_length=50, description="Job description to extract keywords from")


class ATSKeywords(BaseModel):
    """Extracted ATS keywords organized by category."""
    skills: list[str] = Field(default_factory=list, description="Required technical and professional skills")
    technologies: list[str] = Field(default_factory=list, description="Technologies, frameworks, and platforms")
    tools: list[str] = Field(default_factory=list, description="Software tools and applications")
    soft_skills: list[str] = Field(default_factory=list, description="Soft skills and competencies")


class ATSKeywordsResponse(BaseModel):
    """Response model for ATS keyword extraction."""
    skills: list[str] = Field(description="Required technical and professional skills")
    technologies: list[str] = Field(description="Technologies, frameworks, and platforms")
    tools: list[str] = Field(description="Software tools and applications")
    soft_skills: list[str] = Field(description="Soft skills and competencies")

    class Config:
        json_schema_extra = {
            "example": {
                "skills": ["Java", "Python", "SQL", "RESTful API Design"],
                "technologies": ["Spring Boot", "Docker", "Kubernetes", "PostgreSQL"],
                "tools": ["Git", "Jenkins", "JIRA", "Docker Desktop"],
                "soft_skills": ["Leadership", "Communication", "Problem Solving", "Team Collaboration"]
            }
        }

