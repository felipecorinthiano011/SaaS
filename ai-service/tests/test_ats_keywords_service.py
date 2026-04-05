"""Tests for ATS Keywords Service."""

import pytest
from app.services.ats_keywords_service import ATSKeywordsService
from app.schemas.ats_keywords import ATSKeywordsResponse
from app.utils.ats_keyword_utils import (
    extract_keywords_regex,
    categorize_keywords_heuristic,
    remove_duplicates_preserve_order,
    get_most_common_keywords,
)


class TestATSKeywordUtils:
    """Test utility functions for ATS keyword extraction."""

    def test_extract_keywords_regex(self):
        """Test regex-based keyword extraction."""
        text = "We need a Python developer with Spring Boot experience and Docker knowledge"
        keywords = extract_keywords_regex(text)

        assert len(keywords) > 0
        # Should find these keywords
        assert any("python" in kw.lower() for kw in keywords)
        assert any("spring" in kw.lower() or "boot" in kw.lower() for kw in keywords)

    def test_categorize_keywords_technologies(self):
        """Test categorization of technology keywords."""
        keywords = ["Java", "Spring Boot", "PostgreSQL", "Docker", "Git"]
        job_desc = "We need a Java developer with Docker experience"

        result = categorize_keywords_heuristic(keywords, job_desc)

        assert isinstance(result, dict)
        assert "skills" in result
        assert "technologies" in result
        assert "tools" in result
        assert "soft_skills" in result

        # Docker should be in tools
        assert "Docker" in result["tools"]

    def test_categorize_keywords_soft_skills(self):
        """Test categorization of soft skills."""
        keywords = ["Leadership", "Communication", "Problem Solving", "Java"]
        job_desc = "Leadership and communication required"

        result = categorize_keywords_heuristic(keywords, job_desc)

        assert "Leadership" in result["soft_skills"]
        assert "Communication" in result["soft_skills"]
        assert "Java" in result["skills"]

    def test_remove_duplicates_preserve_order(self):
        """Test duplicate removal while preserving order."""
        items = ["Java", "java", "Python", "JAVA", "Python"]
        result = remove_duplicates_preserve_order(items)

        assert len(result) == 2
        assert result[0].lower() == "java"
        assert result[1].lower() == "python"

    def test_get_most_common_keywords(self):
        """Test extraction of most common keywords."""
        text = "Java Java Java Python Docker Docker Docker Docker"
        keywords = get_most_common_keywords(text, count=3)

        assert len(keywords) <= 3
        assert "docker" in keywords or "java" in keywords


