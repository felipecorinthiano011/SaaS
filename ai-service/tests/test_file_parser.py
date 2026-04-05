"""Tests for file parser utility module."""

import pytest
import tempfile
from pathlib import Path
from app.utils.file_parser import (
    clean_text,
    extract_resume_text,
    extract_json_from_text,
)


class TestCleanText:
    """Test the clean_text function."""

    def test_remove_email_addresses(self):
        """Test removal of email addresses."""
        text = "Contact me at john.doe@example.com for more info"
        cleaned = clean_text(text)
        assert "john.doe@example.com" not in cleaned
        assert "Contact me at" in cleaned

    def test_remove_urls(self):
        """Test removal of URLs."""
        text = "Visit my website at https://example.com or http://portfolio.io"
        cleaned = clean_text(text)
        assert "https://" not in cleaned
        assert "http://" not in cleaned
        assert "example.com" not in cleaned

    def test_remove_www_urls(self):
        """Test removal of www URLs."""
        text = "Check out www.github.com/user and www.linkedin.com"
        cleaned = clean_text(text)
        assert "www." not in cleaned

    def test_remove_linkedin_profiles(self):
        """Test removal of LinkedIn profile URLs."""
        text = "LinkedIn: linkedin.com/in/john-doe-123456 for more details"
        cleaned = clean_text(text)
        assert "linkedin.com/in" not in cleaned

    def test_remove_github_profiles(self):
        """Test removal of GitHub URLs."""
        text = "My code: github.com/johndoe/projects"
        cleaned = clean_text(text)
        assert "github.com" not in cleaned

    def test_remove_phone_numbers(self):
        """Test removal of phone numbers in various formats."""
        text = "Call me at 555-123-4567 or (555) 123-4567 or +1-555-123-4567"
        cleaned = clean_text(text)
        assert "555-123-4567" not in cleaned
        assert "(555)" not in cleaned
        assert "+1" not in cleaned

    def test_remove_page_numbers(self):
        """Test removal of page numbers and separators."""
        text = "Some content\nPage 1\nMore content\n---\nFinal section"
        cleaned = clean_text(text)
        assert "Page 1" not in cleaned
        assert "---" not in cleaned

    def test_remove_extra_whitespace(self):
        """Test removal of extra whitespace."""
        text = "Text    with     extra     spaces\nAnd   multiple\n\n\n\nlines"
        cleaned = clean_text(text)
        assert "    " not in cleaned
        assert "\n\n\n" not in cleaned

    def test_remove_multiple_newlines(self):
        """Test removal of multiple consecutive newlines."""
        text = "Line 1\n\n\n\nLine 2\n\n\n\nLine 3"
        cleaned = clean_text(text)
        # Should have at most 2 consecutive newlines
        assert "\n\n\n" not in cleaned

    def test_comprehensive_cleaning(self):
        """Test comprehensive cleaning with all features."""
        text = """
        John Doe
        john.doe@example.com | linkedin.com/in/johndoe | (555) 123-4567
        https://portfolio.io | github.com/johndoe
        
        
        Page 1
        --------
        
        EXPERIENCE
        
        Senior Developer at TechCorp    (2020 - Present)
        - Led development of microservices
        - Improved system performance by 40%
        
        
        
        Developer at StartUp Co  (2018 - 2020)
        - Built REST APIs
        - Page 2 of resume continues...
        """
        cleaned = clean_text(text)

        # All personal info should be removed
        assert "john.doe@example.com" not in cleaned
        assert "linkedin.com" not in cleaned
        assert "(555)" not in cleaned
        assert "portfolio.io" not in cleaned
        assert "github.com" not in cleaned

        # Content should remain
        assert "John Doe" in cleaned
        assert "Senior Developer" in cleaned
        assert "TechCorp" in cleaned
        assert "REST APIs" in cleaned

        # No extra whitespace
        assert "    " not in cleaned
        assert "\n\n\n" not in cleaned


