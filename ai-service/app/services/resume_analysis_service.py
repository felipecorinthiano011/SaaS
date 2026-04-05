"""Advanced resume analysis service using LangChain and OpenAI."""

import logging
from typing import Optional

from app.core.config import settings
from app.utils.file_parser import extract_json_from_text, clean_text
from app.utils.ats_calculator import calculate_keyword_match, calculate_ats_score

logger = logging.getLogger(__name__)

# Common technical keywords to extract for mock mode
_TECH_KEYWORDS = [
    "python", "java", "javascript", "typescript", "react", "angular", "vue",
    "spring", "spring boot", "django", "fastapi", "node.js", "docker", "kubernetes",
    "aws", "azure", "gcp", "postgresql", "mysql", "mongodb", "redis", "kafka",
    "microservices", "rest api", "graphql", "ci/cd", "git", "linux", "agile",
    "scrum", "machine learning", "sql", "html", "css", "terraform", "jenkins",
]

_SOFT_SKILLS = [
    "communication", "teamwork", "leadership", "problem solving", "critical thinking",
    "adaptability", "time management", "collaboration", "mentoring",
]


def _extract_words(text: str) -> set:
    """Return lowercased keywords/phrases present in text."""
    text_lower = text.lower()
    found = set()
    for kw in _TECH_KEYWORDS + _SOFT_SKILLS:
        if kw in text_lower:
            found.add(kw)
    return found


def _mock_analyze(job_description: str, resume_text: str) -> dict:
    """Return a deterministic mock analysis when no OpenAI key is set."""
    jd_words = _extract_words(job_description)
    resume_words = _extract_words(resume_text)

    matched = list(jd_words & resume_words)
    missing = list(jd_words - resume_words)

    tech_kw = [k for k in jd_words if k in _TECH_KEYWORDS]
    soft_kw = [k for k in jd_words if k in _SOFT_SKILLS]

    total = len(jd_words) or 1
    ats_score = min(100, int((len(matched) / total) * 100))

    optimized = (
        resume_text.strip()
        + "\n\n[Mock optimization — set OPENAI_API_KEY for real AI-powered optimization]"
        + (f"\n\nConsider adding these missing keywords: {', '.join(missing[:10])}" if missing else "")
    )

    suggestions = [
        {
            "category": "Keywords",
            "suggestion": f"Add missing keywords to your resume: {', '.join(missing[:5]) or 'none identified'}",
            "priority": "high",
            "impact": "Improves ATS score by including required terms from the job description.",
        },
        {
            "category": "Configuration",
            "suggestion": "Set OPENAI_API_KEY environment variable for real AI-powered analysis.",
            "priority": "medium",
            "impact": "Enables full LLM-based resume optimization and detailed suggestions.",
        },
    ]

    return {
        "ats_score": ats_score,
        "extracted_keywords": {
            "technical_keywords": tech_kw,
            "soft_skills": soft_kw,
            "certifications": [],
            "required_experience": [],
        },
        "matched_keywords": matched,
        "missing_keywords": missing,
        "optimized_resume": optimized,
        "suggestions": suggestions,
        "gap_summary": (
            f"Mock analysis: {len(matched)} of {len(jd_words)} job keywords found in resume. "
            "Provide OPENAI_API_KEY for a detailed gap analysis."
        ),
    }


