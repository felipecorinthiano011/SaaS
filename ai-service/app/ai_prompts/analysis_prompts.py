"""AI Prompt templates for resume analysis."""

EXTRACT_KEYWORDS_PROMPT = """
You are an expert ATS (Applicant Tracking System) analyst.
Extract the most important technical and non-technical keywords from the following job description.
Focus on skills, tools, technologies, certifications, and experiences that an ATS system would look for.

Job Description:
{job_description}

Return ONLY a JSON object with this exact format (no markdown, no extra text):
{{
  "technical_keywords": ["keyword1", "keyword2", ...],
  "soft_skills": ["skill1", "skill2", ...],
  "certifications": ["cert1", "cert2", ...],
  "required_experience": ["exp1", "exp2", ...]
}}

Ensure the lists contain at least 15-20 total keywords.
"""

ANALYZE_RESUME_PROMPT = """
You are an expert resume analyst and ATS specialist.
Analyze the following resume against the job description and keywords.

Job Description:
{job_description}

Resume:
{resume_text}

Required Keywords:
Technical: {technical_keywords}
Soft Skills: {soft_skills}
Certifications: {certifications}
Experience: {required_experience}

Provide analysis in JSON format (no markdown, no extra text):
{{
  "matched_keywords": ["keyword1", "keyword2", ...],
  "missing_keywords": ["keyword1", "keyword2", ...],
  "ats_match_percentage": 85,
  "strengths": ["strength1", "strength2", ...],
  "weaknesses": ["weakness1", "weakness2", ...],
  "gaps_analysis": "Brief analysis of major gaps between resume and job requirements"
}}
"""

OPTIMIZE_RESUME_PROMPT = """
You are an expert resume writer and ATS optimizer.
Optimize the following resume to better match the job description and ATS requirements.
Make the resume more impactful while keeping it truthful and professional.

Original Resume:
{resume_text}

Missing Keywords that could be naturally incorporated:
{missing_keywords}

Job Requirements:
{job_description}

Return the optimized resume text. Make it:
1. More ATS-friendly (use standard formatting, clear section headers)
2. Incorporate missing keywords naturally where relevant
3. Use stronger action verbs
4. Quantify achievements where possible
5. Highlight relevant experience more prominently

Return ONLY the optimized resume text (no markdown formatting, no code blocks).
"""

GENERATE_SUGGESTIONS_PROMPT = """
You are a career coach specializing in job application strategies.
Based on the resume analysis, provide actionable suggestions to improve job match.

Resume Analysis:
- ATS Match: {ats_match_percentage}%
- Missing Keywords: {missing_keywords}
- Main Gaps: {gaps_analysis}

Provide 5-7 specific, actionable suggestions in JSON format (no markdown, no extra text):
{{
  "suggestions": [
    {{
      "category": "Skills",
      "suggestion": "Add XYZ certification",
      "priority": "high",
      "impact": "Would improve ATS match by 15%"
    }},
    ...
  ]
}}

Categories: Skills, Experience, Certifications, Technical, Formatting, Keywords
Priorities: high, medium, low
"""

