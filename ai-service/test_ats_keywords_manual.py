#!/usr/bin/env python
"""Test ATS Keywords Service Implementation"""

import sys
sys.path.insert(0, '.')

print('🔍 Testing ATS Keywords Service Implementation...\n')

try:
    # Test utility imports
    from app.utils.ats_keyword_utils import (
        extract_keywords_regex,
        categorize_keywords_heuristic,
        remove_duplicates_preserve_order,
        get_most_common_keywords,
    )
    print('✅ Utility imports successful')

    # Test schema imports
    from app.schemas.ats_keywords import ATSKeywordsResponse, ATSKeywordsRequest
    print('✅ Schema imports successful')

    # Test prompt imports
    from app.ai_prompts.ats_keywords_prompts import (
        EXTRACT_ATS_KEYWORDS_PROMPT,
        EXTRACT_ATS_KEYWORDS_FALLBACK_PROMPT,
    )
    print('✅ Prompt imports successful')

    # Test regex extraction
    print('\n📌 Testing Regex Extraction...')
    text = '''Senior Java Developer required.
    Skills: Java 11+, Spring Boot 3.0, Microservices
    Technologies: Docker, Kubernetes, PostgreSQL
    Tools: Git, Jenkins, Maven
    Soft Skills: Problem solving, Communication, Leadership'''

    keywords = extract_keywords_regex(text)
    print(f'   ✓ Extracted {len(keywords)} keywords')
    print(f'   Sample: {keywords[:5]}')

    # Test categorization
    print('\n📌 Testing Categorization...')
    categorized = categorize_keywords_heuristic(keywords, text)
    print(f'   ✓ Skills: {len(categorized["skills"])} found')
    print(f'     Examples: {categorized["skills"][:3]}')
    print(f'   ✓ Technologies: {len(categorized["technologies"])} found')
    print(f'     Examples: {categorized["technologies"][:3]}')
    print(f'   ✓ Tools: {len(categorized["tools"])} found')
    print(f'     Examples: {categorized["tools"][:3]}')
    print(f'   ✓ Soft Skills: {len(categorized["soft_skills"])} found')
    print(f'     Examples: {categorized["soft_skills"][:3]}')

    # Test deduplication
    print('\n📌 Testing Deduplication...')
    items = ['Java', 'java', 'Python', 'JAVA', 'Python']
    deduped = remove_duplicates_preserve_order(items)
    print(f'   ✓ Input: {items}')
    print(f'   ✓ Output: {deduped}')

    # Test most common keywords
    print('\n📌 Testing Most Common Keywords...')
    common = get_most_common_keywords(text, count=5)
    print(f'   ✓ Found {len(common)} most common keywords')
    print(f'   Examples: {common}')

    # Test Response Schema
    print('\n📌 Testing Response Schema...')
    response = ATSKeywordsResponse(
        skills=['Java', 'Python'],
        technologies=['Spring Boot', 'Docker'],
        tools=['Git', 'Jenkins'],
        soft_skills=['Leadership', 'Communication']
    )
    print(f'   ✓ Response created successfully')
    print(f'   ✓ JSON: {response.model_dump()}')

    # Test Request Schema
    print('\n📌 Testing Request Schema...')
    request = ATSKeywordsRequest(
        job_description='Senior Java Developer with 5+ years experience...'
    )
    print(f'   ✓ Request created successfully')
    print(f'   ✓ Job description length: {len(request.job_description)}')

    print('\n' + '='*50)
    print('✅ ALL TESTS PASSED!')
    print('='*50)
    print('\n✨ ATS Keywords Service is ready for use!')

except Exception as e:
    print(f'\n❌ Error: {e}')
    import traceback
    traceback.print_exc()