class ResumeAnalysisService:
    """Service for advanced resume analysis using LangChain and OpenAI."""

    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize — falls back to mock mode when no API key is available."""
        key = openai_api_key or settings.openai_api_key
        self._mock_mode = not bool(key)
        self.llm = None
        if not self._mock_mode:
            try:
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    model=settings.llm_name,
                    api_key=key,
                    temperature=0.3,
                )
            except Exception as e:
                logger.error(f"Failed to init ChatOpenAI: {e}")
                self._mock_mode = True
        else:
            logger.warning(
                "No OPENAI_API_KEY found — running in mock mode. "
                "Set AI_OPENAI_API_KEY to enable real AI analysis."
            )

    def analyze_resume(self, job_description: str, resume_text: str) -> dict:
        """
        Perform comprehensive resume analysis.

        Returns:
        {
            "ats_score": int (0-100),
            "extracted_keywords": {"technical_keywords": [...], "soft_skills": [...], ...},
            "matched_keywords": [...],
            "missing_keywords": [...],
            "optimized_resume": str,
            "suggestions": [{"category": str, "suggestion": str, "priority": str, "impact": str}],
            "gap_summary": str
        }
        """
        if self._mock_mode:
            return _mock_analyze(job_description, resume_text)

        try:
            from langchain.prompts import PromptTemplate
            from langchain.chains import LLMChain
            from app.ai_prompts.analysis_prompts import (
                EXTRACT_KEYWORDS_PROMPT,
                ANALYZE_RESUME_PROMPT,
                OPTIMIZE_RESUME_PROMPT,
                GENERATE_SUGGESTIONS_PROMPT,
            )

            # Step 1: Extract keywords from job description
            keywords_data = self._extract_keywords(job_description)

            # Step 2: Analyze resume against keywords
            analysis_data = self._analyze_resume(
                job_description, resume_text, keywords_data
            )

            # Step 3: Calculate ATS score
            matched_count = len(analysis_data.get("matched_keywords", []))
            total_keywords = sum(
                len(keywords_data.get(key, []))
                for key in ["technical_keywords", "soft_skills", "certifications", "required_experience"]
            )
            ats_score = self._calculate_ats_score(matched_count, total_keywords)

            # Step 4: Generate optimized resume
            optimized_resume = self._optimize_resume(
                resume_text,
                analysis_data.get("missing_keywords", []),
                job_description,
            )

            # Step 5: Generate suggestions
            suggestions = self._generate_suggestions(
                ats_score,
                analysis_data.get("missing_keywords", []),
                analysis_data.get("gaps_analysis", ""),
            )

            return {
                "ats_score": ats_score,
                "extracted_keywords": keywords_data,
                "matched_keywords": analysis_data.get("matched_keywords", []),
                "missing_keywords": analysis_data.get("missing_keywords", []),
                "optimized_resume": optimized_resume,
                "suggestions": suggestions,
                "gap_summary": analysis_data.get("gaps_analysis", ""),
            }

        except Exception as e:
            logger.error(f"Resume analysis failed: {str(e)}")
            raise

    def _extract_keywords(self, job_description: str) -> dict:
        """Extract keywords from job description using LLM."""
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        from app.ai_prompts.analysis_prompts import EXTRACT_KEYWORDS_PROMPT

        prompt = PromptTemplate(
            input_variables=["job_description"],
            template=EXTRACT_KEYWORDS_PROMPT,
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(job_description=clean_text(job_description))

        try:
            return extract_json_from_text(response)
        except Exception as e:
            logger.warning(f"Failed to parse keywords response: {e}")
            return {
                "technical_keywords": [],
                "soft_skills": [],
                "certifications": [],
                "required_experience": [],
            }

    def _analyze_resume(
        self, job_description: str, resume_text: str, keywords_data: dict
    ) -> dict:
        """Analyze resume against keywords and job description."""
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        from app.ai_prompts.analysis_prompts import ANALYZE_RESUME_PROMPT

        prompt = PromptTemplate(
            input_variables=[
                "job_description",
                "resume_text",
                "technical_keywords",
                "soft_skills",
                "certifications",
                "required_experience",
            ],
            template=ANALYZE_RESUME_PROMPT,
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(
            job_description=clean_text(job_description),
            resume_text=clean_text(resume_text),
            technical_keywords=", ".join(keywords_data.get("technical_keywords", [])[:15]),
            soft_skills=", ".join(keywords_data.get("soft_skills", [])[:10]),
            certifications=", ".join(keywords_data.get("certifications", [])[:10]),
            required_experience=", ".join(keywords_data.get("required_experience", [])[:10]),
        )

        try:
            return extract_json_from_text(response)
        except Exception as e:
            logger.warning(f"Failed to parse analysis response: {e}")
            return {
                "matched_keywords": [],
                "missing_keywords": [],
                "ats_match_percentage": 0,
                "strengths": [],
                "weaknesses": [],
                "gaps_analysis": "Analysis could not be completed.",
            }

    def _optimize_resume(
        self, resume_text: str, missing_keywords: list, job_description: str
    ) -> str:
        """Generate an optimized version of the resume."""
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        from app.ai_prompts.analysis_prompts import OPTIMIZE_RESUME_PROMPT

        prompt = PromptTemplate(
            input_variables=["resume_text", "missing_keywords", "job_description"],
            template=OPTIMIZE_RESUME_PROMPT,
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(
            resume_text=clean_text(resume_text),
            missing_keywords=", ".join(missing_keywords[:10]),
            job_description=clean_text(job_description),
        )
        return clean_text(response)

    def _generate_suggestions(
        self, ats_score: int, missing_keywords: list, gaps_analysis: str
    ) -> list:
        """Generate actionable suggestions for resume improvement."""
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        from app.ai_prompts.analysis_prompts import GENERATE_SUGGESTIONS_PROMPT

        prompt = PromptTemplate(
            input_variables=["ats_match_percentage", "missing_keywords", "gaps_analysis"],
            template=GENERATE_SUGGESTIONS_PROMPT,
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(
            ats_match_percentage=ats_score,
            missing_keywords=", ".join(missing_keywords[:10]),
            gaps_analysis=gaps_analysis[:500],
        )

        try:
            data = extract_json_from_text(response)
            return data.get("suggestions", [])
        except Exception as e:
            logger.warning(f"Failed to parse suggestions: {e}")
            return []

    def _calculate_ats_score(self, matched_count: int, total_keywords: int) -> int:
        """Calculate ATS score based on keyword matching."""
        return calculate_ats_score(matched_count, total_keywords)
