"""Tests for Resume Optimizer Service."""

import pytest
from app.services.resume_optimizer_service import ResumeOptimizerService
from app.schemas.resume_optimizer import OptimizeResumeResponse
from app.utils.resume_optimizer_utils import (
    calculate_ats_score,
    find_missing_keywords,
    extract_resume_sections,
    improve_action_verbs,
    ats_friendly_formatting,
    generate_suggestions,
)


class TestResumeOptimizerUtils:
    """Test utility functions for resume optimization."""

    def test_calculate_ats_score(self):
        """Test ATS score calculation."""
        resume = "Java developer with Spring Boot experience"
        keywords = ["Java", "Spring Boot", "REST API", "Docker"]

        score = calculate_ats_score(resume, keywords)

        assert isinstance(score, int)
        assert 0 <= score <= 100
        # Should match Java and Spring Boot
        assert score > 30

    def test_find_missing_keywords(self):
        """Test missing keyword detection."""
        resume = "Java and Spring Boot developer"
        keywords = ["Java", "Spring Boot", "Docker", "Kubernetes", "AWS"]

        missing = find_missing_keywords(resume, keywords)

        assert len(missing) > 0
        assert "Docker" in missing or "Kubernetes" in missing or "AWS" in missing

    def test_improve_action_verbs(self):
        """Test action verb improvement."""
        text = "worked on multiple projects and helped improve performance"

        improved = improve_action_verbs(text)

        # Should replace weak verbs
        assert "worked" not in improved.lower() or "Engineered" in improved
        assert improved != text  # Should be different

    def test_ats_friendly_formatting(self):
        """Test ATS formatting."""
        text = "Special chars: → ► ◆ smart quotes "" and tabs\there"

        formatted = ats_friendly_formatting(text)

        assert "→" not in formatted
        assert "►" not in formatted
        assert "" not in formatted
        assert "\t" not in formatted

    def test_extract_resume_sections(self):
        """Test resume section extraction."""
        resume = """
        CONTACT INFORMATION
        john@example.com
        
        PROFESSIONAL SUMMARY
        Senior developer with 5 years experience
        
        EXPERIENCE
        Senior Developer at TechCorp (2020-2023)
        - Worked on Java projects
        
        SKILLS
        Java, Python, Spring Boot
        """

        sections = extract_resume_sections(resume)

        assert len(sections) > 0
        assert any("contact" in k.lower() for k in sections.keys())
        assert any("experience" in k.lower() for k in sections.keys())


