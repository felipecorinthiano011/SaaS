"""Utility functions for ATS resume optimization."""

import re
from collections import Counter


def calculate_ats_score(resume_text: str, job_keywords: list[str]) -> int:
    """
    Calculate ATS match score based on keyword presence.

    Score breakdown:
    - Keyword matching: 50%
    - Content quality: 30%
    - Formatting: 20%

    Args:
        resume_text: Resume text to analyze
        job_keywords: Keywords from job description

    Returns:
        Score from 0-100
    """
    if not job_keywords:
        return 0

    resume_lower = resume_text.lower()

    # Count matched keywords
    matched = sum(1 for kw in job_keywords if kw.lower() in resume_lower)
    keyword_score = (matched / len(job_keywords)) * 100

    # Content quality based on length and structure
    lines = [line.strip() for line in resume_text.split('\n') if line.strip()]
    sections = len(re.findall(r'^[A-Z][A-Z\s]+$', resume_text, re.MULTILINE))
    has_bullets = resume_text.count('-') + resume_text.count('•') + resume_text.count('*')

    content_score = min(100, (len(lines) * 2 + sections * 5 + has_bullets) / 3)

    # Formatting check
    formatting_score = 80
    if '<' in resume_text or '>' in resume_text:
        formatting_score -= 10
    if resume_text.count('\t') > 5:
        formatting_score -= 10

    # Weighted average
    final_score = int(
        (keyword_score * 0.5) +
        (content_score * 0.3) +
        (formatting_score * 0.2)
    )

    return min(100, max(0, final_score))


def find_missing_keywords(resume_text: str, job_keywords: list[str]) -> list[str]:
    """
    Find keywords from job description not present in resume.

    Args:
        resume_text: Resume text
        job_keywords: Keywords from job description

    Returns:
        List of missing keywords (top 5)
    """
    resume_lower = resume_text.lower()

    missing = [
        kw for kw in job_keywords
        if kw.lower() not in resume_lower
    ]

    return missing[:5]


def extract_resume_sections(resume_text: str) -> dict[str, str]:
    """
    Extract common resume sections.

    Args:
        resume_text: Full resume text

    Returns:
        Dictionary with section names as keys
    """
    sections = {}

    # Common section patterns
    section_patterns = {
        'contact': r'(CONTACT|EMAIL|PHONE|ADDRESS)',
        'summary': r'(PROFESSIONAL\s+SUMMARY|SUMMARY|OBJECTIVE)',
        'experience': r'(EXPERIENCE|WORK\s+EXPERIENCE|EMPLOYMENT)',
        'skills': r'(SKILLS|TECHNICAL\s+SKILLS)',
        'education': r'(EDUCATION|DEGREE)',
        'certifications': r'(CERTIFICATIONS?|LICENSES)',
        'projects': r'(PROJECTS?|PORTFOLIO)',
    }

    for section_name, pattern in section_patterns.items():
        matches = re.finditer(
            f'^{pattern}.*?(?=^[A-Z][A-Z\\s]+|$)',
            resume_text,
            re.MULTILINE | re.IGNORECASE
        )
        section_text = '\n'.join(m.group(0) for m in matches)
        if section_text:
            sections[section_name] = section_text

    return sections


def improve_action_verbs(text: str) -> str:
    """
    Replace weak verbs with strong action verbs.

    Args:
        text: Text containing weak verbs

    Returns:
        Text with improved verbs
    """
    weak_to_strong = {
        r'\bworked\b': 'Engineered',
        r'\bhelped\b': 'Facilitated',
        r'\bresponsible\s+for\b': 'Owned',
        r'\bwas\s+involved\s+in\b': 'Spearheaded',
        r'\bdid\b': 'Executed',
        r'\bmade\b': 'Created',
        r'\bhandled\b': 'Managed',
        r'\bused\b': 'Leveraged',
        r'\btried\b': 'Pioneered',
        r'\bhelped\s+improve\b': 'Optimized',
        r'\bwent\s+up\b': 'Increased',
        r'\bwent\s+down\b': 'Reduced',
        r'\btoo\b': 'Addressed',
    }

    result = text
    for weak, strong in weak_to_strong.items():
        result = re.sub(weak, strong, result, flags=re.IGNORECASE)

    return result


def extract_bullet_points(text: str) -> list[str]:
    """
    Extract bullet points from resume.

    Args:
        text: Resume text

    Returns:
        List of bullet points
    """
    # Match lines starting with -, *, •, or similar
    pattern = r'^[\s]*[-•*]\s+(.+)$'
    matches = re.findall(pattern, text, re.MULTILINE)
    return [match.strip() for match in matches]


def quantify_achievements(text: str) -> str:
    """
    Suggest adding numbers/metrics to bullet points.

    Args:
        text: Bullet point text

    Returns:
        Enhanced text with suggestions for quantification
    """
    # If no numbers in the text, suggest addition
    if not re.search(r'\d+', text):
        return f"{text} (consider adding metrics: %, $, or absolute numbers)"
    return text


