# Docker Setup & Deployment Guide

## Complete Guide for ResumeMatcher SaaS

**Date**: April 5, 2026  
**Status**: Production Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Service Details](#service-details)
5. [Configuration](#configuration)
6. [Common Tasks](#common-tasks)
7. [Troubleshooting](#troubleshooting)
8. [Production Deployment](#production-deployment)

---

## Overview

The ResumeMatcher SaaS consists of 4 containerized services:

| Service | Port | Technology | Purpose |
|---------|------|-----------|---------|
| **Frontend** | 4200 | Angular + TailwindCSS | User interface |
| **Backend** | 8080 | Spring Boot 3 | REST API |
| **AI Service** | 8000 | FastAPI (Python) | NLP/AI analysis |
| **Database** | 5432 | PostgreSQL 16 | Data persistence |

**Architecture**:
```
┌─────────────────────────────────────────────────────┐
│                    Frontend (4200)                   │
│                   Angular + TailwindCSS              │
└────────────────────────┬────────────────────────────┘
                         │ HTTP/REST
┌────────────────────────▼────────────────────────────┐
│              Backend API (8080)                      │
│            Spring Boot 3 + Spring Data               │
└────────────┬──────────────────────────┬──────────────┘
             │ JDBC/PostgreSQL          │ HTTP/REST
┌────────────▼──────────────────┐ ┌────▼──────────────┐
│    Database (5432)             │ │ AI Service (8000) │
│   PostgreSQL 16 Alpine         │ │  FastAPI + Python │
└────────────────────────────────┘ └───────────────────┘
```

---

## Prerequisites

### System Requirements

- **CPU**: 2+ cores (4+ recommended)
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 20GB free space
- **OS**: Windows 10+, macOS, or Linux

### Software Requirements

- **Docker Desktop**: v4.0+ (includes Docker & Docker Compose)
- **Git**: For cloning repository
- **cURL**: For testing endpoints (optional)
- **OpenAI API Key**: For LLM features (optional but recommended)

### Installation

**Windows/Mac**:
```bash
# Download and install Docker Desktop from:
https://www.docker.com/products/docker-desktop
```

**Linux** (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose-plugin
sudo usermod -aG docker $USER
```

**Verify Installation**:
```bash
docker --version
docker compose version
```

---

## Quick Start

### 1. Clone Repository

```bash
cd C:\Projects\Saas
```

### 2. Create Environment File

```bash
# Windows PowerShell
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### 3. Edit Configuration

Update `.env` with your values, especially:

```env
# Required for AI features
OPENAI_API_KEY=sk-your-key-here

# Change default passwords in production
POSTGRES_PASSWORD=your-secure-password
JWT_SECRET=your-secret-key-here
```

### 4. Start Services

```bash
# Windows PowerShell
cd docker
.\docker-manager.ps1

# Linux/Mac
cd docker
chmod +x docker-manager.sh
./docker-manager.sh
```

Or manually:

```bash
docker compose up --build
```

### 5. Access Services

Once running:

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8080
- **AI Service**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## Service Details

### Frontend (Port 4200)

**Technology**: Angular + TailwindCSS  
**Build**: Multi-stage Docker build  
**Health Check**: HTTP GET `/`

**Key Features**:
- User authentication
- Resume upload
- Job description analysis
- Results visualization

**Dependencies**:
- Backend API (8080)

**Environment Variables**:
```yaml
API_URL: http://backend:8080
```

### Backend API (Port 8080)

**Technology**: Spring Boot 3 + Spring Data JPA  
**Build**: Maven multi-stage build  
**Health Check**: HTTP GET `/actuator/health`

**Key Endpoints**:
```
POST   /auth/register              # Register user
POST   /auth/login                 # Login
POST   /resume/upload              # Upload resume
POST   /job/analyze                # Analyze job description
GET    /analysis/{id}              # Get analysis results
GET    /actuator/health            # Health check
```

**Environment Variables**:
```yaml
SPRING_DATASOURCE_URL: jdbc:postgresql://postgres:5432/resume_optimizer
SPRING_DATASOURCE_USERNAME: resume_user
SPRING_DATASOURCE_PASSWORD: resume_password
JWT_SECRET: your-secret-key
JWT_EXPIRATION_SECONDS: 3600
AI_SERVICE_BASE_URL: http://ai-service:8000
```

**Dependencies**:
- PostgreSQL (5432)
- AI Service (8000)

### AI Service (Port 8000)

**Technology**: FastAPI + Python 3.11  
**Build**: Single-stage Docker build  
**Health Check**: HTTP GET `/api/v1/keywords/health`

**Key Endpoints**:
```
POST   /api/v1/keywords/extract              # Extract keywords
POST   /api/v1/resume/optimize               # Optimize resume
GET    /api/v1/keywords/health               # Health check
GET    /docs                                  # API documentation
```

**Features**:
- LangChain integration
- OpenAI API integration
- ATS keyword extraction
- Resume optimization
- Resume scoring

**Environment Variables**:
```yaml
OPENAI_API_KEY: sk-your-api-key
AI_LLM_NAME: gpt-4o-mini
AI_DEBUG: false
AI_MINIMUM_KEYWORD_COUNT: 15
```

**Dependencies**:
- OpenAI API (external)

### Database (Port 5432)

**Technology**: PostgreSQL 16 Alpine  
**Health Check**: `pg_isready -U resume_user`

**Configuration**:
```yaml
POSTGRES_DB: resume_optimizer
POSTGRES_USER: resume_user
POSTGRES_PASSWORD: resume_password
```

**Volumes**:
- `postgres_data`: Persistent database storage

**Backup & Recovery**:
```bash
# Backup database
docker compose exec postgres pg_dump -U resume_user resume_optimizer > backup.sql

# Restore database
docker compose exec -T postgres psql -U resume_user resume_optimizer < backup.sql
```

---

## Configuration

### Environment Variables

All configuration is managed through `.env` file:

```env
# DATABASE
POSTGRES_DB=resume_optimizer
POSTGRES_USER=resume_user
POSTGRES_PASSWORD=resume_password

# BACKEND - JWT
JWT_SECRET=your-32-char-secret-key-here
JWT_EXPIRATION_SECONDS=3600

# BACKEND - DATABASE
SPRING_DATASOURCE_URL=jdbc:postgresql://postgres:5432/resume_optimizer
SPRING_DATASOURCE_USERNAME=resume_user
SPRING_DATASOURCE_PASSWORD=resume_password

# BACKEND - AI SERVICE
AI_SERVICE_BASE_URL=http://ai-service:8000

# AI SERVICE
OPENAI_API_KEY=sk-your-key-here
AI_LLM_NAME=gpt-4o-mini
AI_DEBUG=false
AI_MINIMUM_KEYWORD_COUNT=15
```

### Service Dependencies

```
frontend  →  backend  →  ai-service
              ↓
            postgres
```

Docker Compose ensures proper startup order:

```yaml
depends_on:
  postgres:
    condition: service_healthy
  ai-service:
    condition: service_healthy
```

---

## Common Tasks

### View Logs

```bash
# All services
docker compose logs

# Specific service
docker compose logs backend
docker compose logs ai-service
docker compose logs postgres

# Follow logs (live)
docker compose logs -f backend

# Last 100 lines
docker compose logs --tail 100

# With timestamps
docker compose logs -t
```

### Stop Services

```bash
# Stop all services (keep volumes)
docker compose down

# Stop and remove volumes
docker compose down -v

# Stop specific service
docker compose stop backend

# Stop all services
docker compose stop
```

### Restart Services

```bash
# Restart all
docker compose restart

# Restart specific service
docker compose restart ai-service

# Rebuild and restart
docker compose up -d --build
```

### Access Service Directly

```bash
# Execute command in container
docker compose exec backend ls -la

# Open bash shell
docker compose exec backend bash

# Run database query
docker compose exec postgres psql -U resume_user -d resume_optimizer

# View service info
docker compose exec backend java -version
docker compose exec ai-service python --version
```

### Monitor Resources

```bash
# View CPU/Memory usage
docker stats

# View disk usage
docker system df

# List all images
docker images

# List volumes
docker volume ls
```

### Debugging

```bash
# Check if port is in use (Windows)
netstat -ano | findstr :8080

# Check if port is in use (Linux/Mac)
lsof -i :8080

# View network
docker network ls
docker network inspect docker_saas-network

# View containers
docker compose ps
docker ps -a

# Rebuild without cache
docker compose build --no-cache
```

---

## Troubleshooting

### Services Won't Start

**Problem**: Docker services fail to start

**Solution**:
```bash
# Check Docker is running
docker ps

# Check logs
docker compose logs

# Rebuild images
docker compose build --no-cache

# Remove orphaned containers
docker compose down -v
docker system prune -a

# Restart Docker
# Windows: Restart Docker Desktop
# Linux: sudo systemctl restart docker
```

### Database Connection Failed

**Problem**: Backend can't connect to PostgreSQL

**Solution**:
```bash
# Check PostgreSQL is running
docker compose ps postgres

# Test connection
docker compose exec postgres psql -U resume_user -d resume_optimizer

# Check database exists
docker compose exec postgres psql -U resume_user -l

# View PostgreSQL logs
docker compose logs postgres

# Verify environment variables
docker compose config | grep POSTGRES
```

### Port Already in Use

**Problem**: Port 8080/8000/5432 already in use

**Solution**:
```bash
# Windows: Find process using port
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Linux/Mac: Find process using port
lsof -i :8080
kill -9 <PID>

# Or change ports in docker-compose.yml
# Then start services
docker compose up
```

### AI Service Not Responding

**Problem**: AI Service returns errors

**Solution**:
```bash
# Check service is running
docker compose ps ai-service

# Test endpoint
curl http://localhost:8000/api/v1/keywords/health

# Check logs
docker compose logs ai-service

# Verify OpenAI API key
docker compose config | grep OPENAI

# Check API key is valid (in AI service logs)
```

### Memory Issues

**Problem**: Services crash due to memory

**Solution**:
```bash
# Check Docker memory allocation
docker system df

# Increase Docker memory (Docker Desktop settings)
# Windows/Mac: Docker Desktop → Settings → Resources

# Or add resource limits in docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 1G
```

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] Change all default passwords
- [ ] Generate new JWT secret: `openssl rand -base64 32`
- [ ] Set OPENAI_API_KEY in environment
- [ ] Use managed PostgreSQL (AWS RDS, Google Cloud SQL, etc.)
- [ ] Enable HTTPS/TLS
- [ ] Set up logging aggregation
- [ ] Configure monitoring and alerts
- [ ] Set up CI/CD pipeline
- [ ] Plan for backups and disaster recovery
- [ ] Review security settings

### Generate Secure JWT Secret

```bash
# Windows PowerShell
$bytes = [byte[]]::new(32)
[Security.Cryptography.RNGCryptoServiceProvider]::new().GetBytes($bytes)
[Convert]::ToBase64String($bytes)

# Linux/Mac
openssl rand -base64 32
```

### Deployment to AWS ECS

```bash
# 1. Create ECR repositories
aws ecr create-repository --repository-name resume-matcher/backend
aws ecr create-repository --repository-name resume-matcher/ai-service
aws ecr create-repository --repository-name resume-matcher/frontend

# 2. Push images
docker tag resume-matcher:backend <account>.dkr.ecr.us-east-1.amazonaws.com/resume-matcher/backend:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/resume-matcher/backend:latest

# 3. Create ECS cluster, services, and tasks
# (Use AWS CLI or AWS Console)

# 4. Set environment variables in ECS task definition
# Use AWS Secrets Manager for sensitive data
```

### Deployment to Google Cloud Run

```bash
# 1. Build and push to Artifact Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/resume-matcher-backend

# 2. Deploy to Cloud Run
gcloud run deploy resume-matcher-backend \
  --image gcr.io/PROJECT_ID/resume-matcher-backend \
  --platform managed \
  --memory 1Gi \
  --set-env-vars "OPENAI_API_KEY=$OPENAI_API_KEY" \
  --allow-unauthenticated

# 3. Set up Cloud SQL proxy for PostgreSQL
```

### Kubernetes Deployment

```bash
# 1. Build and push images to registry

# 2. Create Kubernetes manifests
kubectl apply -f kubernetes/

# 3. Deploy services
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/ai-service-deployment.yaml
kubectl apply -f kubernetes/postgres-deployment.yaml

# 4. Monitor deployment
kubectl get pods
kubectl logs deployment/resume-matcher-backend
```

---

## Performance Optimization

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_resume_user_id ON resumes(user_id);
CREATE INDEX idx_analysis_user_id ON job_analyses(user_id);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM job_analyses WHERE user_id = 1;

-- Vacuum database
VACUUM ANALYZE;
```

### Caching Configuration

```yaml
# Add Redis for caching (optional)
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
```

### Resource Limits

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

---

## Monitoring & Logging

### ELK Stack Integration (Optional)

```yaml
# Add Elasticsearch, Logstash, Kibana
elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
  
logstash:
  image: docker.elastic.co/logstash/logstash:8.0.0
  
kibana:
  image: docker.elastic.co/kibana/kibana:8.0.0
```

### Prometheus Metrics (Optional)

```yaml
# Add Prometheus for metrics
prometheus:
  image: prom/prometheus
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

---

## Security Best Practices

1. **Never commit .env file**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Use strong passwords**
   ```bash
   # Generate strong password
   openssl rand -base64 16
   ```

3. **Keep images updated**
   ```bash
   docker pull postgres:16
   docker compose build --no-cache
   ```

4. **Use private networks**
   ```yaml
   networks:
     saas-network:
       driver: bridge
   ```

5. **Implement rate limiting**
   ```yaml
   # In Spring Boot application.yml
   spring:
     cloud:
       gateway:
         routes:
           - id: rate_limit
             predicates:
               - Path=/**
             filters:
               - name: RequestRateLimiter
   ```

---

## Support & Resources

- Docker Docs: https://docs.docker.com/
- Spring Boot Deployment: https://spring.io/guides/topicals/spring-boot-docker/
- FastAPI Docker: https://fastapi.tiangolo.com/deployment/docker/
- PostgreSQL Docs: https://www.postgresql.org/docs/

---

**Last Updated**: April 5, 2026  
**Status**: Production Ready