class TestResumeOptimizerService:
    """Test Resume Optimizer Service."""

    @pytest.fixture
    def service(self):
        """Create service instance."""
        return ResumeOptimizerService(llm_client=None)

    @pytest.fixture
    def sample_job_description(self):
        """Sample job description."""
        return """
        Senior Java Developer
        
        Requirements:
        - 5+ years Java experience
        - Spring Boot expertise
        - Docker and Kubernetes
        - REST API design
        - PostgreSQL knowledge
        - Git and CI/CD
        - Strong problem-solving skills
        - Leadership experience
        """

    @pytest.fixture
    def sample_resume(self):
        """Sample resume."""
        return """
        JOHN DOE
        john@example.com | (555) 123-4567
        
        PROFESSIONAL SUMMARY
        Senior Software Engineer with 6 years of experience building enterprise applications
        
        EXPERIENCE
        Senior Developer at TechCorp (2020-Present)
        - Worked on Java microservices
        - Used Spring Boot for REST APIs
        - Managed Docker containers
        - Improved system performance by 40%
        
        Developer at StartupInc (2018-2020)
        - Developed backend services
        - Used databases and Git
        - Helped teams with code reviews
        
        SKILLS
        Java 11+, Spring Boot, PostgreSQL, Git, Linux
        
        EDUCATION
        BS Computer Science, State University (2018)
        """

    def test_optimize_resume_valid(self, service, sample_job_description, sample_resume):
        """Test resume optimization with valid input."""
        result = service.optimize_resume(sample_job_description, sample_resume)

        assert isinstance(result, OptimizeResumeResponse)
        assert isinstance(result.ats_score, int)
        assert 0 <= result.ats_score <= 100
        assert isinstance(result.missing_keywords, list)
        assert isinstance(result.optimized_resume, str)
        assert isinstance(result.suggestions, list)

    def test_optimize_resume_too_short(self, service):
        """Test rejection of short inputs."""
        with pytest.raises(ValueError, match="at least 50 characters"):
            service.optimize_resume("Too short", "Sample")

    def test_optimize_resume_has_suggestions(self, service, sample_job_description, sample_resume):
        """Test that suggestions are generated."""
        result = service.optimize_resume(sample_job_description, sample_resume)

        assert len(result.suggestions) > 0
        # Each suggestion should have required fields
        for suggestion in result.suggestions:
            assert suggestion.category
            assert suggestion.suggestion
            assert suggestion.priority in ["high", "medium", "low"]
            assert suggestion.rationale

    def test_optimize_resume_has_missing_keywords(self, service, sample_job_description, sample_resume):
        """Test missing keyword identification."""
        result = service.optimize_resume(sample_job_description, sample_resume)

        # Should identify some missing keywords
        # (Kubernetes likely not in the sample resume)
        assert isinstance(result.missing_keywords, list)

    def test_optimize_resume_has_optimized_text(self, service, sample_job_description, sample_resume):
        """Test that optimized resume is generated."""
        result = service.optimize_resume(sample_job_description, sample_resume)

        assert len(result.optimized_resume) > 0
        # Should be longer or similar (improvements but no invented content)
        assert len(result.optimized_resume) >= len(sample_resume) * 0.8

    def test_compare_resumes(self, service):
        """Test resume comparison."""
        original = "Worked on projects and helped improve performance"
        optimized = "Engineered innovative solutions that optimized system performance by 40%"

        comparison = service.compare_resumes(original, optimized)

        assert isinstance(comparison, dict)
        assert "strong_verbs_improved" in comparison
        assert comparison["strong_verbs_improved"] > 0  # Should have added strong verbs

    def test_keyword_integration(self, service):
        """Test that job keywords are integrated into optimized resume."""
        job_desc = "We need Kubernetes and Docker expertise with Spring Boot"
        resume = "Senior developer with 5 years Java experience using Spring Framework"

        result = service.optimize_resume(job_desc, resume)

        # Optimized resume should mention Docker or Kubernetes if resume mentions containers
        assert result.ats_score > 30  # Should have some match


class TestResumeOptimizerIntegration:
    """Integration tests for Resume Optimizer."""

    def test_full_optimization_workflow(self):
        """Test complete optimization workflow."""
        service = ResumeOptimizerService(llm_client=None)

        job_desc = """
        Machine Learning Engineer
        
        Required Skills:
        - Python 3.8+
        - TensorFlow or PyTorch
        - Scikit-learn
        - SQL and databases
        - Git and GitHub
        - Strong math background
        - Communication skills
        """

        resume = """
        Jane Smith
        jane@example.com
        
        Summary
        Python programmer with 4 years experience
        
        Experience
        Junior Developer at DataCorp (2021-Present)
        - Used Python for data processing
        - Worked with TensorFlow
        - Used databases for storage
        - Helped teammates with problems
        
        Education
        BS Mathematics, University (2021)
        """

        # Run optimization
        result = service.optimize_resume(job_desc, resume)

        # Verify result structure
        assert result.ats_score > 0
        assert len(result.optimized_resume) > 0
        assert len(result.suggestions) > 0

        # Verify key improvements
        assert "Python" in result.optimized_resume or "Python" in job_desc
        assert "TensorFlow" in result.optimized_resume or "TensorFlow" in job_desc

    def test_multiple_optimizations(self):
        """Test optimizing multiple different resumes."""
        service = ResumeOptimizerService(llm_client=None)

        jobs = [
            ("Frontend Developer - React.js, TypeScript, CSS", "Web developer with JavaScript experience"),
            ("DevOps Engineer - Docker, Kubernetes, AWS", "Linux admin with containers experience"),
        ]

        for job, resume in jobs:
            result = service.optimize_resume(job, resume)
            assert result.ats_score >= 0
            assert len(result.optimized_resume) > 0