def ats_friendly_formatting(text: str) -> str:
    """
    Clean resume for ATS compatibility.

    Args:
        text: Resume text

    Returns:
        ATS-friendly formatted text
    """
    # Remove special characters that confuse ATS
    text = text.replace('→', '-')
    text = text.replace('►', '-')
    text = text.replace('◆', '-')
    text = text.replace(''', "'")
    text = text.replace(''', "'")
    text = text.replace('"', '"')
    text = text.replace('"', '"')

    # Remove tabs, replace with spaces
    text = text.replace('\t', '  ')

    # Normalize spacing
    lines = [line.rstrip() for line in text.split('\n')]
    text = '\n'.join(lines)

    # Remove excessive blank lines
    text = re.sub(r'\n\n\n+', '\n\n', text)

    return text


def generate_suggestions(
    resume_text: str,
    job_keywords: list[str],
    ats_score: int
) -> list[dict]:
    """
    Generate optimization suggestions.

    Args:
        resume_text: Resume text
        job_keywords: Keywords from job
        ats_score: Current ATS score

    Returns:
        List of suggestions with priority
    """
    suggestions = []

    # Check for common issues
    if ats_score < 50:
        suggestions.append({
            "category": "Keywords",
            "suggestion": "Add more keywords from the job description to your resume",
            "priority": "high",
            "rationale": "Low keyword match is hurting ATS score significantly"
        })

    if '<' in resume_text or '>' in resume_text or resume_text.count('\t') > 5:
        suggestions.append({
            "category": "Formatting",
            "suggestion": "Remove special characters and complex formatting for ATS compatibility",
            "priority": "high",
            "rationale": "ATS systems struggle with unusual formatting"
        })

    # Check for weak verbs
    weak_verbs = ['worked', 'helped', 'did', 'made', 'used', 'tried']
    if any(f' {verb} ' in resume_text.lower() for verb in weak_verbs):
        suggestions.append({
            "category": "Content",
            "suggestion": "Replace weak action verbs with strong ones (Engineered, Spearheaded, Optimized)",
            "priority": "high",
            "rationale": "Strong verbs make achievements more impactful"
        })

    # Check for quantification
    bullet_count = len(extract_bullet_points(resume_text))
    if bullet_count == 0:
        suggestions.append({
            "category": "Content",
            "suggestion": "Use bullet points to highlight achievements and responsibilities",
            "priority": "high",
            "rationale": "Bullet points are ATS-friendly and improve readability"
        })
    else:
        numbered_bullets = len(re.findall(r'(\d+%|\$\d+|increased by \d+)', resume_text, re.IGNORECASE))
        if numbered_bullets < bullet_count * 0.3:
            suggestions.append({
                "category": "Content",
                "suggestion": "Add metrics and numbers to at least 30% of bullet points",
                "priority": "medium",
                "rationale": "Quantified achievements are more compelling and trackable"
            })

    # Check for required sections
    required_sections = ['experience', 'skills', 'education']
    sections = extract_resume_sections(resume_text)
    missing_sections = [s for s in required_sections if s not in sections]

    if missing_sections:
        suggestions.append({
            "category": "Structure",
            "suggestion": f"Add missing section(s): {', '.join(missing_sections)}",
            "priority": "medium",
            "rationale": "ATS systems look for standard resume sections"
        })

    # Sort by priority
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    suggestions.sort(key=lambda x: priority_order.get(x['priority'], 3))

    return suggestions[:5]  # Return top 5 suggestions


def match_resume_to_job(resume_text: str, job_keywords: list[str]) -> str:
    """
    Reorder resume sections to emphasize relevant experience.

    Args:
        resume_text: Original resume
        job_keywords: Keywords from job description

    Returns:
        Reordered resume text
    """
    sections = extract_resume_sections(resume_text)

    # Calculate section relevance
    relevance_scores = {}
    resume_lower = resume_text.lower()

    for section_name, section_text in sections.items():
        section_lower = section_text.lower()
        matched = sum(1 for kw in job_keywords if kw.lower() in section_lower)
        relevance_scores[section_name] = matched

    # Reorder by relevance (most relevant first)
    # Always put summary, then experience, then skills, then others
    preferred_order = ['summary', 'experience', 'skills', 'education', 'certifications', 'projects']

    ordered_sections = []
    for section in preferred_order:
        if section in sections:
            ordered_sections.append((section, sections[section]))

    # Add any remaining sections
    for section_name in sections:
        if not any(s[0] == section_name for s in ordered_sections):
            ordered_sections.append((section_name, sections[section_name]))

    # Reconstruct resume
    result = '\n\n'.join(section_text for _, section_text in ordered_sections)
    return result

