"""
Security Middleware for Mindframe AI
Implements rate limiting, CORS, XSS protection, and input validation
"""
from fastapi import Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import re
from typing import Callable
from loguru import logger

# ============================================================================
# RATE LIMITING
# ============================================================================

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

# Rate limit configurations
RATE_LIMITS = {
    "general": "100/minute",
    "api": "60/minute",
    "auth": "5/minute",  # Strict for login/register
    "income_bots": "1000/hour",  # More lenient for bot operations
    "marketplace": "200/minute"
}

# ============================================================================
# CORS CONFIGURATION
# ============================================================================

def setup_cors(app):
    """Configure CORS for production"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://mindframe.ai",
            "https://www.mindframe.ai",
            "https://mframe.io",
            "https://www.mframe.io"
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"],
        expose_headers=["X-Total-Count", "X-RateLimit-Limit", "X-RateLimit-Remaining"]
    )

# ============================================================================
# TRUSTED HOSTS
# ============================================================================

def setup_trusted_hosts(app):
    """Configure trusted hosts"""
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "mindframe.ai",
            "www.mindframe.ai",
            "mframe.io",
            "www.mframe.io",
            "*.mindframe.ai"  # Allow subdomains
        ]
    )

# ============================================================================
# XSS PROTECTION MIDDLEWARE
# ============================================================================

class XSSProtectionMiddleware(BaseHTTPMiddleware):
    """Middleware to prevent XSS attacks"""

    async def dispatch(self, request: Request, call_next: Callable):
        # Check for suspicious patterns in query parameters
        if request.query_params:
            for key, value in request.query_params.items():
                if self._contains_xss(value):
                    logger.warning(f"XSS attempt detected in query param: {key}={value}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid input detected"
                    )

        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https://api.openai.com"
        )

        return response

    def _contains_xss(self, value: str) -> bool:
        """Check if value contains common XSS patterns"""
        xss_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',  # Event handlers like onclick=
            r'<iframe',
            r'<object',
            r'<embed',
            r'eval\(',
            r'expression\('
        ]

        for pattern in xss_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                return True
        return False

# ============================================================================
# SQL INJECTION PROTECTION
# ============================================================================

class SQLInjectionProtectionMiddleware(BaseHTTPMiddleware):
    """Middleware to detect SQL injection attempts"""

    async def dispatch(self, request: Request, call_next: Callable):
        # Check query parameters
        if request.query_params:
            for key, value in request.query_params.items():
                if self._contains_sql_injection(value):
                    logger.warning(f"SQL injection attempt detected: {key}={value}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid input detected"
                    )

        response = await call_next(request)
        return response

    def _contains_sql_injection(self, value: str) -> bool:
        """Check if value contains SQL injection patterns"""
        sql_patterns = [
            r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC)\b)",
            r"(--|#|\/\*|\*\/)",  # SQL comments
            r"(\bOR\b.*?=.*?=)",  # OR 1=1
            r"(\bUNION\b.*?\bSELECT\b)",
            r"';",
            r"1=1",
            r"' OR '1'='1"
        ]

        for pattern in sql_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                return True
        return False

# ============================================================================
# REQUEST LOGGING MIDDLEWARE
# ============================================================================

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests for security auditing"""

    async def dispatch(self, request: Request, call_next: Callable):
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )

        response = await call_next(request)

        # Log response
        logger.info(f"Response: {response.status_code} for {request.url.path}")

        return response

# ============================================================================
# INPUT VALIDATION
# ============================================================================

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> bool:
    """
    Validate password strength
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    """
    if len(password) < 8:
        return False

    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))

    return has_upper and has_lower and has_digit

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove javascript:
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)

    # Remove event handlers
    text = re.sub(r'on\w+\s*=', '', text, flags=re.IGNORECASE)

    return text.strip()

# ============================================================================
# SETUP FUNCTION
# ============================================================================

def setup_security_middleware(app):
    """Setup all security middleware"""

    # Add security headers and XSS protection
    app.add_middleware(XSSProtectionMiddleware)

    # Add SQL injection protection
    app.add_middleware(SQLInjectionProtectionMiddleware)

    # Add request logging
    app.add_middleware(RequestLoggingMiddleware)

    # Setup CORS
    setup_cors(app)

    # Setup trusted hosts (production only)
    # setup_trusted_hosts(app)  # Uncomment for production

    # Add rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    logger.success("✅ Security middleware configured")
