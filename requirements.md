# FastAPI Authentication Tutorial - Dependencies

This document lists all Python packages that will be installed for this tutorial.

## Core Dependencies

### Web Framework
| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | latest | FastAPI web framework |
| uvicorn | latest | ASGI server to run FastAPI |
| python-multipart | latest | Form data parsing for OAuth2 |

### Database
| Package | Version | Purpose |
|---------|---------|---------|
| sqlalchemy | 2.x | SQLAlchemy ORM (async support) |
| asyncpg | latest | Async PostgreSQL driver |
| psycopg2-binary | latest | PostgreSQL driver (fallback) |

### Authentication & Security
| Package | Version | Purpose |
|---------|---------|---------|
| python-jose[cryptography] | latest | JWT token creation/validation |
| pwdlib | latest | Password hashing (Argon2 algorithm) |
| passlib | latest | Password hashing utilities |

### Configuration
| Package | Version | Purpose |
|---------|---------|---------|
| pydantic | 2.x | Data validation and settings |
| pydantic-settings | latest | Environment variable handling |

---

## Development Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | latest | Testing framework |
| pytest-asyncio | latest | Async test support |
| httpx | latest | HTTP client for testing |
| pytest-cov | latest | Test coverage reporting |

---

## Installation Command

```bash
# Install all dependencies
pip install fastapi uvicorn sqlalchemy asyncpg psycopg2-binary \
    "python-jose[cryptography]" pwdlib passlib \
    pydantic pydantic-settings \
    pytest pytest-asyncio httpx pytest-cov
```

---

## Project Structure After Installation

```
venv/lib/pythonX.X/site-packages/
├── fastapi/
├── uvicorn/
├── sqlalchemy/
├── asyncpg/
├── jose/
├── pwdlib/
├── passlib/
├── pydantic/
├── pytest/
└── ... (other dependencies)
```

---

## Notes

- **python-jose[cryptography]** includes cryptography library needed for JWT signing
- **pwdlib** automatically uses Argon2 (recommended by FastAPI docs)
- **asyncpg** is the async PostgreSQL driver - much faster than sync psycopg2 for web apps
- All packages are from PyPI - no special installation required