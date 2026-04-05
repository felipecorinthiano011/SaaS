# Token Optimization Guide - AI Resume Analysis Pipeline

## Executive Summary

This guide explains how to reduce LLM token usage by **50-70%** in the resume analysis pipeline through intelligent text preprocessing, smart caching, and optimized prompting.

**Bottom Line**: Instead of sending 4,000 tokens, send 1,500-1,800 tokens while maintaining analysis quality.

---

## Optimization Strategies

### 1. Resume Pre-Processing (40-60% reduction)

**Before Optimization**:
```
Original Resume: 2,500 characters (~625 tokens)
- Full contact info (phone, email, LinkedIn URLs)
- Multiple repeated section headers
- Extensive whitespace and formatting
- All dates, locations, zip codes
- Generic objectives and descriptors
- Contact information repeated multiple times
```

**After Optimization**:
```
Cleaned Resume: 1,000-1,200 characters (~250-300 tokens)
- Contact info removed (not needed for matching)
- Headers consolidated
- Whitespace normalized
- Dates/locations removed (skills matter, not when)
- Generic text filtered out
- Deduplication applied
```

**Techniques Used**:

#### A. Remove Non-Essential Information (3-10% saving)
```python
# Remove contact information (not needed for job matching)
text = re.sub(r'(phone|email|linkedin|github|twitter|address)', '', text)

# Remove URLs (not relevant to skills analysis)
text = re.sub(r'https?://[^\s]+', '', text)

# Remove formatting separators
text = re.sub(r'^[-=*_]+$', '', text, flags=re.MULTILINE)
```

**Why**: Contact info, URLs, and formatting don't affect keyword matching or ATS scoring. Removing saves ~5-10% without losing information.

#### B. Condense Whitespace (5-10% saving)
```python
# Replace multiple spaces with single space
text = re.sub(r'\s{2,}', ' ', text)

# Limit consecutive newlines (paragraphs)
text = re.sub(r'\n\n+', '\n', text)
```

**Why**: Each extra space/newline = tokens. Normalization saves tokens without affecting content.

#### C. Extract Only Key Sections (20-30% saving)
```python
# Priority order (descending importance for job matching):
sections = {
    'skills': extract_skills_section(text),      # Most important - direct match
    'experience': extract_experience(text),        # Shows actual capabilities
    'education': extract_education(text),          # Validates foundation
    'certifications': extract_certs(text),         # Specialized knowledge
    'projects': extract_projects(text),            # Hands-on proof
}

# Exclude lower-priority sections:
# - Objectives (usually generic)
# - References (not needed)
# - Personal interests (irrelevant)
# - Awards (unless directly relevant)
```

