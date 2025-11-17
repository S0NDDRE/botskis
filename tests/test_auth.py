"""
Authentication Tests
Test login, registration, JWT tokens, etc.
"""
import pytest
from fastapi.testclient import TestClient


# ============================================================================
# UNIT TESTS
# ============================================================================

@pytest.mark.unit
def test_create_access_token():
    """Test JWT token creation"""
    from src.auth.jwt import create_access_token, decode_access_token

    user_id = 123
    token = create_access_token(user_id)

    assert token is not None
    assert isinstance(token, str)

    # Decode and verify
    payload = decode_access_token(token)
    assert payload["user_id"] == user_id


@pytest.mark.unit
def test_password_hashing():
    """Test password hashing and verification"""
    from src.auth.password import hash_password, verify_password

    password = "SecurePassword123!"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

@pytest.mark.integration
def test_register_user(client: TestClient):
    """Test user registration"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "SecurePassword123!",
            "name": "New User"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert "token" in data
    assert data["user"]["email"] == "newuser@example.com"


@pytest.mark.integration
def test_register_duplicate_email(client: TestClient):
    """Test registering with existing email"""
    # First registration
    client.post(
        "/api/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "Password123!",
            "name": "User One"
        }
    )

    # Duplicate registration
    response = client.post(
        "/api/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "Password456!",
            "name": "User Two"
        }
    )

    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "already exists" in data["error"]["message"].lower()


@pytest.mark.integration
def test_login_success(client: TestClient):
    """Test successful login"""
    # Register user first
    client.post(
        "/api/auth/register",
        json={
            "email": "login@example.com",
            "password": "Password123!",
            "name": "Login Test"
        }
    )

    # Login
    response = client.post(
        "/api/auth/login",
        json={
            "email": "login@example.com",
            "password": "Password123!"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "token" in data
    assert data["user"]["email"] == "login@example.com"


@pytest.mark.integration
def test_login_wrong_password(client: TestClient):
    """Test login with wrong password"""
    # Register user first
    client.post(
        "/api/auth/register",
        json={
            "email": "wrongpw@example.com",
            "password": "CorrectPassword123!",
            "name": "Test User"
        }
    )

    # Login with wrong password
    response = client.post(
        "/api/auth/login",
        json={
            "email": "wrongpw@example.com",
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False


@pytest.mark.integration
def test_protected_endpoint_without_auth(client: TestClient):
    """Test accessing protected endpoint without token"""
    response = client.get("/api/users/me")

    assert response.status_code == 401


@pytest.mark.integration
def test_protected_endpoint_with_auth(client: TestClient, auth_headers):
    """Test accessing protected endpoint with valid token"""
    response = client.get("/api/users/me", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert "user" in data


# ============================================================================
# E2E TESTS
# ============================================================================

@pytest.mark.e2e
def test_complete_auth_flow(client: TestClient):
    """Test complete authentication flow"""
    # 1. Register
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "e2e@example.com",
            "password": "Password123!",
            "name": "E2E Test"
        }
    )
    assert register_response.status_code == 201
    token = register_response.json()["token"]

    # 2. Access protected resource
    headers = {"Authorization": f"Bearer {token}"}
    me_response = client.get("/api/users/me", headers=headers)
    assert me_response.status_code == 200
    assert me_response.json()["user"]["email"] == "e2e@example.com"

    # 3. Logout (if implemented)
    # logout_response = client.post("/api/auth/logout", headers=headers)
    # assert logout_response.status_code == 200

    # 4. Try to access after logout (should fail)
    # me_response_after = client.get("/api/users/me", headers=headers)
    # assert me_response_after.status_code == 401
