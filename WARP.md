# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a full-stack OAuth SaaS application implementing Google OAuth authentication flow with a React frontend and FastAPI backend. The architecture follows a clean separation of concerns with the OAuth logic handled entirely on the backend for security.

### Tech Stack
- **Frontend**: React, TypeScript, Vite
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose

## Project Setup

### Initial Setup
Ensure you have a proper .gitignore file in the root directory to prevent committing sensitive files:

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environments
.venv/
venv/
env/

# IDE / Editor specific
.vscode/
.idea/
*.swp

# Secrets
.env
*.env

# Frontend specific (we'll add more later)
frontend/node_modules/
frontend/dist/

# Test artifacts
.pytest_cache/
```

## Development Commands

### Environment Setup
```bash
# Start all services (backend, frontend, database)
docker-compose up -d

# Start development with live reload
docker-compose up --build

# Stop all services
docker-compose down
```

### Backend Development
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run FastAPI development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run database migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Run tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run tests with coverage
pytest --cov=app --cov-report=html
```

### Frontend Development
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint
```

## Architecture Overview

### Backend Structure (`/backend/app/`)
The FastAPI backend is organized into clear modules:

- **`auth/`**: OAuth authentication logic
  - Google OAuth flow implementation
  - JWT token management
  - Session handling
- **`users/`**: User management endpoints
  - User profile operations
  - User data schemas
- **`core/`**: Core application logic
  - Configuration management (environment variables)
  - Security utilities (JWT creation/validation)
- **`db/`**: Database layer
  - SQLAlchemy models
  - Database connection setup
- **`api/v1/`**: API versioning and routing
  - Combines all routers into versioned API

### OAuth Authentication Flow
1. Frontend requests Google login URL from `/api/v1/auth/login/google`
2. User redirects to Google OAuth
3. Google redirects to backend callback `/api/v1/auth/callback/google`
4. Backend exchanges code for tokens, creates user session
5. Backend sets HTTP-only JWT cookie and redirects to frontend
6. Frontend makes authenticated requests using the cookie

### Key API Endpoints
- `GET /api/v1/auth/login/google` - Get Google OAuth URL
- `GET /api/v1/auth/callback/google` - Handle OAuth callback
- `GET /api/v1/users/me` - Get current user profile
- `POST /api/v1/auth/logout` - Logout and clear session

## Database Management

### Alembic Migrations
- Configuration: `backend/alembic.ini`
- Migration scripts are auto-generated and stored in `backend/alembic/versions/`
- Always review auto-generated migrations before applying

### Models
- User model includes OAuth provider data
- Database connection uses SQLAlchemy with PostgreSQL

## Security Considerations

### Environment Variables
- Google OAuth Client ID/Secret stored in `.env`
- Database credentials managed via environment variables
- JWT secret keys for token signing

### Cookie Security
- HTTP-only cookies prevent XSS attacks
- Secure flag for HTTPS environments
- SameSite attribute for CSRF protection

## Testing Strategy

### Backend Tests (`/backend/tests/`)
- `test_auth.py`: OAuth flow testing
- `test_users.py`: User endpoint testing
- Use pytest with FastAPI test client
- Mock external OAuth provider calls

### Test Database
- Use separate test database configuration
- Reset database state between test runs

## Development Workflow

1. **Feature Development**:
   - Create feature branch from main
   - Implement backend API endpoints first
   - Add corresponding tests
   - Implement frontend integration
   - Test OAuth flow end-to-end

2. **Database Changes**:
   - Modify SQLAlchemy models
   - Generate migration: `alembic revision --autogenerate`
   - Review and edit migration if needed
   - Apply migration: `alembic upgrade head`

3. **Authentication Testing**:
   - Use Google OAuth sandbox/test environment
   - Test token refresh logic
   - Verify session management

## Production Considerations

### Docker Deployment
- Multi-stage Docker builds for optimization
- Environment-specific configurations
- Health checks for all services

### Security
- Rate limiting on auth endpoints
- CORS configuration for production domains
- SSL/TLS termination
- Secure cookie configuration

### Monitoring
- Log OAuth flows for debugging
- Monitor token refresh patterns
- Track user session metrics
