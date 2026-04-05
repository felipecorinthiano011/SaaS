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


def calculate_ats_score(matched_count: int, total_keywords: int) -> int:
    """
    Calculate ATS score (0-100) based on keyword match ratio.
    """
    if total_keywords == 0:
        return 0
    return min(100, max(0, int((matched_count / total_keywords) * 100)))


def format_keywords_for_prompt(keywords: List[str]) -> str:
    """Format keyword list for prompt insertion."""
    if not keywords:
        return "None"
    return ", ".join(keywords[:20])  # Limit to 20 keywords per category

