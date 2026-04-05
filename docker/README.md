# Docker Setup Guide

## Overview

This directory contains Docker configurations for running the complete ResumeMatcher SaaS platform locally. The setup includes:

- **PostgreSQL Database** - Port 5432
- **Python FastAPI AI Service** - Port 8000
- **Spring Boot Backend API** - Port 8080
- **Angular Frontend** - Port 4200

## Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0+
- At least 4GB RAM available
- OpenAI API key (optional, for LLM features)

## Quick Start

### 1. Clone Repository

```bash
cd C:\Projects\Saas
```

### 2. Create Environment File

```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your values
# Important: Update OPENAI_API_KEY if using LLM features
```

### 3. Start All Services

```bash
# Navigate to docker directory
cd docker

# Build and start all services
docker compose up --build

# Or run in background
docker compose up -d --build

# View logs
docker compose logs -f
```

### 4. Verify Services

Once running, test each service:

```bash
# Frontend
open http://localhost:4200

# Backend API
curl http://localhost:8080/actuator/health

# AI Service
curl http://localhost:8000/api/v1/keywords/health

# Database (using psql)
psql -h localhost -U resume_user -d resume_optimizer
```

## Services Detail

### PostgreSQL Database

**Configuration**:
- Port: 5432
- Database: resume_optimizer
- User: resume_user
- Password: resume_password (change in production)

**Environment Variables**:
```yaml
POSTGRES_DB: resume_optimizer
POSTGRES_USER: resume_user
POSTGRES_PASSWORD: resume_password
```

**Volumes**:
- `postgres_data`: Persistent database storage

**Health Check**:
- Command: `pg_isready -U resume_user`
- Interval: 10 seconds
- Timeout: 5 seconds

### Python FastAPI AI Service

**Configuration**:
- Port: 8000
- Base URL: http://ai-service:8000
- Framework: FastAPI + Uvicorn

**Environment Variables**:
```yaml
OPENAI_API_KEY: Your OpenAI API key
AI_LLM_NAME: gpt-4o-mini
AI_DEBUG: false
AI_MINIMUM_KEYWORD_COUNT: 15
```

**Key Endpoints**:
- `POST /api/v1/keywords/extract` - Extract keywords
- `POST /api/v1/resume/optimize` - Optimize resume
- `GET /api/v1/keywords/health` - Health check

**Health Check**:
- Command: `curl http://localhost:8000/api/v1/keywords/health`
- Interval: 30 seconds
- Timeout: 10 seconds

### Spring Boot Backend

**Configuration**:
- Port: 8080
- Framework: Spring Boot 3.0+
- Database: PostgreSQL (via JDBC)

**Environment Variables**:
```yaml
SPRING_DATASOURCE_URL: jdbc:postgresql://postgres:5432/resume_optimizer
SPRING_DATASOURCE_USERNAME: resume_user
SPRING_DATASOURCE_PASSWORD: resume_password
JWT_SECRET: Your JWT secret key
JWT_EXPIRATION_SECONDS: 3600
AI_SERVICE_BASE_URL: http://ai-service:8000
```

**Key Endpoints**:
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /resume/upload` - Upload resume
- `POST /job/analyze` - Analyze job description
- `GET /actuator/health` - Health check

**Health Check**:
- Command: `curl http://localhost:8080/actuator/health`
- Interval: 30 seconds
- Timeout: 10 seconds

### Angular Frontend

**Configuration**:
- Port: 4200
- Framework: Angular with TailwindCSS
- Build: Multi-stage Docker build

**Environment Variables**:
```yaml
API_URL: http://backend:8080
```

**Health Check**:
- Command: `curl http://localhost:80/`
- Interval: 30 seconds
- Timeout: 10 seconds

## Docker Commands

### Basic Commands

```bash
# Start services
docker compose up

# Start in background
docker compose up -d

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v

# View logs
docker compose logs

# View specific service logs
docker compose logs backend

# Follow logs (tail)
docker compose logs -f ai-service
```

### Rebuild Commands

```bash
# Rebuild all images
docker compose build

# Rebuild specific service
docker compose build backend

# Rebuild without cache
docker compose build --no-cache

# Rebuild and start
docker compose up --build
```

### Container Commands

```bash
# List running containers
docker compose ps

# Execute command in container
docker compose exec backend ls -la

# Run bash in container
docker compose exec backend bash

# Check service status
docker compose ps postgres

# View container resource usage
docker stats
```

## Environment Configuration

### Configuration Hierarchy

1. `.env` file (local overrides)
2. `docker-compose.yml` defaults
3. Service default values

### Key Environment Variables

