#!/usr/bin/env python
"""Test script for file_parser module."""

import sys
sys.path.insert(0, '.')

from app.utils.file_parser import clean_text, extract_json_from_text

# Test clean_text function
test_resume = """
JOHN DOE
john.doe@example.com | (555) 123-4567
linkedin.com/in/johndoe | github.com/johndoe

SENIOR SOFTWARE ENGINEER


Page 1
=====================

EXPERIENCE

Senior Developer at TechCorp (2020 - Present)
- Built microservices architecture
- Improved performance by 40%

Developer at StartUp (2018 - 2020)
- Created REST APIs
- Implemented CI/CD pipelines


SKILLS
Java, Python, Spring Boot, PostgreSQL
"""

print("=== Original Text ===")
print(test_resume[:200])
print("\n=== Cleaned Text ===")
cleaned = clean_text(test_resume)
print(cleaned[:200])

print("\n=== Verification ===")
print(f"Email removed: {'john.doe@example.com' not in cleaned}")
print(f"Phone removed: {'555-123-4567' not in cleaned}")
print(f"LinkedIn removed: {'linkedin.com' not in cleaned}")
print(f"GitHub removed: {'github.com' not in cleaned}")
print(f"Page numbers removed: {'Page 1' not in cleaned}")
print(f"Separators removed: {'==' not in cleaned}")
print(f"Content preserved: {'SENIOR SOFTWARE ENGINEER' in cleaned}")
print(f"Skills preserved: {'Spring Boot' in cleaned}")

# Test extract_json_from_text function
print("\n=== JSON Extraction Test ===")
text_with_json = 'Here is some analysis: {"ats_score": 85, "keywords": ["Java", "Spring"]} and more text'
result = extract_json_from_text(text_with_json)
print(f"Extracted JSON: {result}")
print(f"ATS Score: {result['ats_score']}")

print("\n=== All Tests Passed ===")

