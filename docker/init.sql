-- Initialize database for Resume Optimizer
-- This script is run automatically when the container starts
-- NOTE: Tables are managed by Spring Boot / Hibernate (ddl-auto: update)
-- This file only handles extensions and permission grants.

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Connect to the resume_optimizer database
\c resume_optimizer

-- Grant all privileges on public schema to resume_user
GRANT ALL PRIVILEGES ON SCHEMA public TO resume_user;

-- Set default privileges so resume_user owns all future tables/sequences
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO resume_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO resume_user;

SELECT 'Database initialized successfully' AS status;

