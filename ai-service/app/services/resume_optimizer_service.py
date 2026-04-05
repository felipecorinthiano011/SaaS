"""
ATS Resume Optimizer Service

This service optimizes resumes to better match job descriptions while:
- Maintaining truthfulness (no invented experience)
- Using strong action verbs
- Integrating relevant keywords
- Improving ATS compatibility
- Following clean architecture principles
"""

import json
import logging
from typing import Optional

from app.ai_prompts.resume_optimizer_prompts import (
    OPTIMIZE_RESUME_PROMPT,
    OPTIMIZE_RESUME_FALLBACK_PROMPT,
)
from app.core.config import settings
from app.schemas.resume_optimizer import OptimizeResumeResponse, Suggestion
from app.services.ats_keywords_service import ATSKeywordsService
from app.utils.file_parser import extract_json_from_text
from app.utils.resume_optimizer_utils import (
    ats_friendly_formatting,
    calculate_ats_score,
    find_missing_keywords,
    generate_suggestions,
    improve_action_verbs,
    match_resume_to_job,
)

logger = logging.getLogger(__name__)


class ResumeOptimizerService:
    """Service for optimizing resumes to match job descriptions."""

    def __init__(self, llm_client=None):
        """
        Initialize the Resume Optimizer Service.

        Args:
            llm_client: Optional LLM client (from LangChain/OpenAI)
        """
        self.llm_client = llm_client
        self.use_llm = llm_client is not None
        self.ats_keywords_service = ATSKeywordsService(llm_client=None)

    def optimize_resume(
        self,
        job_description: str,
        resume_text: str
    ) -> OptimizeResumeResponse:
        """
        Optimize a resume to match a job description.

        Process:
        1. Extract keywords from job description
        2. Calculate initial ATS score
        3. Generate optimized resume
        4. Identify missing keywords
        5. Create improvement suggestions

        Args:
            job_description: The job description
            resume_text: The original resume text

        Returns:
            OptimizeResumeResponse with optimization results

        Raises:
            ValueError: If inputs are invalid
        """
        # Validate inputs
        if not job_description or len(job_description.strip()) < 50:
            raise ValueError("Job description must be at least 50 characters")
        if not resume_text or len(resume_text.strip()) < 50:
            raise ValueError("Resume must be at least 50 characters")

        logger.info("Optimizing resume for job description")

        try:
            # Extract keywords from job description
            logger.debug("Extracting keywords from job description")
            keywords_response = self.ats_keywords_service.extract_keywords(job_description)

            # Combine all keywords
            all_keywords = (
                keywords_response.skills +
                keywords_response.technologies +
                keywords_response.tools +
                keywords_response.soft_skills
            )

            # Calculate initial ATS score
            initial_ats_score = calculate_ats_score(resume_text, all_keywords)
            logger.debug(f"Initial ATS score: {initial_ats_score}")

            # Try LLM optimization first
            if self.use_llm and self.llm_client:
                logger.info("Using LLM for resume optimization")
                try:
                    optimized = self._optimize_with_llm(
                        job_description,
                        resume_text,
                        all_keywords
                    )
                    return optimized
                except Exception as e:
                    logger.warning(f"LLM optimization failed, using fallback: {e}")

            # Fallback to rule-based optimization
            logger.info("Using rule-based optimization")
            return self._optimize_with_rules(
                job_description,
                resume_text,
                all_keywords
            )

        except Exception as e:
            logger.error(f"Error optimizing resume: {e}", exc_info=True)
            raise

    def _optimize_with_llm(
        self,
        job_description: str,
        resume_text: str,
        job_keywords: list[str]
    ) -> OptimizeResumeResponse:
        """
        Optimize resume using LLM.

        Args:
            job_description: Job description
            resume_text: Original resume
            job_keywords: Extracted keywords

        Returns:
            Optimized resume response
        """
        # Prepare prompt
        prompt = OPTIMIZE_RESUME_PROMPT.format(
            job_description=job_description,
            resume_text=resume_text
        )

        # Call LLM
        response = self.llm_client.invoke(prompt)
        response_text = response.content if hasattr(response, 'content') else str(response)

        try:
            # Parse response
            result_data = extract_json_from_text(response_text)
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}")
            # Fall back to rules
            return self._optimize_with_rules(
                job_description,
                resume_text,
                job_keywords
            )

        # Validate response
        return self._process_llm_response(result_data)

    def _optimize_with_rules(
        self,
        job_description: str,
        resume_text: str,
        job_keywords: list[str]
    ) -> OptimizeResumeResponse:
        """
        Optimize resume using rule-based approach.

        Process:
        1. Improve action verbs
        2. Reorder sections by relevance
        3. Format for ATS
        4. Calculate score
        5. Generate suggestions

        Args:
            job_description: Job description
            resume_text: Original resume
            job_keywords: Extracted keywords

        Returns:
            Optimized resume response
        """
        logger.debug("Applying rule-based optimizations")

        # Step 1: Improve action verbs
        improved = improve_action_verbs(resume_text)

        # Step 2: Reorder sections by relevance
        reordered = match_resume_to_job(improved, job_keywords)

        # Step 3: Format for ATS
        optimized_resume = ats_friendly_formatting(reordered)

        # Step 4: Calculate ATS score
        ats_score = calculate_ats_score(optimized_resume, job_keywords)

        # Step 5: Find missing keywords
        missing = find_missing_keywords(optimized_resume, job_keywords)

        # Step 6: Generate suggestions
        raw_suggestions = generate_suggestions(
            optimized_resume,
            job_keywords,
            ats_score
        )

        # Convert to Suggestion objects
        suggestions = [
            Suggestion(**s) for s in raw_suggestions
        ]

        return OptimizeResumeResponse(
            ats_score=ats_score,
            missing_keywords=missing,
            optimized_resume=optimized_resume,
            suggestions=suggestions
        )

    def _process_llm_response(self, response_data: dict) -> OptimizeResumeResponse:
        """
        Process and validate LLM response.

        Args:
            response_data: Dictionary from LLM

        Returns:
            Validated OptimizeResumeResponse
        """
        # Extract fields with defaults
        ats_score = response_data.get("ats_score", 50)
        missing_keywords = response_data.get("missing_keywords", [])
        optimized_resume = response_data.get("optimized_resume", "")
        suggestions_data = response_data.get("suggestions", [])

        # Validate types
        if not isinstance(ats_score, int):
            ats_score = int(ats_score) if ats_score else 50
        ats_score = max(0, min(100, ats_score))

        if not isinstance(missing_keywords, list):
            missing_keywords = [missing_keywords] if missing_keywords else []

        # Convert suggestion dicts to Suggestion objects
        suggestions = []
        for s in suggestions_data:
            if isinstance(s, dict):
                suggestions.append(Suggestion(**s))

        return OptimizeResumeResponse(
            ats_score=ats_score,
            missing_keywords=missing_keywords,
            optimized_resume=optimized_resume,
            suggestions=suggestions
        )

    def compare_resumes(
        self,
        original_resume: str,
        optimized_resume: str
    ) -> dict:
        """
        Compare original and optimized resumes.

        Args:
            original_resume: Original resume text
            optimized_resume: Optimized resume text

        Returns:
            Dictionary with comparison metrics
        """
        import re

        original_lower = original_resume.lower()
        optimized_lower = optimized_resume.lower()

        # Count verbs
        strong_verbs = [
            'engineered', 'spearheaded', 'optimized', 'facilitated',
            'orchestrated', 'pioneered', 'leveraged', 'transformed'
        ]

        original_strong = sum(
            original_lower.count(verb) for verb in strong_verbs
        )
        optimized_strong = sum(
            optimized_lower.count(verb) for verb in strong_verbs
        )

        # Count metrics
        original_metrics = len(re.findall(r'\d+(%|\$|K|M)', original_resume))
        optimized_metrics = len(re.findall(r'\d+(%|\$|K|M)', optimized_resume))

        return {
            "strong_verbs_improved": optimized_strong - original_strong,
            "metrics_added": optimized_metrics - original_metrics,
            "length_change": len(optimized_resume) - len(original_resume),
            "formatting_improved": not ('<' in original_resume or '>' in original_resume) or
                                  ('<' not in optimized_resume and '>' not in optimized_resume)
        }

