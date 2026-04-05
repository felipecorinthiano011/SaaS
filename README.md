# LinkedIn Resume Optimizer SaaS Monorepo

This repository contains a scalable, clean-architecture starter for a SaaS that analyzes LinkedIn job descriptions and adapts resumes using AI.

## Services

- `frontend/` - Angular + TailwindCSS client (deployable to Vercel)
- `backend/` - Spring Boot REST API with JWT auth and PostgreSQL
- `ai-service/` - FastAPI microservice for ATS analysis and resume optimization
- `docker/` - Local container orchestration and Dockerfiles

## High-level flow

1. User signs up and logs in (`backend` JWT issuance).
2. User submits a LinkedIn job description and uploads resume file.
3. `backend` stores metadata and forwards processing request to `ai-service`.
4. `ai-service` extracts keywords, parses resume, computes score, and returns optimized content.
5. `backend` persists analysis and exposes downloadable optimized output.

## Local quick start

Prerequisites (typical): Node 20+, Java 21, Maven 3.9+, Python 3.11+, Docker.

```powershell
# From repo root
cd docker
docker compose up --build
```

Then open:
- Frontend: http://localhost:4200
- Backend: http://localhost:8080/api/health
- AI service: http://localhost:8000/health

## Deployment notes

- Vercel: deploy `frontend/` using build command `npm run build` and output `dist/frontend/browser`.
- Railway: deploy `backend/` and `ai-service/` as separate services using included Dockerfiles.

## Next implementation milestones

- Replace placeholder AI logic with real PDF/DOCX parsing and LLM prompts.
- Add resume file storage (S3-compatible) and signed download URLs.
- Add refresh token flow and role-based authorization.
- Add observability (OpenTelemetry, structured logs, tracing IDs).

## CI/CD

### GitHub Actions

Push to your GitHub repository. Actions will automatically:
- Test Python AI service (`pytest`)
- Build Angular frontend (`ng build`)
- Test Spring Boot backend (`mvn test`)

See `.github/workflows/build-test.yml` for details.

### GitLab CI

Push to your GitLab instance. Pipelines will run tests for all services.

See `.gitlab-ci.yml` for details.

## Remote Repository Setup

See `DEPLOYMENT_REMOTE.md` for step-by-step instructions on connecting to GitHub, GitLab, or self-hosted Git.