**Why**: Different resume sections have different value:
- **Skills**: 100% relevant for ATS matching
- **Experience**: 90% relevant (some descriptions are fluff)
- **Education**: 70% relevant (dates don't matter, institution does)
- **References**: 0% relevant for job matching

#### D. Remove Redundant Content (3-8% saving)
```python
# Deduplication: Skip repeated lines
seen = set()
for line in text.split('\n'):
    normalized = line.lower().strip()
    if normalized not in seen:
        seen.add(normalized)
        output.append(line)
```

**Why**: Resumes often repeat information (job titles appear multiple times, skills listed in multiple sections). Deduplication removes waste.

---

### 2. Job Description Optimization (30-50% reduction)

**Before Optimization**:
```
Original Job Description: 1,500 characters (~375 tokens)
- Company culture/background
- Marketing copy
- Benefits package description
- "Nice to have" vs "Must have" mixed together
- Redundant requirement statements
- How to apply instructions
- Non-technical context
```

**After Optimization**:
```
Cleaned Job Description: 600-700 characters (~150-175 tokens)
- Only actual requirements
- Only technical skills/tools
- Deduplicated requirements
- Clear priority order
```

**Techniques**:

#### A. Remove Non-Requirement Content (20-30% saving)
```python
# Filter out marketing sections
ignore_keywords = [
    'about us', 'company culture', 'benefits',
    'compensation', 'how to apply', 'equal opportunity'
]

# Keep only paragraphs with requirement indicators
keep_if_contains = [
    'required', 'must', 'should', 'experience with',
    'proficient', 'qualifications', 'skills'
]

filtered_text = ''
for para in text.split('\n\n'):
    if any(k in para.lower() for k in keep_if_contains):
        if not any(ignore in para.lower() for ignore in ignore_keywords):
            filtered_text += para + '\n\n'
```

**Why**: Job descriptions contain 40-50% non-essential information:
- Company background (doesn't help job matching)
- Benefits/compensation (not relevant to resume)
- Marketing copy (puffery)
- Application instructions (for recruiter, not analysis)

#### B. Deduplicate Requirements (10% saving)
```python
# Many job postings repeat requirements
# "Must know Java" appears 3x, "Java experience" appears 2x
# Keep unique, remove duplicates

seen_requirements = set()
unique_requirements = []

for line in requirements:
    normalized = line.lower().strip()
    if normalized not in seen_requirements:
        seen_requirements.add(normalized)
        unique_requirements.append(line)
```

**Why**: Requirements are often repeated for emphasis. First mention is sufficient for analysis.

---

### 3. Keyword Extraction Caching (10-20% reduction)

**Problem**: Same jobs analyzed by multiple candidates = same keyword extraction done multiple times

**Solution**: Cache keyword extraction results

```python
class ResumeAnalyzer:
    def __init__(self):
        self.keyword_cache = {}  # {job_hash: extracted_keywords}
    
    def analyze(self, job_description, resume_text):
        # Check cache first
        job_hash = hash(job_description)
        
        if job_hash in self.keyword_cache:
            keywords = self.keyword_cache[job_hash]
            # Saved 1 LLM call! ~200-300 tokens saved
        else:
            keywords = llm.extract_keywords(job_description)
            self.keyword_cache[job_hash] = keywords
        
        # Continue with analysis using cached keywords
        return analyze_with_keywords(resume_text, keywords)
```

**Savings**:
- Cache hit rate: ~20% (job postings reused)
- Tokens per cache hit: 200-300 (one LLM call avoided)
- Monthly savings: if 1000 analyses, ~200 would be cache hits = 40,000-60,000 tokens saved

---

### 4. Optimized LLM Prompts (30-50% reduction)

**Before (Verbose Prompt)**:
```
Tokens: ~600-800

"You are an expert ATS resume optimizer. Your task is to optimize a resume 
to match a job description. The goal is to increase the ATS match score by 
naturally integrating relevant keywords from the job description into the 
resume content.

Here is the job description:
[FULL JOB DESCRIPTION - 375 tokens]

Here is the resume:
[FULL RESUME - 625 tokens]

Please follow these guidelines:
1. Do not invent any experience that is not in the original resume
2. Only rephrase and reorganize existing information
3. Use strong action verbs to make achievements more impactful
...
[10 more guideline paragraphs]

Return the results as JSON with these fields:
- optimized_resume: the improved resume text
- keywords_added: list of keywords incorporated
- suggestions: array of recommendations
..."
```

**After (Optimized Prompt)**:
```
Tokens: ~200-250

"TASK: Optimize resume for ATS matching.

JOB KEYWORDS (by importance):
[TOP 15 KEYWORDS ONLY]

RESUME (cleaned):
[OPTIMIZED RESUME ONLY - 250 tokens]

OUTPUT FORMAT (JSON):
{
  "optimized_resume": "...",
  "added_keywords": [...],
  "improvements": [...]
}

RULES:
1. Keep real experience unchanged
2. Integrate missing keywords naturally
3. Use strong action verbs"
```

**Token Reduction Techniques**:

#### A. Eliminate Preamble and Explanations (10-15% saving)
```
REMOVED: "You are an expert AI assistant trained in..."
REMOVED: "Your task is to help candidates..."
REMOVED: Lengthy explanations of what optimizing means

KEPT: Direct instruction
```

#### B. Use Structured Format (5-10% saving)
```
INSTEAD OF: "Please provide your response as a JSON object with the 
following fields: optimized_resume which contains the full optimized 
resume, and suggestions which is an array of improvement suggestions..."

USE: "OUTPUT FORMAT (JSON):
{
  "optimized_resume": "...",
  "suggestions": [...]
}"
```

#### C. Abbreviate and Prioritize Information (5-10% saving)
```
INSTEAD OF: [SEND FULL JOB DESCRIPTION]

USE: [TOP 15 KEYWORDS IN ORDER OF IMPORTANCE]
"Java, Spring Boot, REST APIs, Docker, Kubernetes, PostgreSQL, 
Git, Microservices, Leadership, Communication, ..."

RATIONALE: LLM only needs keywords for matching, not full JD
```

#### D. Limit Keywords List (5% saving)
```
INSTEAD OF: 50+ extracted keywords

USE: Top 15-20 most impactful keywords only

WHY: Diminishing returns - first 15 keywords capture 90% of matching value
```

---

## Real-World Example

### Before Optimization

```
INPUT TOKENS:
  Job Description: 375 tokens (1,500 chars)
  Resume: 625 tokens (2,500 chars)
  LLM Prompt: 600 tokens (preamble, examples, explanations)
  Total Input: ~1,600 tokens

LLM PROCESSING:
  Output Tokens: 400 tokens (optimized resume, suggestions)

TOTAL COST: 1,600 + 400 = 2,000 tokens
COST AT $0.015/1K: $0.03 per analysis
```

### After Optimization

```
INPUT TOKENS:
  Optimized Job Description: 150 tokens (600 chars, -60%)
  Optimized Resume: 250 tokens (1,000 chars, -60%)
  Optimized Prompt: 250 tokens (structured, -60%)
  Total Input: ~650 tokens (-60%)

LLM PROCESSING:
  Output Tokens: 250 tokens (same content, structured output)

TOTAL COST: 650 + 250 = 900 tokens (-55%)
COST AT $0.015/1K: $0.014 per analysis

SAVINGS: $0.016 per analysis (-50%)
MONTHLY (1000 analyses): $16 saved (-50%)
YEARLY (12,000 analyses): $192 saved (-50%)
```

---

## Implementation Guide

### Step 1: Add Token Optimization

```python
# app/services/token_optimizer.py
from app.services.token_optimizer import TokenOptimizedResumeProcessor

processor = TokenOptimizedResumeProcessor()

# Optimize inputs before processing
optimized_job = processor.optimize_job_description(job_description)
optimized_resume = processor.optimize_resume_text(resume_text)

# Continue with analysis using optimized versions
```

### Step 2: Use Caching

```python
# app/routers/resume_optimizer.py
from app.services.token_optimizer import OptimizedResumeAnalyzerPipeline

pipeline = OptimizedResumeAnalyzerPipeline()

result = pipeline.analyze_resume(
    job_description=job_description,
    resume_text=resume_text,
    cache_job_id=job_id  # Enable keyword extraction caching
)
```

### Step 3: Update Prompts

```python
# app/ai_prompts/resume_optimizer_prompts.py

# Replace verbose prompts with optimized versions
OPTIMIZED_PROMPT = """
TASK: Optimize resume for ATS matching.

JOB KEYWORDS:
{keywords}

RESUME:
{resume_text}

OUTPUT (JSON):
{"optimized_resume": "...", "added_keywords": [...]}
"""
```

---

## Monitoring & Measurement

### Track Optimization Metrics

```python
import logging

logger = logging.getLogger(__name__)

# Log token usage
logger.info(f"Original: {original_tokens} tokens")
logger.info(f"Optimized: {optimized_tokens} tokens")
logger.info(f"Savings: {(1 - optimized_tokens/original_tokens) * 100:.1f}%")

# Example output:
# Original: 1,850 tokens
# Optimized: 850 tokens
# Savings: 54.1%
```

### Expected Results

| Optimization | Savings | Typical Value |
|--------------|---------|---------------|
| Resume preprocessing | 40-60% | 250→100 tokens |
| Job description prep | 30-50% | 375→150 tokens |
| Keyword caching | 10-20% | 20% of analyses |
| LLM prompt optimization | 30-50% | 600→250 tokens |
| **Total Combined** | **50-70%** | **2000→600 tokens** |

---

## Best Practices

1. **Always validate output**: Optimization shouldn't reduce quality
2. **Monitor cache hit rate**: Adjust retention based on traffic
3. **Profile locally**: Measure exact savings in your environment
4. **Gradual rollout**: Test on subset before full deployment
5. **Log metrics**: Track tokens, costs, and quality metrics

---

## Common Pitfalls to Avoid

❌ **Removing too much context**
- Don't strip all dates (some are contextual)
- Keep recent experience more verbose than old

❌ **Over-aggressive deduplication**
- Some repetition is intentional (emphasis)
- Only remove exact duplicates

❌ **Losing semantic meaning**
- Don't abbreviate job descriptions too much
- Keep technical keywords intact

✅ **Instead**:
- Test optimization on real resumes
- Measure ATS score before/after
- Keep quality metrics high

---

## Further Optimizations (Advanced)

### 1. Batch Processing
```python
# Process multiple resumes against same job in one batch
# Reduces per-analysis overhead

results = pipeline.batch_analyze_resumes(
    job_description=job,
    resumes=[resume1, resume2, resume3],
    batch_size=3
)
```

### 2. Incremental Updates
```python
# If candidate updates only one section, re-analyze only that section
# Saves ~80% of tokens

pipeline.update_section(
    resume_id=resume_id,
    section='experience',
    updated_text=new_experience_text
)
```

### 3. Smart Tokenization
```python
# Use actual tokenizer for precise estimates
from tiktoken import encoding_for_model

enc = encoding_for_model("gpt-4")
actual_tokens = len(enc.encode(text))
```

---

## Summary

By implementing these optimizations:

1. **Minimize data sent to LLM** (60% reduction through preprocessing)
2. **Clean inputs before processing** (removes noise, improves quality)
3. **Extract only relevant sections** (focus on what matters)
4. **Avoid repeated data** (caching, deduplication)
5. **Optimize prompts** (structured, concise)

**Result**: 50-70% token usage reduction while maintaining or improving analysis quality.

**Implementation Time**: 2-4 hours  
**Maintenance**: Minimal (monitoring only)  
**ROI**: Quick return for high-volume usage (1,000+ analyses/month)

