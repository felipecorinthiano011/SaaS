"""Initialize ai_prompts package."""

from app.ai_prompts.analysis_prompts import (
    EXTRACT_KEYWORDS_PROMPT,
    ANALYZE_RESUME_PROMPT,
    OPTIMIZE_RESUME_PROMPT,
    GENERATE_SUGGESTIONS_PROMPT,
)

__all__ = [
    "EXTRACT_KEYWORDS_PROMPT",
    "ANALYZE_RESUME_PROMPT",
    "OPTIMIZE_RESUME_PROMPT",
    "GENERATE_SUGGESTIONS_PROMPT",
]

