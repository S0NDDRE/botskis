"""
Security Middleware
Protection against common vulnerabilities
"""
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Optional, Callable
from datetime import datetime, timedelta
from collections import defaultdict
import re
import hashlib
from loguru import logger


# ============================================================================
# RATE LIMITING
# ============================================================================

class RateLimiter:
    """
    Rate limiting to prevent abuse

    Protects against:
    - Brute force attacks
    - DoS attacks
    - API abuse

    Usage:
    ```python
    limiter = RateLimiter(max_requests=100, window_seconds=60)

    if not limiter.is_allowed(client_ip):
        raise HTTPException(429, "Too many requests")
    ```
    """

    def __init__(
        self,
        max_requests: int = 100,
        window_seconds: int = 60
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

        # Track requests per IP
        self.requests: Dict[str, list] = defaultdict(list)

    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed"""
        now = datetime.now()
        window_start = now - timedelta(seconds=self.window_seconds)

        # Clean old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > window_start
        ]

        # Check limit
        if len(self.requests[identifier]) >= self.max_requests:
            logger.warning(
                f"⚠️  Rate limit exceeded for {identifier}: "
                f"{len(self.requests[identifier])} requests"
            )
            return False

        # Add current request
        self.requests[identifier].append(now)
        return True

    def get_remaining(self, identifier: str) -> int:
        """Get remaining requests in window"""
        now = datetime.now()
        window_start = now - timedelta(seconds=self.window_seconds)

        # Count recent requests
        recent = [
            req_time for req_time in self.requests.get(identifier, [])
            if req_time > window_start
        ]

        return max(0, self.max_requests - len(recent))


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""

    def __init__(
        self,
        app,
        max_requests: int = 100,
        window_seconds: int = 60
    ):
        super().__init__(app)
        self.limiter = RateLimiter(max_requests, window_seconds)

    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host

        # Check rate limit
        if not self.limiter.is_allowed(client_ip):
            return HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later.",
                headers={
                    "Retry-After": str(self.limiter.window_seconds)
                }
            )

        # Add rate limit headers
        response = await call_next(request)

        response.headers["X-RateLimit-Limit"] = str(self.limiter.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(
            self.limiter.get_remaining(client_ip)
        )

        return response


# ============================================================================
# XSS PROTECTION
# ============================================================================

class XSSProtection:
    """
    Cross-Site Scripting (XSS) protection

    Sanitizes user input to prevent XSS attacks
    """

    # Dangerous patterns
    XSS_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',  # onclick, onload, etc.
        r'<iframe[^>]*>',
        r'<object[^>]*>',
        r'<embed[^>]*>',
    ]

    @classmethod
    def sanitize(cls, text: str) -> str:
        """Sanitize text from XSS"""
        if not text:
            return text

        # Remove dangerous patterns
        for pattern in cls.XSS_PATTERNS:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)

        # Escape HTML entities
        text = (
            text.replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#x27;')
        )

        return text

    @classmethod
    def is_safe(cls, text: str) -> bool:
        """Check if text is safe from XSS"""
        if not text:
            return True

        for pattern in cls.XSS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                logger.warning(f"⚠️  XSS pattern detected: {pattern}")
                return False

        return True


# ============================================================================
# SQL INJECTION PROTECTION
# ============================================================================

class SQLInjectionProtection:
    """
    SQL Injection protection

    Detects and blocks SQL injection attempts
    """

    # Common SQL injection patterns
    SQL_PATTERNS = [
        r"(\bunion\b.*\bselect\b)",
        r"(\bselect\b.*\bfrom\b)",
        r"(\binsert\b.*\binto\b)",
        r"(\bupdate\b.*\bset\b)",
        r"(\bdelete\b.*\bfrom\b)",
        r"(\bdrop\b.*\btable\b)",
        r"(;\s*drop\b)",
        r"(--\s*$)",
        r"(/\*.*\*/)",
        r"(\bor\b\s+['\"]?1['\"]?\s*=\s*['\"]?1)",
        r"(\band\b\s+['\"]?1['\"]?\s*=\s*['\"]?1)",
    ]

    @classmethod
    def is_safe(cls, text: str) -> bool:
        """Check if text is safe from SQL injection"""
        if not text:
            return True

        for pattern in cls.SQL_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                logger.warning(
                    f"🚨 SQL Injection attempt detected: {pattern}"
                )
                return False

        return True

    @classmethod
    def validate_input(cls, text: str) -> str:
        """Validate and raise if SQL injection detected"""
        if not cls.is_safe(text):
            raise HTTPException(
                status_code=400,
                detail="Invalid input detected"
            )
        return text


# ============================================================================
# CSRF PROTECTION
# ============================================================================

class CSRFProtection:
    """
    Cross-Site Request Forgery (CSRF) protection

    Generates and validates CSRF tokens
    """

    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def generate_token(self, session_id: str) -> str:
        """Generate CSRF token"""
        data = f"{session_id}:{self.secret_key}:{datetime.now().isoformat()}"
        token = hashlib.sha256(data.encode()).hexdigest()
        return token

    def validate_token(self, token: str, session_id: str) -> bool:
        """Validate CSRF token"""
        expected_token = self.generate_token(session_id)

        # Constant-time comparison (prevent timing attacks)
        if len(token) != len(expected_token):
            return False

        result = 0
        for a, b in zip(token, expected_token):
            result |= ord(a) ^ ord(b)

        return result == 0


class CSRFMiddleware(BaseHTTPMiddleware):
    """CSRF protection middleware"""

    def __init__(self, app, secret_key: str):
        super().__init__(app)
        self.csrf = CSRFProtection(secret_key)

    async def dispatch(self, request: Request, call_next):
        # Skip CSRF for GET, HEAD, OPTIONS
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return await call_next(request)

        # Skip for API endpoints with Bearer token
        if request.headers.get("Authorization", "").startswith("Bearer "):
            return await call_next(request)

        # Get CSRF token from header
        csrf_token = request.headers.get("X-CSRF-Token")

        if not csrf_token:
            raise HTTPException(
                status_code=403,
                detail="CSRF token missing"
            )

        # Get session ID (from cookie or header)
        session_id = request.cookies.get("session_id", "")

        if not self.csrf.validate_token(csrf_token, session_id):
            logger.warning("🚨 CSRF token validation failed")
            raise HTTPException(
                status_code=403,
                detail="CSRF token invalid"
            )

        return await call_next(request)


# ============================================================================
# SECURITY HEADERS
# ============================================================================

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to responses

    Headers:
    - X-Content-Type-Options: nosniff
    - X-Frame-Options: DENY
    - X-XSS-Protection: 1; mode=block
    - Strict-Transport-Security: HTTPS only
    - Content-Security-Policy: Prevent XSS
    """

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # XSS protection
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # HTTPS only (in production)
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

        # Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )

        # Referrer policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions policy
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )

        return response


