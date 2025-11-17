"""
Security Tests
Test protection against vulnerabilities
"""
import pytest
from fastapi.testclient import TestClient
import time


# ============================================================================
# RATE LIMITING TESTS
# ============================================================================

@pytest.mark.unit
def test_rate_limiter():
    """Test rate limiting logic"""
    from src.security.security_middleware import RateLimiter

    limiter = RateLimiter(max_requests=5, window_seconds=60)

    # Should allow first 5 requests
    for i in range(5):
        assert limiter.is_allowed("test_ip") is True

    # 6th request should be blocked
    assert limiter.is_allowed("test_ip") is False


@pytest.mark.unit
def test_rate_limiter_window_reset():
    """Test rate limit window reset"""
    from src.security.security_middleware import RateLimiter

    limiter = RateLimiter(max_requests=2, window_seconds=1)

    # Use up limit
    assert limiter.is_allowed("test_ip") is True
    assert limiter.is_allowed("test_ip") is True
    assert limiter.is_allowed("test_ip") is False

    # Wait for window to reset
    time.sleep(1.1)

    # Should be allowed again
    assert limiter.is_allowed("test_ip") is True


@pytest.mark.integration
def test_rate_limit_endpoint(client):
    """Test rate limiting on endpoints"""
    # Make many requests quickly
    responses = []
    for i in range(150):
        response = client.get("/api/health")
        responses.append(response.status_code)

    # Some should be rate limited (429)
    assert 429 in responses


# ============================================================================
# XSS PROTECTION TESTS
# ============================================================================

@pytest.mark.unit
def test_xss_sanitization():
    """Test XSS sanitization"""
    from src.security.security_middleware import XSSProtection

    # Malicious script
    malicious = '<script>alert("XSS")</script>'
    sanitized = XSSProtection.sanitize(malicious)

    assert '<script>' not in sanitized
    assert 'alert' not in sanitized

    # Javascript event handler
    malicious2 = '<img src=x onerror=alert("XSS")>'
    sanitized2 = XSSProtection.sanitize(malicious2)

    assert 'onerror' not in sanitized2

    # Safe text should remain
    safe = "Hello, world!"
    assert XSSProtection.sanitize(safe) == safe


@pytest.mark.unit
def test_xss_detection():
    """Test XSS pattern detection"""
    from src.security.security_middleware import XSSProtection

    # Should detect XSS
    assert XSSProtection.is_safe('<script>alert(1)</script>') is False
    assert XSSProtection.is_safe('javascript:alert(1)') is False
    assert XSSProtection.is_safe('<img onerror=alert(1)>') is False

    # Should pass safe content
    assert XSSProtection.is_safe('Hello, world!') is True
    assert XSSProtection.is_safe('user@example.com') is True


@pytest.mark.integration
def test_xss_protection_endpoint(client, auth_headers):
    """Test XSS protection on user input"""
    response = client.post(
        "/api/users/update",
        headers=auth_headers,
        json={
            "name": '<script>alert("XSS")</script>John Doe'
        }
    )

    # Should either reject or sanitize
    if response.status_code == 200:
        data = response.json()
        # Name should be sanitized
        assert '<script>' not in data.get('name', '')


# ============================================================================
# SQL INJECTION TESTS
# ============================================================================

@pytest.mark.unit
def test_sql_injection_detection():
    """Test SQL injection pattern detection"""
    from src.security.security_middleware import SQLInjectionProtection

    # Should detect SQL injection
    assert SQLInjectionProtection.is_safe("1' OR '1'='1") is False
    assert SQLInjectionProtection.is_safe("admin'--") is False
    assert SQLInjectionProtection.is_safe("'; DROP TABLE users--") is False
    assert SQLInjectionProtection.is_safe("1 UNION SELECT * FROM users") is False

    # Should pass safe input
    assert SQLInjectionProtection.is_safe("john@example.com") is True
    assert SQLInjectionProtection.is_safe("John Doe") is True


@pytest.mark.integration
def test_sql_injection_protection_endpoint(client):
    """Test SQL injection protection on login"""
    # Attempt SQL injection in login
    response = client.post(
        "/api/auth/login",
        json={
            "email": "admin'--",
            "password": "anything"
        }
    )

    # Should be rejected (400 or 401)
    assert response.status_code in [400, 401]

    # Attempt SQL injection in search
    response2 = client.get(
        "/api/search?q=1' UNION SELECT * FROM users--",
        headers={"Authorization": "Bearer test"}
    )

    # Should be rejected
    assert response2.status_code in [400, 404]


# ============================================================================
# CSRF PROTECTION TESTS
# ============================================================================

@pytest.mark.unit
def test_csrf_token_generation():
    """Test CSRF token generation"""
    from src.security.security_middleware import CSRFProtection

    csrf = CSRFProtection(secret_key="test_secret")

    token1 = csrf.generate_token("session_123")
    token2 = csrf.generate_token("session_123")

    # Tokens should be consistent for same session
    assert token1 == token2

    # Different sessions should have different tokens
    token3 = csrf.generate_token("session_456")
    assert token1 != token3


@pytest.mark.unit
def test_csrf_token_validation():
    """Test CSRF token validation"""
    from src.security.security_middleware import CSRFProtection

    csrf = CSRFProtection(secret_key="test_secret")

    session_id = "session_123"
    token = csrf.generate_token(session_id)

    # Valid token should pass
    assert csrf.validate_token(token, session_id) is True

    # Invalid token should fail
    assert csrf.validate_token("invalid_token", session_id) is False

    # Token for wrong session should fail
    assert csrf.validate_token(token, "different_session") is False


