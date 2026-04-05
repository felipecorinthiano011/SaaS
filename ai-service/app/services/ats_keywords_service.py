"""
ATS Keywords Extraction Service

This service extracts ATS (Applicant Tracking System) keywords from job descriptions.
It categorizes keywords into: skills, technologies, tools, and soft skills.

Following clean architecture principles:
- Single Responsibility: Focuses only on keyword extraction
- Dependency Injection: Takes LLM client as dependency
- Testable: Can be tested with mock LLM responses
- Reusable: Can be used independently from other services
"""

import json
import logging
from typing import Optional

from app.ai_prompts.ats_keywords_prompts import (
    EXTRACT_ATS_KEYWORDS_PROMPT,
    EXTRACT_ATS_KEYWORDS_FALLBACK_PROMPT,
)
from app.core.config import settings
from app.schemas.ats_keywords import ATSKeywords, ATSKeywordsResponse
from app.utils.ats_keyword_utils import (
    categorize_keywords_heuristic,
    extract_keywords_regex,
    get_most_common_keywords,
    remove_duplicates_preserve_order,
)
from app.utils.file_parser import extract_json_from_text

logger = logging.getLogger(__name__)


class ATSKeywordsService:
    """Service for extracting ATS keywords from job descriptions."""

    def __init__(self, llm_client=None):
        """
        Initialize the ATS Keywords Service.

        Args:
            llm_client: Optional LLM client (from LangChain/OpenAI)
                       If not provided, will use fallback regex-based extraction
        """
        self.llm_client = llm_client
        self.use_llm = llm_client is not None

    def extract_keywords(self, job_description: str) -> ATSKeywordsResponse:
        """
        Extract ATS keywords from a job description.

        This is the main public method that:
        1. Attempts LLM-based extraction (if available)
        2. Falls back to regex-based extraction
        3. Combines both approaches for better results
        4. Deduplicates and organizes results

        Args:
            job_description: The job description text to analyze

        Returns:
            ATSKeywordsResponse with categorized keywords

        Raises:
            ValueError: If job_description is too short or invalid
        """
        # Validate input
        if not job_description or len(job_description.strip()) < 50:
            raise ValueError("Job description must be at least 50 characters long")

        try:
            if self.use_llm and self.llm_client:
                # Try LLM-based extraction first
                logger.info("Extracting keywords using LLM...")
                return self._extract_with_llm(job_description)
            else:
                # Fall back to regex-based extraction
                logger.info("Extracting keywords using regex fallback...")
                return self._extract_with_regex(job_description)
        except Exception as e:
            logger.warning(f"LLM extraction failed, falling back to regex: {str(e)}")
            # Always fall back to regex if LLM fails
            return self._extract_with_regex(job_description)

    def _extract_with_llm(self, job_description: str) -> ATSKeywordsResponse:
        """
        Extract keywords using LLM (LangChain + OpenAI).

        Args:
            job_description: Job description to analyze

        Returns:
            ATSKeywordsResponse with LLM-extracted keywords

        Raises:
            Exception: If LLM call fails
        """
        # Prepare prompt
        prompt = EXTRACT_ATS_KEYWORDS_PROMPT.format(
            job_description=job_description
        )

        # Call LLM
        response = self.llm_client.invoke(prompt)

        # Parse response
        response_text = response.content if hasattr(response, 'content') else str(response)

        try:
            keywords_data = extract_json_from_text(response_text)
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {str(e)}")
            # If JSON parsing fails, try fallback
            return self._extract_with_regex(job_description)

        # Validate and clean response
        return self._process_llm_response(keywords_data)

    def _extract_with_regex(self, job_description: str) -> ATSKeywordsResponse:
        """
        Extract keywords using regex patterns (fallback method).

        This method:
        1. Extracts candidate keywords using regex
        2. Gets most common keywords
        3. Categorizes using heuristic patterns
        4. Deduplicates and organizes results

        Args:
            job_description: Job description to analyze

        Returns:
            ATSKeywordsResponse with regex-extracted keywords
        """
        logger.debug("Using regex-based keyword extraction")

        # Extract candidate keywords
        candidate_keywords = extract_keywords_regex(job_description)

        # Get most common keywords
        most_common = get_most_common_keywords(job_description, count=30)

        # Combine and deduplicate
        all_keywords = remove_duplicates_preserve_order(candidate_keywords + most_common)

        # Categorize keywords
        categorized = categorize_keywords_heuristic(all_keywords, job_description)

        # Ensure reasonable number of keywords in each category
        return ATSKeywordsResponse(
            skills=categorized["skills"][:8],
            technologies=categorized["technologies"][:8],
            tools=categorized["tools"][:6],
            soft_skills=categorized["soft_skills"][:6],
        )

    def _process_llm_response(self, keywords_data: dict) -> ATSKeywordsResponse:
        """
        Process and validate LLM response.

        Args:
            keywords_data: Dictionary with keywords from LLM

        Returns:
            Validated ATSKeywordsResponse
        """
        # Ensure keys exist
        skills = keywords_data.get("skills", [])
        technologies = keywords_data.get("technologies", [])
        tools = keywords_data.get("tools", [])
        soft_skills = keywords_data.get("soft_skills", [])

        # Validate types
        if not isinstance(skills, list):
            skills = [skills] if skills else []
        if not isinstance(technologies, list):
            technologies = [technologies] if technologies else []
        if not isinstance(tools, list):
            tools = [tools] if tools else []
        if not isinstance(soft_skills, list):
            soft_skills = [soft_skills] if soft_skills else []

        # Deduplicate
        skills = remove_duplicates_preserve_order(skills)
        technologies = remove_duplicates_preserve_order(technologies)
        tools = remove_duplicates_preserve_order(tools)
        soft_skills = remove_duplicates_preserve_order(soft_skills)

        return ATSKeywordsResponse(
            skills=skills,
            technologies=technologies,
            tools=tools,
            soft_skills=soft_skills,
        )

    def extract_and_analyze(
        self,
        job_description: str,
        resume_text: Optional[str] = None
    ) -> dict:
        """
        Extract keywords and optionally analyze against resume.

        Args:
            job_description: Job description to analyze
            resume_text: Optional resume text for comparison

        Returns:
            Dictionary with keywords and optional matching information
        """
        keywords = self.extract_keywords(job_description)

        result = {
            "keywords": keywords.dict(),
            "total_keywords": (
                len(keywords.skills) +
                len(keywords.technologies) +
                len(keywords.tools) +
                len(keywords.soft_skills)
            )
        }

        # If resume provided, do matching
        if resume_text:
            result["matched"] = self._find_matching_keywords(keywords, resume_text)

        return result

    def _find_matching_keywords(self, keywords: ATSKeywordsResponse, resume_text: str) -> dict:
        """
        Find which keywords are present in resume.

        Args:
            keywords: Extracted keywords
            resume_text: Resume text to search in

        Returns:
            Dictionary with matched keywords by category
        """
        resume_lower = resume_text.lower()

        return {
            "skills": [kw for kw in keywords.skills if kw.lower() in resume_lower],
            "technologies": [kw for kw in keywords.technologies if kw.lower() in resume_lower],
            "tools": [kw for kw in keywords.tools if kw.lower() in resume_lower],
            "soft_skills": [kw for kw in keywords.soft_skills if kw.lower() in resume_lower],
        }