# ============================================================================
# INPUT VALIDATION
# ============================================================================

class InputValidator:
    """
    Comprehensive input validation

    Validates:
    - Email addresses
    - Phone numbers
    - URLs
    - Usernames
    - Passwords
    """

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number"""
        # Remove common formatting
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)

        # Check if valid E.164 format
        pattern = r'^\+?[1-9]\d{1,14}$'
        return bool(re.match(pattern, cleaned))

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL"""
        pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
        return bool(re.match(pattern, url))

    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username"""
        # 3-20 chars, alphanumeric + underscore
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return bool(re.match(pattern, username))

    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, bool]:
        """Check password strength"""
        return {
            "length": len(password) >= 8,
            "uppercase": bool(re.search(r'[A-Z]', password)),
            "lowercase": bool(re.search(r'[a-z]', password)),
            "digit": bool(re.search(r'\d', password)),
            "special": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
        }

    @staticmethod
    def is_password_strong(password: str) -> bool:
        """Check if password is strong"""
        checks = InputValidator.validate_password_strength(password)
        return all(checks.values())


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'RateLimiter',
    'RateLimitMiddleware',
    'XSSProtection',
    'SQLInjectionProtection',
    'CSRFProtection',
    'CSRFMiddleware',
    'SecurityHeadersMiddleware',
    'InputValidator',
]
