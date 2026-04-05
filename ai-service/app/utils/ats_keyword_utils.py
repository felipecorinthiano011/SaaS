"""Utility functions for ATS keyword extraction."""

import re
from collections import Counter


def extract_keywords_regex(text: str, min_length: int = 3) -> list[str]:
    """
    Extract potential keywords from text using regex patterns.

    Identifies:
    - Multi-word phrases (CamelCase, kebab-case)
    - Technical terms (+ . # characters)
    - Standard words with capitals

    Args:
        text: Text to extract keywords from
        min_length: Minimum keyword length

    Returns:
        List of extracted keywords
    """
    # Extract multi-word patterns and technical terms
    keywords = re.findall(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*|[A-Za-z][A-Za-z+.#-]{2,}", text)

    # Filter by length and remove pure stop words
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
        "by", "from", "as", "is", "be", "are", "was", "were", "have", "has", "do", "does",
        "did", "will", "would", "could", "should", "may", "might", "must", "can"
    }

    filtered = [
        kw for kw in keywords
        if len(kw) >= min_length and kw.lower() not in stop_words
    ]

    return filtered


def categorize_keywords_heuristic(keywords: list[str], job_description: str) -> dict[str, list[str]]:
    """
    Categorize keywords using heuristic patterns.

    Patterns:
    - Technologies: db, database, cloud, server, platform, framework, api, sdk
    - Tools: git, jenkins, jira, docker, kubernetes, docker-compose
    - Soft Skills: communication, leadership, problem-solving, collaboration, analytical
    - Skills: everything else (languages, methodologies)

    Args:
        keywords: List of keywords to categorize
        job_description: Original job description for context

    Returns:
        Dictionary with categorized keywords
    """
    tech_patterns = {
        r"(sql|database|db|nosql|mongodb|postgresql|mysql)",
        r"(cloud|aws|azure|gcp|serverless)",
        r"(framework|spring|django|flask|react|angular)",
        r"(api|rest|graphql|soap)",
        r"(docker|kubernetes|container)",
    }

    tool_patterns = {
        r"(git|github|gitlab|svn)",
        r"(jenkins|circleci|gitlab-ci)",
        r"(jira|confluence|asana)",
        r"(docker|docker-compose|podman)",
    }

    soft_skill_patterns = {
        r"(communication|writing|presentation)",
        r"(leadership|management|mentoring)",
        r"(problem-solving|analytical|critical thinking)",
        r"(collaboration|teamwork|team)",
        r"(creativity|innovation)",
    }

    categorized = {
        "skills": [],
        "technologies": [],
        "tools": [],
        "soft_skills": []
    }

    for keyword in keywords:
        keyword_lower = keyword.lower()

        # Check soft skills first (most specific)
        if any(re.search(pattern, keyword_lower) for pattern in soft_skill_patterns):
            categorized["soft_skills"].append(keyword)
        # Check tools
        elif any(re.search(pattern, keyword_lower) for pattern in tool_patterns):
            categorized["tools"].append(keyword)
        # Check technologies
        elif any(re.search(pattern, keyword_lower) for pattern in tech_patterns):
            categorized["technologies"].append(keyword)
        # Everything else is a skill
        else:
            categorized["skills"].append(keyword)

    return categorized


def remove_duplicates_preserve_order(items: list[str]) -> list[str]:
    """
    Remove duplicates from list while preserving order.

    Args:
        items: List with potential duplicates

    Returns:
        List with duplicates removed, order preserved
    """
    seen = set()
    result = []
    for item in items:
        item_lower = item.lower()
        if item_lower not in seen:
            seen.add(item_lower)
            result.append(item)
    return result


def get_most_common_keywords(text: str, count: int = 20) -> list[str]:
    """
    Get the most frequently occurring keywords in text.

    Args:
        text: Text to analyze
        count: Number of keywords to return

    Returns:
        List of most common keywords
    """
    words = re.findall(r"[A-Za-z+.#-]{3,}", text)
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
        "is", "are", "be", "have", "has", "will", "would", "could"
    }

    filtered = [w for w in words if w.lower() not in stop_words]
    counter = Counter(w.lower() for w in filtered)

    return [word for word, _ in counter.most_common(count)]

