# Backend (Spring Boot)

## Purpose

REST API for auth, analysis orchestration, and persistence.

## Clean architecture slices

- `common/` cross-cutting configuration, security, exception handling
- `modules/auth/` authentication feature
- `modules/analysis/` resume analysis feature and AI service integration

## Run locally

```powershell
cd backend
mvn spring-boot:run
```

## API endpoints (starter)

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/health`
- `POST /api/analysis` (JWT required)
- `GET /api/analysis` (JWT required)

