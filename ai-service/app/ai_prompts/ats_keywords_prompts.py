"""AI Prompts for ATS Keyword Extraction."""


EXTRACT_ATS_KEYWORDS_PROMPT = """
You are an expert ATS (Applicant Tracking System) specialist.
Analyze the following job description and extract the most important keywords that an ATS system would look for.

Categorize keywords into these groups:
1. **skills**: Technical skills, programming languages, methodologies (e.g., "Java", "System Design", "Agile")
2. **technologies**: Frameworks, platforms, databases, services (e.g., "Spring Boot", "AWS", "PostgreSQL")
3. **tools**: Software tools and applications (e.g., "Git", "Docker", "JIRA")
4. **soft_skills**: Soft skills and competencies (e.g., "Leadership", "Communication", "Problem Solving")

Job Description:
{job_description}

Instructions:
- Extract 5-8 keywords per category
- Focus on keywords that are most relevant to the job
- Include both explicit and implicit requirements
- Prioritize keywords mentioned multiple times or with emphasis
- Ensure keywords are specific and searchable by ATS
- Use exact terminology from the job description where possible

Return ONLY a valid JSON object with no markdown, no code blocks, and no extra text:
{{
    "skills": ["skill1", "skill2", ...],
    "technologies": ["tech1", "tech2", ...],
    "tools": ["tool1", "tool2", ...],
    "soft_skills": ["skill1", "skill2", ...]
}}
"""


EXTRACT_ATS_KEYWORDS_FALLBACK_PROMPT = """
Extract ATS keywords from this job description. Return valid JSON only.

Job Description:
{job_description}

Return only:
{{
    "skills": ["skill1", "skill2"],
    "technologies": ["tech1", "tech2"],
    "tools": ["tool1", "tool2"],
    "soft_skills": ["skill1", "skill2"]
}}
"""

