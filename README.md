# Bright Blog API

A modern, secure FastAPI application for blog management with authentication.

## Project Structure

```
bright/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application factory and entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # API-level dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py       # API router (includes all v1 routers)
│   │       └── endpoints/
│   │       |   ├── __init__.py
│   │       |   ├── auth.py  # Authentication endpoints
│   │       |   ├── users.py # User management endpoints
│   │       |   └── posts.py # Blog post endpoints (placeholder)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Application settings (pydantic-settings)
│   │   ├── security.py      # Password hashing, JWT token handling
│   │   └── database.py      # Database setup and session management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   └── post.py          # Post model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── shared.py        # Shared schemas (PostBase, etc.)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py      # Auth-related schemas (LoginRequest)
│   │       ├── user.py      # User-related schemas
│   │       └── post.py      # Post-related schemas
│   └── services/
│       ├── __init__.py
│       ├── auth_service.py  # Authentication business logic
│   │   ├── user_service.py  # User business logic (placeholder)
│   │   ├── post_service.py  # Post business logic (placeholder)
│   │   └── security_service.py # Security utilities (password hashing, JWT)
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── api/
│   │   └── v1/
│   │       └── test_auth.py
│   ├── services/
│   │   └── test_auth_service.py
│   └── db/
│       └── test_repositories.py
├── alembic/                 # Database migrations
├── .env                     # Environment variables (local development)
├── .env.example             # Template for environment variables
├── Dockerfile               # Docker container definition
├── pyproject.toml           # Project dependencies and metadata
└── README.md                # This file
```

## Key Features

- **Modular Architecture**: Separation of concerns with clear layer boundaries
- **API Versioning**: Ready for versioned API endpoints (/api/v1/)
- **Environment Configuration**: All configuration via environment variables
- **Security-Focused**:
  - Password hashing using industry-standard Argon2/Bcrypt via pwdlib
  - JWT-based authentication with configurable expiration
  - HttpOnly cookies with XSS/CSRF protection
  - Environment-controlled secure flags for production deployment
- **Type Safety**: Full type hints throughout
- **Production Ready**: Structured for easy deployment with Docker/Gunicorn

## Getting Started

### Prerequisites

- Python 3.13+
- UV package manager (or pip)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd bright

# Create virtual environment (if not using uv)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .\.venv\Scripts\activate   # Windows

# Install dependencies
uv sync  # or: pip install -e .

# Set up environment variables
cp .env.example .env
# Edit .env with your local development values
```

### Running the Application

#### Development Mode

```bash
python main.py
# Or with explicit environment variables:
HOST=127.0.0.1 PORT=8000 RELOAD=true python main.py
```

#### Production Mode

```bash
# Using Gunicorn with Uvicorn workers
gunicorn app.main:app \
  -k uvicorn.workers.UvicornWorker \
  -w 4 \
  -b 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

#### Using Docker

```bash
docker build -t bright:latest .
docker run -p 8000:8000 \
  -e SECRET_KEY=$(openssl rand -hex 32) \
  -e DATABASE_URL="postgresql://user:pass@host:port/db" \
  -e COOKIE_SECURE="true" \
  bright:latest
```

## API Documentation

Once the application is running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

See `.env.example` for all available configuration options:

- `SECRET_KEY`: Secret key for JWT signing (required)
- `DATABASE_URL`: Database connection string (required)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `COOKIE_SECURE`: Whether cookies should be secure (default: false)
- `HOST`: Server host (default: 127.0.0.1)
- `PORT`: Server port (default: 8000)
- `RELOAD`: Enable auto-reload (default: false)

## Testing

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test suite
pytest tests/test_auth.py -v
```

## Database Migrations

This project uses Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Show migration history
alembic history
```