class TestExtractJsonFromText:
    """Test the extract_json_from_text function."""

    def test_extract_valid_json(self):
        """Test extraction of valid JSON from text."""
        text = 'Some text before {"key": "value", "number": 42} and some text after'
        result = extract_json_from_text(text)
        assert result == {"key": "value", "number": 42}

    def test_extract_nested_json(self):
        """Test extraction of nested JSON."""
        text = 'Prefix {"outer": {"inner": "data"}} Suffix'
        result = extract_json_from_text(text)
        assert result == {"outer": {"inner": "data"}}

    def test_extract_json_with_array(self):
        """Test extraction of JSON containing arrays."""
        text = 'Text {"items": [1, 2, 3]} More text'
        result = extract_json_from_text(text)
        assert result == {"items": [1, 2, 3]}

    def test_invalid_json(self):
        """Test error handling for invalid JSON."""
        text = 'Some text {invalid json} more text'
        with pytest.raises(ValueError):
            extract_json_from_text(text)

    def test_no_json_found(self):
        """Test error handling when no JSON is found."""
        text = 'Text without any JSON object'
        with pytest.raises(ValueError):
            extract_json_from_text(text)


class TestExtractResumeText:
    """Test the extract_resume_text function."""

    def test_extract_with_file_path_string(self):
        """Test extraction with file path as string."""
        # This would require actual PDF/DOCX file
        # Skipping actual file test as it requires test files
        pass

    def test_extract_with_path_object(self):
        """Test extraction with Path object."""
        # This would require actual PDF/DOCX file
        pass

    def test_invalid_file_format(self):
        """Test error handling for unsupported file format."""
        with pytest.raises(ValueError, match="Unsupported file format"):
            extract_resume_text("resume.txt")


class TestIntegration:
    """Integration tests."""

    def test_clean_realistic_resume_text(self):
        """Test cleaning with realistic resume-like content."""
        resume_text = """
        JOHN ANDERSON
        john.anderson@gmail.com | (415) 555-0123
        linkedin.com/in/johnanderson | github.com/janderson
        https://portfolio.example.com
        
        SENIOR SOFTWARE ENGINEER
        
        San Francisco, CA
        
        ========================================
        
        PROFESSIONAL SUMMARY
        
        Experienced software engineer with 8+ years of experience
        building scalable web applications. Expert in Java, Python,
        and cloud technologies.
        
        EXPERIENCE
        
        Senior Engineer | TechCorp Inc.
        January 2020 - Present
        - Architected microservices platform serving 1M+ users
        - Led team of 6 engineers
        - Improved system performance by 35%
        
        Software Engineer | StartUp Co.
        June 2018 - December 2019
        - Built REST APIs using Spring Boot
        - Implemented CI/CD pipeline
        
        SKILLS
        
        Languages: Java, Python, JavaScript, SQL
        Frameworks: Spring Boot, Django, React
        Databases: PostgreSQL, MongoDB
        Cloud: AWS, GCP, Docker
        
        Page 1 of 1
        """

        cleaned = clean_text(resume_text)

        # Personal info should be removed
        assert "john.anderson@gmail.com" not in cleaned
        assert "(415)" not in cleaned
        assert "linkedin.com" not in cleaned
        assert "github.com" not in cleaned
        assert "portfolio.example.com" not in cleaned

        # Content should be preserved
        assert "JOHN ANDERSON" in cleaned
        assert "SENIOR SOFTWARE ENGINEER" in cleaned
        assert "TechCorp" in cleaned
        assert "Spring Boot" in cleaned
        assert "Python" in cleaned
        assert "PostgreSQL" in cleaned

        # No page numbers or separators
        assert "Page 1 of 1" not in cleaned
        assert "========" not in cleaned

        # Good for AI processing
        lines = cleaned.split('\n')
        assert all(line == line.strip() for line in lines)
        assert not any(line == '' for line in lines)

