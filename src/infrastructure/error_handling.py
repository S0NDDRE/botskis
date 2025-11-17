"""
Standardized Error Handling
Ensures app NEVER crashes with proper error handling

Features:
- Custom exception classes
- Error middleware
- Retry logic with exponential backoff
- Circuit breaker pattern
- User-friendly error messages
- Automatic error tracking integration
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Callable, Optional, Any, TypeVar, Dict
from functools import wraps
import asyncio
import time
from enum import Enum
from loguru import logger
from datetime import datetime, timedelta


# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class MindframeException(Exception):
    """Base exception for all Mindframe errors"""
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Dict] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class DatabaseError(MindframeException):
    """Database operation failed"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=message,
            status_code=503,
            error_code="DATABASE_ERROR",
            details=details
        )


class ValidationError(MindframeException):
    """Input validation failed"""
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            message=message,
            status_code=400,
            error_code="VALIDATION_ERROR",
            details={"field": field} if field else {}
        )


class AuthenticationError(MindframeException):
    """Authentication failed"""
    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            message=message,
            status_code=401,
            error_code="AUTHENTICATION_ERROR"
        )


class AuthorizationError(MindframeException):
    """Authorization failed (insufficient permissions)"""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            status_code=403,
            error_code="AUTHORIZATION_ERROR"
        )


class NotFoundError(MindframeException):
    """Resource not found"""
    def __init__(self, resource: str, resource_id: Any):
        super().__init__(
            message=f"{resource} not found",
            status_code=404,
            error_code="NOT_FOUND",
            details={"resource": resource, "id": str(resource_id)}
        )


class RateLimitError(MindframeException):
    """Rate limit exceeded"""
    def __init__(self, retry_after: int = 60):
        super().__init__(
            message="Rate limit exceeded",
            status_code=429,
            error_code="RATE_LIMIT_EXCEEDED",
            details={"retry_after_seconds": retry_after}
        )


class ExternalServiceError(MindframeException):
    """External service (Stripe, Vipps, etc.) failed"""
    def __init__(self, service: str, message: str):
        super().__init__(
            message=f"{service} error: {message}",
            status_code=502,
            error_code="EXTERNAL_SERVICE_ERROR",
            details={"service": service}
        )


# ============================================================================
# ERROR MIDDLEWARE
# ============================================================================

async def error_handling_middleware(request: Request, call_next):
    """
    Global error handling middleware

    Catches all unhandled exceptions and returns user-friendly responses
    """
    try:
        response = await call_next(request)
        return response

    except MindframeException as e:
        # Our custom exceptions - already formatted
        logger.warning(f"⚠️  {e.error_code}: {e.message}")

        # Track error
        try:
            from src.monitoring.error_tracker import error_tracker
            await error_tracker.capture_message(
                message=f"{e.error_code}: {e.message}",
                level="warning"
            )
        except:
            pass

        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "error": {
                    "code": e.error_code,
                    "message": e.message,
                    "details": e.details
                }
            }
        )

    except HTTPException as e:
        # FastAPI HTTP exceptions
        logger.warning(f"⚠️  HTTP {e.status_code}: {e.detail}")

        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "error": {
                    "code": f"HTTP_{e.status_code}",
                    "message": e.detail
                }
            }
        )

    except Exception as e:
        # Unexpected errors - log and track
        logger.error(f"❌ Unhandled exception: {e}", exc_info=True)

        # Track error
        try:
            from src.monitoring.error_tracker import error_tracker, ErrorContext, ErrorSeverity
            await error_tracker.capture_exception(
                exception=e,
                context=ErrorContext(
                    url=str(request.url),
                    method=request.method
                ),
                severity=ErrorSeverity.CRITICAL
            )
        except:
            pass

        # Return generic error (don't expose internals)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred. Our team has been notified."
                }
            }
        )


# ============================================================================
# RETRY LOGIC
# ============================================================================

T = TypeVar('T')

async def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    exceptions: tuple = (Exception,)
) -> Any:
    """
    Retry function with exponential backoff

    Args:
        func: Async function to retry
        max_retries: Maximum number of retries
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff
        exceptions: Tuple of exceptions to catch

    Returns:
        Function result

    Raises:
        Last exception if all retries fail

    Example:
    ```python
    async def fetch_external_api():
        response = await http.get("https://api.example.com")
        return response

    # Retry up to 3 times with exponential backoff
    result = await retry_with_backoff(
        fetch_external_api,
        max_retries=3,
        initial_delay=1.0
    )
    ```
    """
    last_exception = None
    delay = initial_delay

    for attempt in range(max_retries + 1):
        try:
            return await func()

        except exceptions as e:
            last_exception = e

            if attempt == max_retries:
                logger.error(f"❌ All {max_retries} retries failed: {e}")
                raise

            # Calculate next delay with exponential backoff
            delay = min(initial_delay * (exponential_base ** attempt), max_delay)

            logger.warning(
                f"⚠️  Attempt {attempt + 1}/{max_retries} failed: {e}. "
                f"Retrying in {delay:.1f}s..."
            )

            await asyncio.sleep(delay)

    raise last_exception