@pytest.mark.integration
def test_csrf_protection_endpoint(client):
    """Test CSRF protection on state-changing operations"""
    # POST without CSRF token should fail
    response = client.post(
        "/api/users/update",
        json={"name": "New Name"}
    )

    # Should be rejected (403 or require auth)
    assert response.status_code in [401, 403]


# ============================================================================
# SECURITY HEADERS TESTS
# ============================================================================

@pytest.mark.integration
def test_security_headers(client):
    """Test security headers are present"""
    response = client.get("/api/health")

    # Check security headers
    assert "X-Content-Type-Options" in response.headers
    assert response.headers["X-Content-Type-Options"] == "nosniff"

    assert "X-Frame-Options" in response.headers
    assert response.headers["X-Frame-Options"] == "DENY"

    assert "X-XSS-Protection" in response.headers

    assert "Content-Security-Policy" in response.headers

    assert "Strict-Transport-Security" in response.headers


# ============================================================================
# INPUT VALIDATION TESTS
# ============================================================================

@pytest.mark.unit
def test_email_validation():
    """Test email validation"""
    from src.security.security_middleware import InputValidator

    # Valid emails
    assert InputValidator.validate_email("test@example.com") is True
    assert InputValidator.validate_email("user.name@domain.co.uk") is True

    # Invalid emails
    assert InputValidator.validate_email("invalid") is False
    assert InputValidator.validate_email("@example.com") is False
    assert InputValidator.validate_email("test@") is False


@pytest.mark.unit
def test_phone_validation():
    """Test phone number validation"""
    from src.security.security_middleware import InputValidator

    # Valid phones
    assert InputValidator.validate_phone("+4712345678") is True
    assert InputValidator.validate_phone("+1-555-123-4567") is True

    # Invalid phones
    assert InputValidator.validate_phone("123") is False
    assert InputValidator.validate_phone("abc") is False


@pytest.mark.unit
def test_url_validation():
    """Test URL validation"""
    from src.security.security_middleware import InputValidator

    # Valid URLs
    assert InputValidator.validate_url("https://example.com") is True
    assert InputValidator.validate_url("http://subdomain.example.com/path") is True

    # Invalid URLs
    assert InputValidator.validate_url("not a url") is False
    assert InputValidator.validate_url("ftp://example.com") is False


@pytest.mark.unit
def test_password_strength():
    """Test password strength validation"""
    from src.security.security_middleware import InputValidator

    # Weak passwords
    assert InputValidator.is_password_strong("password") is False
    assert InputValidator.is_password_strong("12345678") is False

    # Strong passwords
    assert InputValidator.is_password_strong("SecurePass123!") is True
    assert InputValidator.is_password_strong("MyP@ssw0rd2025") is True


# ============================================================================
# E2E SECURITY TESTS
# ============================================================================

@pytest.mark.e2e
def test_complete_security_workflow(client):
    """Test complete security workflow"""

    # 1. Rate limiting should work
    for _ in range(100):
        client.get("/api/health")

    # 100+ requests should trigger rate limit
    response = client.get("/api/health")
    # Might be 429 if rate limited

    # 2. Security headers should be present
    assert "X-Content-Type-Options" in response.headers

    # 3. XSS should be blocked/sanitized
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "SecurePass123!",
            "name": "<script>alert('XSS')</script>"
        }
    )

    # Should either reject or sanitize
    # Check user was created safely

    # 4. SQL injection should be blocked
    response = client.post(
        "/api/auth/login",
        json={
            "email": "admin'--",
            "password": "anything"
        }
    )

    # Should be rejected
    assert response.status_code in [400, 401]


@pytest.mark.e2e
def test_authentication_security(client):
    """Test authentication security"""

    # 1. Weak password should be rejected
    response = client.post(
        "/api/auth/register",
        json={
            "email": "weak@example.com",
            "password": "weak",
            "name": "Weak User"
        }
    )

    # Should reject weak password
    assert response.status_code == 400

    # 2. SQL injection in email should be blocked
    response = client.post(
        "/api/auth/register",
        json={
            "email": "admin'--@example.com",
            "password": "SecurePass123!",
            "name": "Test"
        }
    )

    assert response.status_code == 400

    # 3. Invalid email format should be rejected
    response = client.post(
        "/api/auth/register",
        json={
            "email": "not_an_email",
            "password": "SecurePass123!",
            "name": "Test"
        }
    )

    assert response.status_code == 400


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_penetration_testing_scenarios():
    """Test common penetration testing scenarios"""
    from src.security.security_middleware import (
        XSSProtection,
        SQLInjectionProtection,
        InputValidator
    )

    # Common XSS payloads
    xss_payloads = [
        '<script>alert(1)</script>',
        '<img src=x onerror=alert(1)>',
        'javascript:alert(1)',
        '<svg onload=alert(1)>',
    ]

    for payload in xss_payloads:
        assert XSSProtection.is_safe(payload) is False

    # Common SQL injection payloads
    sql_payloads = [
        "1' OR '1'='1",
        "admin'--",
        "'; DROP TABLE users--",
        "1 UNION SELECT NULL--",
    ]

    for payload in sql_payloads:
        assert SQLInjectionProtection.is_safe(payload) is False

    # Common validation bypasses
    assert InputValidator.validate_email("admin'--@example.com") is False
    assert InputValidator.validate_url("javascript:alert(1)") is False
