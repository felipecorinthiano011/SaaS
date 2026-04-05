# Backend API Endpoints

## Authentication

### Register User
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}

Response: 200 OK
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Login User
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}

Response: 200 OK
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## Resume Management

### Upload Resume
```
POST /api/resume/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

Form data:
- file: (PDF/DOCX file)
- extractedText: (plain text extracted from file)

Response: 200 OK
{
  "id": 1,
  "fileName": "my-resume.pdf",
  "userEmail": "user@example.com",
  "uploadedAt": "2026-04-05T10:30:00Z",
  "message": "Resume uploaded successfully"
}
```

### List User Resumes
```
GET /api/resume
Authorization: Bearer {token}

Response: 200 OK
[
  {
    "id": 1,
    "fileName": "my-resume.pdf",
    "userEmail": "user@example.com",
    "extractedText": "...",
    "uploadedAt": "2026-04-05T10:30:00Z"
  }
]
```

### Get Resume Details
```
GET /api/resume/{id}
Authorization: Bearer {token}

Response: 200 OK
{
  "id": 1,
  "fileName": "my-resume.pdf",
  "userEmail": "user@example.com",
  "extractedText": "...",
  "uploadedAt": "2026-04-05T10:30:00Z"
}
```

---

## Job Analysis

### Analyze Job Description vs Resume
```
POST /api/job/analyze
Authorization: Bearer {token}
Content-Type: application/json

{
  "jobDescription": "Looking for Senior Java Developer with Spring Boot...",
  "resumeText": "I am a Java developer with 5 years of experience...",
  "resumeId": 1
}

Response: 200 OK
{
  "id": 1,
  "resumeId": 1,
  "atsScore": 78,
  "extractedKeywords": ["Java", "Spring Boot", "PostgreSQL", "REST API", "Microservices"],
  "optimizedResume": "I am a Java developer with 5 years of experience...\n\nSuggested ATS keyword enhancements:\n- Kubernetes\n- Docker\n- CI/CD",
  "gapSummary": "Consider incorporating these missing keywords where accurate and truthful: Kubernetes, Docker, CI/CD, AWS, Terraform",
  "createdAt": "2026-04-05T10:35:00Z"
}
```

### Get Analysis Results
```
GET /api/job/{id}
Authorization: Bearer {token}

Response: 200 OK
{
  "id": 1,
  "resumeId": 1,
  "atsScore": 78,
  "extractedKeywords": ["Java", "Spring Boot", "PostgreSQL", "REST API", "Microservices"],
  "optimizedResume": "...",
  "gapSummary": "...",
  "createdAt": "2026-04-05T10:35:00Z"
}
```

### List User's Analyses
```
GET /api/job
Authorization: Bearer {token}

Response: 200 OK
[
  {
    "id": 1,
    "resumeId": 1,
    "atsScore": 78,
    "extractedKeywords": [...],
    "optimizedResume": "...",
    "gapSummary": "...",
    "createdAt": "2026-04-05T10:35:00Z"
  }
]
```

---

## Health Check

```
GET /api/health

Response: 200 OK
{
  "status": "ok"
}
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK` - Success
- `400 Bad Request` - Validation failed
- `401 Unauthorized` - Missing or invalid JWT token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

Error response format:
```json
{
  "timestamp": "2026-04-05T10:35:00Z",
  "message": "Error description",
  "errors": [
    {
      "field": "email",
      "message": "Email is required"
    }
  ]
}
```

