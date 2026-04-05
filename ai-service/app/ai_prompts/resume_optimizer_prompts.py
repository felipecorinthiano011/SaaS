"""AI Prompts for ATS Resume Optimization."""


OPTIMIZE_RESUME_PROMPT = """
You are an expert ATS (Applicant Tracking System) resume optimizer and career coach.
Your task is to optimize a resume to better match a job description.

IMPORTANT RULES:
1. Do NOT invent experience or skills the candidate doesn't have
2. Only rephrase and reorganize existing information
3. Use strong action verbs to describe accomplishments
4. Integrate relevant keywords from the job description naturally
5. Improve bullet points for ATS-friendliness
6. Keep formatting clean and simple (avoid complex formatting)
7. Maintain truthfulness and authenticity

Job Description:
{job_description}

Original Resume:
{resume_text}

Task:
1. Analyze how well the resume matches the job description
2. Identify missing keywords that are mentioned in the job description
3. Rewrite the resume to better highlight relevant experience
4. Improve formatting for ATS compatibility
5. Generate optimization suggestions

Return ONLY a valid JSON object (no markdown, no code blocks):
{{
    "ats_score": 78,
    "missing_keywords": ["keyword1", "keyword2"],
    "optimized_resume": "Full optimized resume text here",
    "suggestions": [
        {{
            "category": "Skills",
            "suggestion": "Specific suggestion here",
            "priority": "high",
            "rationale": "Why this improves ATS match"
        }}
    ]
}}

Guidelines:
- ATS Score: 0-100 based on keyword match and relevance
- Missing Keywords: List 3-5 most impactful missing keywords from job description
- Optimized Resume: Rewrite preserving all true experience but improving clarity and keyword integration
- Suggestions: 3-5 specific, actionable improvements ranked by impact
"""


OPTIMIZE_RESUME_FALLBACK_PROMPT = """
Optimize this resume for the job description.

Job: {job_description}

Resume: {resume_text}

Return JSON:
{{
    "ats_score": 0-100,
    "missing_keywords": ["keyword1", "keyword2"],
    "optimized_resume": "improved resume text",
    "suggestions": [
        {{"category": "category", "suggestion": "text", "priority": "high", "rationale": "reason"}}
    ]
}}
"""


ANALYZE_RESUME_GAPS_PROMPT = """
Analyze the gaps between a resume and job description.

Job Requirements:
{job_description}

Candidate Resume:
{resume_text}

Identify:
1. Missing skills and qualifications
2. Experience gaps
3. Keyword mismatches
4. Areas of strong alignment

Return JSON:
{{
    "matched_skills": ["skill1", "skill2"],
    "missing_skills": ["skill1", "skill2"],
    "gap_analysis": "text analysis of gaps",
    "alignment_score": 0-100
}}
"""


IMPROVE_BULLET_POINTS_PROMPT = """
Improve these resume bullet points using strong action verbs and relevant keywords.

Current Bullets:
{bullets}

Job Keywords:
{keywords}

Requirements:
- Use strong action verbs
- Quantify achievements when possible
- Include relevant keywords naturally
- Keep concise (one line each)
- Maintain truthfulness

Return improved bullets as JSON array:
{{
    "improved_bullets": ["bullet1", "bullet2", "bullet3"]
}}
"""

