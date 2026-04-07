# FastAPI Authentication Tutorial

A beginner-friendly tutorial on implementing authentication and authorization in FastAPI with PostgreSQL.

## Features

- User registration with Argon2 password hashing
- JWT token-based login
- Protected routes with authentication
- Role-based access control (user/admin)
- Async SQLAlchemy with PostgreSQL

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL (running on localhost:5432)
- pip or poetry

### Installation

```bash
pip install -r requirements.txt
```

Create `.env` file:
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_auth
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=true
```

### Run the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## API Endpoints

### Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

Response:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Get Current User (Protected)
```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/auth/me
```

### Admin Only Route
```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/auth/admin/users
```

## Project Structure

```
.
├── main.py                 # FastAPI application entry point
├── config.py               # Settings configuration
├── app/
│   ├── api/v1/auth.py      # Auth endpoints
│   ├── auth/
│   │   ├── password.py     # Argon2 password hashing
│   │   ├── jwt.py          # JWT token utilities
│   │   └── dependencies.py # Auth dependencies
│   ├── db/database.py      # Database configuration
│   ├── models/user.py      # User SQLAlchemy model
│   └── schemas/user.py     # Pydantic schemas
├── tests/
│   └── test_auth.py        # Integration tests
└── docker-compose.yml      # PostgreSQL setup
```

## Key Concepts

### Password Hashing
Uses Argon2 (via pwdlib) - recommended by FastAPI for security:
```python
from app.auth.password import hash_password, verify_password

hashed = hash_password("mypassword")
is_valid = verify_password("mypassword", hashed)
```

### JWT Tokens
```python
from app.auth.jwt import create_access_token, decode_token

token = create_access_token(data={"sub": "user-id", "role": "user"})
payload = decode_token(token)
```

### Protected Routes
```python
from app.auth.dependencies import get_current_user

@app.get("/protected")
async def protected_route(user: User = Depends(get_current_user)):
    return {"user": user.email}
```

### Role-Based Access Control
```python
from app.auth.dependencies import require_role

@app.get("/admin/users")
async def admin_route(user: User = Depends(require_role("admin"))):
    return {"data": "admin only"}
```

## Testing

```bash
pytest tests/test_auth.py -v
```

## Security Notes

- Never hardcode secrets - use environment variables
- Passwords are hashed with Argon2 (not stored as plain text)
- JWT tokens expire after 30 minutes
- Regular users cannot access admin routes
- Error messages don't reveal if email exists (prevents enumeration)