def retry(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    exceptions: tuple = (Exception,)
):
    """
    Decorator for retry with exponential backoff

    Example:
    ```python
    @retry(max_retries=3, initial_delay=1.0)
    async def fetch_data():
        return await external_api.get_data()
    ```
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await retry_with_backoff(
                lambda: func(*args, **kwargs),
                max_retries=max_retries,
                initial_delay=initial_delay,
                exceptions=exceptions
            )
        return wrapper
    return decorator


# ============================================================================
# CIRCUIT BREAKER
# ============================================================================

class CircuitState(str, Enum):
    """Circuit breaker states"""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Service unavailable, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitBreaker:
    """
    Circuit Breaker Pattern

    Prevents cascading failures by stopping calls to failing services

    States:
    - CLOSED: Normal operation, all calls go through
    - OPEN: Service failing, reject all calls
    - HALF_OPEN: Testing recovery, allow limited calls

    Example:
    ```python
    stripe_breaker = CircuitBreaker(
        failure_threshold=5,
        timeout_seconds=60
    )

    @stripe_breaker.call
    async def charge_customer():
        return await stripe.charge(...)
    ```
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        timeout_seconds: int = 60,
        half_open_max_calls: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.half_open_max_calls = half_open_max_calls

        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = CircuitState.CLOSED
        self.half_open_calls = 0

    def call(self, func: Callable) -> Callable:
        """Decorator to wrap function with circuit breaker"""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await self._execute(func, *args, **kwargs)
        return wrapper

    async def _execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker logic"""

        # Check if circuit is OPEN
        if self.state == CircuitState.OPEN:
            # Check if timeout has passed
            if self.last_failure_time:
                elapsed = (datetime.now() - self.last_failure_time).total_seconds()
                if elapsed > self.timeout_seconds:
                    # Try to recover
                    logger.info("🔄 Circuit HALF_OPEN - testing recovery")
                    self.state = CircuitState.HALF_OPEN
                    self.half_open_calls = 0
                else:
                    # Still in timeout
                    raise ExternalServiceError(
                        service="Circuit Breaker",
                        message=f"Service unavailable (circuit OPEN). Retry in {self.timeout_seconds - elapsed:.0f}s"
                    )

        # Limit calls in HALF_OPEN state
        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_calls >= self.half_open_max_calls:
                raise ExternalServiceError(
                    service="Circuit Breaker",
                    message="Service recovering (circuit HALF_OPEN). Please retry later."
                )
            self.half_open_calls += 1

        try:
            # Execute function
            result = await func(*args, **kwargs)

            # Success - reset circuit
            if self.state == CircuitState.HALF_OPEN:
                logger.info("✅ Circuit CLOSED - service recovered")
                self.state = CircuitState.CLOSED
                self.failure_count = 0

            return result

        except Exception as e:
            # Failure - update circuit
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.failure_threshold:
                logger.error(
                    f"❌ Circuit OPEN - {self.failure_count} failures. "
                    f"Service unavailable for {self.timeout_seconds}s"
                )
                self.state = CircuitState.OPEN

            raise


# ============================================================================
# ERROR RESPONSE HELPERS
# ============================================================================

def error_response(
    message: str,
    status_code: int = 500,
    error_code: str = "ERROR",
    details: Optional[Dict] = None
) -> JSONResponse:
    """
    Create standardized error response

    Example:
    ```python
    return error_response(
        message="User not found",
        status_code=404,
        error_code="USER_NOT_FOUND",
        details={"user_id": user_id}
    )
    ```
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "code": error_code,
                "message": message,
                "details": details or {}
            }
        }
    )


def success_response(
    data: Any = None,
    message: Optional[str] = None
) -> Dict:
    """
    Create standardized success response

    Example:
    ```python
    return success_response(
        data={"user": user_dict},
        message="User created successfully"
    )
    ```
    """
    response = {"success": True}

    if data is not None:
        response["data"] = data

    if message:
        response["message"] = message

    return response


# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def validate_required(value: Any, field_name: str):
    """Validate required field"""
    if value is None or value == "":
        raise ValidationError(f"{field_name} is required", field=field_name)


def validate_email(email: str):
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("Invalid email format", field="email")


def validate_min_length(value: str, min_length: int, field_name: str):
    """Validate minimum length"""
    if len(value) < min_length:
        raise ValidationError(
            f"{field_name} must be at least {min_length} characters",
            field=field_name
        )


def validate_max_length(value: str, max_length: int, field_name: str):
    """Validate maximum length"""
    if len(value) > max_length:
        raise ValidationError(
            f"{field_name} must be at most {max_length} characters",
            field=field_name
        )


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    # Exceptions
    'MindframeException',
    'DatabaseError',
    'ValidationError',
    'AuthenticationError',
    'AuthorizationError',
    'NotFoundError',
    'RateLimitError',
    'ExternalServiceError',

    # Middleware
    'error_handling_middleware',

    # Retry
    'retry_with_backoff',
    'retry',

    # Circuit Breaker
    'CircuitBreaker',
    'CircuitState',

    # Helpers
    'error_response',
    'success_response',
    'validate_required',
    'validate_email',
    'validate_min_length',
    'validate_max_length'
]
