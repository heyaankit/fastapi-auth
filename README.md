# OTP-Based Authentication System

A FastAPI-based OTP authentication system for mobile-first applications.

## Features

- User registration with phone number
- OTP generation and verification (6 digits, 5 min expiry)
- Separate country code and phone number fields
- Login via phone + OTP (no password)
- JWT token-based authentication
- Protected routes
- Health check endpoint

## Tech Stack

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **SQLite** - Database
- **python-jose** - JWT tokens
- **pydantic** - Data validation

## Setup

### Clone and Install

```bash
git clone https://github.com/heyaankit/fastapi-auth.git
cd fastapi-auth
pip install -r requirements.txt
```

### Run the server

```bash
uvicorn main:app --reload
```

The API runs on `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### Reset Database (optional)

If you want a fresh database:
```bash
rm data/app.db
uvicorn main:app --reload
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/request-otp` | POST | Request OTP for registration |
| `/api/v1/auth/register` | POST | Verify OTP + create user |
| `/api/v1/auth/request-login-otp` | POST | Request OTP for login |
| `/api/v1/auth/login` | POST | Verify OTP + return JWT |
| `/api/v1/users/me` | GET | Get current user (protected) |
| `/health` | GET | Health check |

## Usage Example

### Registration (New User)

**1. Request OTP for registration**
```bash
curl -X POST http://localhost:8000/api/v1/auth/request-otp \
  -H "Content-Type: application/json" \
  -d '{"country_code": "+91", "phone": "9876543210"}'
```

**2. Get OTP from database**
```bash
sqlite3 "data/app.db" "SELECT code FROM otp WHERE phone='9876543210' ORDER BY created_at DESC LIMIT 1;"
```

**3. Register**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"country_code": "+91", "phone": "9876543210", "code": "YOUR_OTP", "name": "John Doe", "email": "john@example.com"}'
```

### Login (Returning User)

**1. Request Login OTP**
```bash
curl -X POST http://localhost:8000/api/v1/auth/request-login-otp \
  -H "Content-Type: application/json" \
  -d '{"country_code": "+91", "phone": "9876543210"}'
```

**2. Get OTP from database**
```bash
sqlite3 "data/app.db" "SELECT code FROM otp WHERE phone='9876543210' ORDER BY created_at DESC LIMIT 1;"
```

**3. Login**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"country_code": "+91", "phone": "9876543210", "code": "YOUR_OTP"}'
```

### Get Current User

```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Project Structure

```
.
├── main.py              # FastAPI app and routes
├── otp_app/
│   ├── config.py        # Settings
│   ├── database.py      # Database config
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   └── services/        # Business logic
├── data/                # SQLite database
└── .venv/               # Virtual environment
```

## Notes

- OTP is mock (generated and stored, not sent via SMS)
- OTP expires after 5 minutes
- JWT token expires after 30 minutes
- SQLite database at `./data/app.db`
- Country code and phone number are stored as separate fields