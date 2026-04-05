# Backend (Spring Boot)

## Purpose

REST API for auth, resume management, and job analysis orchestration.

## Clean architecture slices

- `common/` cross-cutting configuration, security, exception handling
- `modules/auth/` authentication module
- `modules/resume/` resume upload and storage module
- `modules/analysis/` job analysis and AI service integration

## Module Structure

Each module follows clean architecture:
```
modules/{name}/
├── api/           # Controllers (HTTP endpoints)
├── application/   # DTOs, services
├── domain/        # Entities
└── infra/         # Repositories (JPA)
```

## Run locally

```powershell
cd backend
mvn spring-boot:run
```

## API Endpoints

Full endpoint documentation: [API_ENDPOINTS.md](API_ENDPOINTS.md)

**Authentication:**
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Login

**Resume Management:**
- `POST /api/resume/upload` - Upload resume file
- `GET /api/resume` - List user resumes
- `GET /api/resume/{id}` - Get resume details

**Job Analysis:**
- `POST /api/job/analyze` - Analyze job description vs resume
- `GET /api/job` - List analyses
- `GET /api/job/{id}` - Get analysis result

**Health:**
- `GET /api/health` - Service health check

## Database

PostgreSQL with Hibernate auto-schema creation (`ddl-auto: update`).

**Key tables:**
- `users` - User accounts
- `resumes` - Uploaded resume files
- `resume_analyses` - Analysis results linking resumes to job analyses
