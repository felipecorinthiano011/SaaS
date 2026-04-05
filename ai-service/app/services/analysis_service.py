import re
from collections import Counter

from app.core.config import settings


class AnalysisService:
    def analyze(self, job_description: str, resume_text: str) -> dict:
        keywords = self._extract_keywords(job_description)
        matched_keywords = [kw for kw in keywords if kw.lower() in resume_text.lower()]

        if not keywords:
            score = 0
        else:
            score = int((len(matched_keywords) / len(keywords)) * 100)

        missing_keywords = [kw for kw in keywords if kw.lower() not in resume_text.lower()]

        optimized_resume = self._generate_optimized_resume(resume_text, missing_keywords)
        gap_summary = self._build_gap_summary(missing_keywords)

        return {
            "atsScore": score,
            "extractedKeywords": keywords,
            "optimizedResume": optimized_resume,
            "gapSummary": gap_summary,
        }

    def _extract_keywords(self, job_description: str) -> list[str]:
        tokens = re.findall(r"[A-Za-z][A-Za-z+.#-]{2,}", job_description)
        stop_words = {
            "with",
            "from",
            "this",
            "that",
            "your",
            "have",
            "will",
            "team",
            "work",
            "role",
            "experience",
            "years",
            "about",
            "strong",
            "skills",
            "ability",
        }
        filtered = [token for token in tokens if token.lower() not in stop_words]
        top = Counter(token.lower() for token in filtered).most_common(settings.minimum_keyword_count)
        return [item[0] for item in top]

    def _generate_optimized_resume(self, resume_text: str, missing_keywords: list[str]) -> str:
        if not missing_keywords:
            return resume_text

        additions = "\n\nSuggested ATS keyword enhancements:\n- " + "\n- ".join(missing_keywords[:10])
        return resume_text + additions

    def _build_gap_summary(self, missing_keywords: list[str]) -> str:
        if not missing_keywords:
            return "Your resume already aligns well with the provided job description."
        return (
            "Consider incorporating these missing keywords where accurate and truthful: "
            + ", ".join(missing_keywords[:12])
        )