class TestATSKeywordsService:
    """Test ATS Keywords Service."""

    @pytest.fixture
    def service(self):
        """Create service instance without LLM."""
        return ATSKeywordsService(llm_client=None)

    @pytest.fixture
    def sample_job_description(self):
        """Sample job description for testing."""
        return """
        Senior Java Developer
        
        We are looking for an experienced Java developer with:
        - 5+ years of Java and Spring Boot experience
        - Strong knowledge of microservices and Docker
        - Experience with PostgreSQL and SQL optimization
        - Kubernetes deployment experience
        - Git and CI/CD pipelines (Jenkins, GitLab CI)
        - Strong problem-solving and analytical skills
        - Excellent communication and team collaboration
        - Experience with AWS cloud services
        - RESTful API design
        
        Required Skills:
        - Java 11+
        - Spring Boot 3.0+
        - Microservices architecture
        - Docker containers
        - Kubernetes orchestration
        - SQL and Database design
        
        Nice to have:
        - AWS certification
        - Kubernetes certification
        - Message queues (RabbitMQ, Kafka)
        """

    def test_extract_keywords_valid_input(self, service, sample_job_description):
        """Test keyword extraction with valid input."""
        result = service.extract_keywords(sample_job_description)

        assert isinstance(result, ATSKeywordsResponse)
        assert isinstance(result.skills, list)
        assert isinstance(result.technologies, list)
        assert isinstance(result.tools, list)
        assert isinstance(result.soft_skills, list)

    def test_extract_keywords_too_short(self, service):
        """Test that short descriptions are rejected."""
        with pytest.raises(ValueError, match="at least 50 characters"):
            service.extract_keywords("Too short")

    def test_extract_keywords_contains_expected_terms(self, service, sample_job_description):
        """Test that extracted keywords contain expected terms."""
        result = service.extract_keywords(sample_job_description)

        # Combine all keywords
        all_keywords = (
            result.skills +
            result.technologies +
            result.tools +
            result.soft_skills
        )

        all_keywords_lower = [kw.lower() for kw in all_keywords]

        # Should find some expected keywords
        assert any("java" in kw for kw in all_keywords_lower)
        assert any("spring" in kw for kw in all_keywords_lower)

    def test_extract_keywords_no_duplicates(self, service, sample_job_description):
        """Test that extracted keywords have no duplicates."""
        result = service.extract_keywords(sample_job_description)

        # Check for duplicates in each category
        for category in [result.skills, result.technologies, result.tools, result.soft_skills]:
            category_lower = [kw.lower() for kw in category]
            assert len(category_lower) == len(set(category_lower)), \
                f"Found duplicates in category with keywords: {category}"

    def test_extract_and_analyze_without_resume(self, service, sample_job_description):
        """Test extract_and_analyze without resume."""
        result = service.extract_and_analyze(sample_job_description)

        assert "keywords" in result
        assert "total_keywords" in result
        assert "matched" not in result

    def test_extract_and_analyze_with_resume(self, service, sample_job_description):
        """Test extract_and_analyze with resume matching."""
        resume = "I am a Java developer with 6 years of experience. I know Spring Boot, Docker, and PostgreSQL."

        result = service.extract_and_analyze(sample_job_description, resume)

        assert "keywords" in result
        assert "matched" in result
        assert isinstance(result["matched"], dict)
        assert "skills" in result["matched"]
        assert "technologies" in result["matched"]
        assert "tools" in result["matched"]
        assert "soft_skills" in result["matched"]

    def test_find_matching_keywords(self, service, sample_job_description):
        """Test keyword matching against resume."""
        resume = "I have Java, Spring Boot, Docker, and Git experience"

        keywords = service.extract_keywords(sample_job_description)
        matched = service._find_matching_keywords(keywords, resume)

        assert isinstance(matched, dict)
        # Should find Java in skills
        matched_skills_lower = [s.lower() for s in matched["skills"]]
        matched_techs_lower = [t.lower() for t in matched["technologies"]]

        # At least one keyword should match
        total_matched = len(matched_skills_lower) + len(matched_techs_lower) + \
                       len(matched["tools"]) + len(matched["soft_skills"])
        assert total_matched > 0


class TestATSKeywordsIntegration:
    """Integration tests for ATS Keywords Service."""

    def test_full_workflow(self):
        """Test complete workflow from job description to keywords."""
        service = ATSKeywordsService(llm_client=None)

        job_description = """
        Machine Learning Engineer
        
        Requirements:
        - Python programming (3+ years)
        - TensorFlow or PyTorch experience
        - Scikit-learn and Pandas
        - AWS SageMaker
        - Git and GitHub
        - SQL and PostgreSQL
        - Strong analytical and problem-solving skills
        - Excellent communication
        """

        resume = """
        Python Developer
        - 5 years Python experience
        - TensorFlow and Keras
        - PostgreSQL database design
        - GitHub contributor
        """

        # Extract keywords
        keywords = service.extract_keywords(job_description)

        # Check that we got all categories
        assert len(keywords.skills) > 0
        assert len(keywords.technologies) > 0
        assert len(keywords.soft_skills) > 0

        # Analyze with resume
        analysis = service.extract_and_analyze(job_description, resume)

        assert analysis["total_keywords"] > 0
        assert len(analysis["matched"]["skills"]) > 0 or \
               len(analysis["matched"]["technologies"]) > 0

    def test_realistic_job_descriptions(self):
        """Test with realistic job descriptions of various types."""
        service = ATSKeywordsService(llm_client=None)

        test_cases = [
            ("Backend Developer", """
            Backend Engineer - Java/Spring Boot
            - Java 11+, Spring Boot 2.7+
            - Microservices architecture
            - Docker and Kubernetes
            - REST APIs, GraphQL
            - PostgreSQL, MongoDB
            """),
            ("Frontend Developer", """
            Frontend Developer - React
            - React 18+, TypeScript
            - Webpack, Babel
            - HTML5, CSS3, SCSS
            - Jest testing
            - Git, GitHub Actions
            """),
            ("DevOps Engineer", """
            DevOps Engineer
            - Linux, bash scripting
            - Docker, Kubernetes
            - Jenkins, GitLab CI/CD
            - AWS, Terraform
            - Monitoring: Prometheus, ELK
            """),
        ]

        for job_title, description in test_cases:
            keywords = service.extract_keywords(description)

            # Should extract something
            total = len(keywords.skills) + len(keywords.technologies) + \
                   len(keywords.tools) + len(keywords.soft_skills)
            assert total > 0, f"Failed to extract keywords for {job_title}"