```yaml
# Database
POSTGRES_DB=resume_optimizer           # Database name
POSTGRES_USER=resume_user              # DB user
POSTGRES_PASSWORD=resume_password      # DB password

# Backend - JWT
JWT_SECRET=your-secret-key-here        # Min 32 chars
JWT_EXPIRATION_SECONDS=3600            # Token TTL

# Backend - Database Connection
SPRING_DATASOURCE_URL=jdbc:postgresql://postgres:5432/resume_optimizer
SPRING_DATASOURCE_USERNAME=resume_user
SPRING_DATASOURCE_PASSWORD=resume_password

# Backend - AI Service
AI_SERVICE_BASE_URL=http://ai-service:8000

# AI Service - OpenAI
OPENAI_API_KEY=sk-your-key-here        # Required for LLM
AI_LLM_NAME=gpt-4o-mini                # LLM model
AI_DEBUG=false                          # Debug mode
```

## Production Deployment

### Pre-Deployment Checklist

- [ ] Change all default passwords
- [ ] Generate new JWT secret: `openssl rand -base64 32`
- [ ] Configure OPENAI_API_KEY in secure environment
- [ ] Use managed PostgreSQL service (AWS RDS, Google Cloud SQL, etc.)
- [ ] Enable HTTPS for all services
- [ ] Configure proper logging
- [ ] Set up monitoring and alerts
- [ ] Review security settings

### Production Environment Variables

```yaml
# Use environment-specific values
POSTGRES_DB=resume_optimizer_prod
POSTGRES_USER=prod_user
POSTGRES_PASSWORD=strong-random-password-here

# Use secure secret management
JWT_SECRET=use-aws-secrets-manager
OPENAI_API_KEY=use-aws-secrets-manager

# Disable debug mode
AI_DEBUG=false

# Use external database
SPRING_DATASOURCE_URL=jdbc:postgresql://prod-db.region.amazonaws.com:5432/resume_optimizer
```

### Deployment Platforms

**AWS ECS**:
- Use ECR for image registry
- Use RDS for PostgreSQL
- Use Secrets Manager for sensitive data
- Use Application Load Balancer for routing

**Google Cloud Run**:
- Push images to Artifact Registry
- Use Cloud SQL for PostgreSQL
- Use Secret Manager
- Use Cloud Load Balancing

**Azure Container Instances**:
- Use Azure Container Registry
- Use Azure Database for PostgreSQL
- Use Key Vault for secrets
- Use Azure Load Balancer

## Troubleshooting

### Services Won't Start

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
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker compose ps postgres

# Test connection
docker compose exec postgres psql -U resume_user -d resume_optimizer

# Check database logs
docker compose logs postgres

# Verify environment variables
docker compose config | grep POSTGRES
```

### AI Service Not Responding

```bash
# Check service is running
docker compose ps ai-service

# Test endpoint
curl http://localhost:8000/api/v1/keywords/health

# Check logs
docker compose logs ai-service

# Verify OpenAI API key
docker compose config | grep OPENAI
```

### Backend API Issues

```bash
# Check service is running
docker compose ps backend

# Test endpoint
curl http://localhost:8080/actuator/health

# Check logs
docker compose logs backend

# Verify database connection
docker compose exec backend curl http://postgres:5432/
```

## Performance Optimization

### Memory Management

```yaml
# Limit service resources in docker-compose.yml
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

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_resume_user_id ON resumes(user_id);
CREATE INDEX idx_analysis_user_id ON job_analyses(user_id);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM job_analyses WHERE user_id = 1;
```

## Monitoring & Logging

### View Logs

```bash
# All services
docker compose logs

# Specific service
docker compose logs backend

# Last 100 lines
docker compose logs --tail 100

# Follow logs (live)
docker compose logs -f

# With timestamps
docker compose logs -t
```

### Performance Monitoring

```bash
# Monitor resource usage
docker stats

# Check service health
docker compose ps

# Inspect service configuration
docker compose config

# View running processes
docker compose top backend
```

## Security Best Practices

1. **Never commit .env file**
   - Keep sensitive data in environment only
   - Use `.gitignore` to exclude `.env`

2. **Change default credentials**
   - Database passwords
   - JWT secret
   - API keys

3. **Use secure protocols**
   - HTTPS in production
   - TLS for database connections

4. **Limit network access**
   - Use private networks
   - Restrict port exposure
   - Implement firewalls

5. **Regular updates**
   - Update base images
   - Patch dependencies
   - Security audits

## Links & Resources

- Docker Documentation: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- PostgreSQL Docker: https://hub.docker.com/_/postgres
- Spring Boot Docker: https://spring.io/guides/topicals/spring-boot-docker/
- FastAPI Docker: https://fastapi.tiangolo.com/deployment/docker/

## Support

For issues or questions:
- Check logs: `docker compose logs`
- Verify configuration: `docker compose config`
- Test services individually
- Check port conflicts: `netstat -an`
- Review Docker volumes: `docker volume ls`
