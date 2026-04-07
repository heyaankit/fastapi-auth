import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "testuser@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "password" not in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@example.com", "password": "password123"},
    )
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@example.com", "password": "password456"},
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_register_short_password(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "short@example.com", "password": "short"},
    )
    assert response.status_code == 400
    assert "at least 8 characters" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "loginuser@example.com", "password": "password123"},
    )
    response = await client.post(
        "/api/v1/auth/token",
        data={"username": "loginuser@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "wrongpass@example.com", "password": "password123"},
    )
    response = await client.post(
        "/api/v1/auth/token",
        data={"username": "wrongpass@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/token",
        data={"username": "nonexistent@example.com", "password": "password123"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_route_without_token(client: AsyncClient):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_route_with_valid_token(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "protected@example.com", "password": "password123"},
    )
    login_response = await client.post(
        "/api/v1/auth/token",
        data={"username": "protected@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "protected@example.com"


@pytest.mark.asyncio
async def test_admin_route_blocked_for_regular_user(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "regular@example.com", "password": "password123"},
    )
    login_response = await client.post(
        "/api/v1/auth/token",
        data={"username": "regular@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/auth/admin/users",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_route_allowed_for_admin(client: AsyncClient):
    from sqlalchemy import select
    from app.db.database import async_session_maker
    from app.models.user import User
    from app.auth.password import hash_password

    async with async_session_maker() as session:
        admin_user = User(
            email="admin@example.com",
            hashed_password=hash_password("adminpass123"),
            role="admin",
        )
        session.add(admin_user)
        await session.commit()

    login_response = await client.post(
        "/api/v1/auth/token",
        data={"username": "admin@example.com", "password": "adminpass123"},
    )
    token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/auth/admin/users",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
