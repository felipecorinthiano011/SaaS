"""Utility functions for ATS analysis."""

from typing import List


def calculate_keyword_match(resume_text: str, keywords: List[str]) -> tuple[List[str], List[str]]:
    """
    Calculate which keywords are present in resume.

    Returns: (matched_keywords, missing_keywords)
    """
    resume_lower = resume_text.lower()
    matched = []
    missing = []

    for keyword in keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in resume_lower:
            matched.append(keyword)
        else:
            missing.append(keyword)

    return matched, missing


def calculate_ats_score(
    matched_count: int,
    total_keywords: int,
    keyword_match_percent: float = 0.4,
    formatting_score: float = 20,
    content_score: float = 40
) -> int:
    """
    Calculate ATS score (0-100).

    Components:
    - Keyword matching: 40%
    - Formatting/Structure: 20%
    - Content quality: 40%
    """
    if total_keywords == 0:
        return 0

    keyword_score = (matched_count / total_keywords) * keyword_match_percent
    base_score = int((keyword_score + formatting_score + content_score) * 100)

    return min(100, max(0, base_score))


def format_keywords_for_prompt(keywords: List[str]) -> str:
    """Format keyword list for prompt insertion."""
    if not keywords:
        return "None"
    return ", ".join(keywords[:20])  # Limit to 20 keywords per category

