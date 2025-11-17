"""
Comprehensive Error Handling for Mindframe API

Provides:
- Custom exception classes
- Error response formatting
- Logging integration
- Sentry integration
- User-friendly error messages
"""
from typing import Optional, Dict, Any
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from loguru import logger
import traceback
from datetime import datetime
from enum import Enum


# ============================================================================
# ERROR CODES
# ============================================================================

class ErrorCode(str, Enum):
    """Standard error codes for the API"""

    # Authentication & Authorization
    UNAUTHORIZED = "UNAUTHORIZED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"

    # Validation
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_INPUT = "INVALID_INPUT"
    MISSING_FIELD = "MISSING_FIELD"

    # Resources
    NOT_FOUND = "NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    CONFLICT = "CONFLICT"

    # Rate Limiting
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    QUOTA_EXCEEDED = "QUOTA_EXCEEDED"

    # Payments
    PAYMENT_REQUIRED = "PAYMENT_REQUIRED"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    INVALID_SUBSCRIPTION = "INVALID_SUBSCRIPTION"

    # External Services
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    STRIPE_ERROR = "STRIPE_ERROR"
    SENDGRID_ERROR = "SENDGRID_ERROR"
    OPENAI_ERROR = "OPENAI_ERROR"
    TWILIO_ERROR = "TWILIO_ERROR"

    # System
    INTERNAL_ERROR = "INTERNAL_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    REDIS_ERROR = "REDIS_ERROR"
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"

    # Business Logic
    AGENT_DEPLOY_FAILED = "AGENT_DEPLOY_FAILED"
    WORKFLOW_ERROR = "WORKFLOW_ERROR"
    VOICE_CALL_FAILED = "VOICE_CALL_FAILED"


# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class MindframeException(Exception):
    """Base exception for all Mindframe errors"""

    def __init__(
        self,
        message: str,
        code: ErrorCode,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(MindframeException):
    """Raised when authentication fails"""

    def __init__(self, message: str = "Authentication failed", details: Optional[Dict] = None):
        super().__init__(
            message=message,
            code=ErrorCode.UNAUTHORIZED,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details
        )


class InvalidCredentialsError(MindframeException):
    """Raised when credentials are invalid"""

    def __init__(self, message: str = "Invalid email or password", details: Optional[Dict] = None):
        super().__init__(
            message=message,
            code=ErrorCode.INVALID_CREDENTIALS,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details
        )


class TokenExpiredError(MindframeException):
    """Raised when JWT token is expired"""

    def __init__(self, message: str = "Token has expired", details: Optional[Dict] = None):
        super().__init__(
            message=message,
            code=ErrorCode.TOKEN_EXPIRED,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details
        )


class PermissionDeniedError(MindframeException):
    """Raised when user doesn't have permission"""

    def __init__(self, message: str = "Permission denied", details: Optional[Dict] = None):
        super().__init__(
            message=message,
            code=ErrorCode.INSUFFICIENT_PERMISSIONS,
            status_code=status.HTTP_403_FORBIDDEN,
            details=details
        )


class ValidationError(MindframeException):
    """Raised when input validation fails"""

    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=message,
            code=ErrorCode.VALIDATION_ERROR,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


class ResourceNotFoundError(MindframeException):
    """Raised when a resource is not found"""

    def __init__(self, resource: str, identifier: Any, details: Optional[Dict] = None):
        message = f"{resource} with identifier '{identifier}' not found"
        super().__init__(
            message=message,
            code=ErrorCode.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details
        )


class ResourceAlreadyExistsError(MindframeException):
    """Raised when a resource already exists"""

    def __init__(self, resource: str, identifier: Any, details: Optional[Dict] = None):
        message = f"{resource} with identifier '{identifier}' already exists"
        super().__init__(
            message=message,
            code=ErrorCode.ALREADY_EXISTS,
            status_code=status.HTTP_409_CONFLICT,
            details=details
        )


class RateLimitExceededError(MindframeException):
    """Raised when rate limit is exceeded"""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: Optional[int] = None):
        details = {"retry_after": retry_after} if retry_after else {}
        super().__init__(
            message=message,
            code=ErrorCode.RATE_LIMIT_EXCEEDED,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details=details
        )


class PaymentRequiredError(MindframeException):
    """Raised when payment is required"""

    def __init__(self, message: str = "Payment required", details: Optional[Dict] = None):
        super().__init__(
            message=message,
            code=ErrorCode.PAYMENT_REQUIRED,
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            details=details
        )


class ExternalServiceError(MindframeException):
    """Raised when external service fails"""

    def __init__(self, service: str, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=f"{service} error: {message}",
            code=ErrorCode.EXTERNAL_SERVICE_ERROR,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details
        )


class DatabaseError(MindframeException):
    """Raised when database operation fails"""

    def __init__(self, message: str = "Database error occurred", details: Optional[Dict] = None):
        super().__init__(
            message=message,
            code=ErrorCode.DATABASE_ERROR,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


# ============================================================================
# ERROR RESPONSE FORMATTER
# ============================================================================

class ErrorResponse:
    """Standard error response format"""

    @staticmethod
    def format(
        error: Exception,
        request_id: Optional[str] = None,
        include_traceback: bool = False
    ) -> Dict[str, Any]:
        """
        Format error as JSON response

        Args:
            error: The exception
            request_id: Optional request ID for tracking
            include_traceback: Whether to include full traceback (debug only)

        Returns:
            Formatted error response
        """
        response = {
            "error": {
                "message": str(error),
                "timestamp": datetime.utcnow().isoformat(),
            }
        }

        # Add error code if available
        if isinstance(error, MindframeException):
            response["error"]["code"] = error.code
            response["error"]["details"] = error.details

        # Add request ID if available
        if request_id:
            response["error"]["request_id"] = request_id

        # Add traceback if enabled (debug mode only)
        if include_traceback:
            response["error"]["traceback"] = traceback.format_exc()

        return response


# ============================================================================
# ERROR HANDLER
# ============================================================================

async def mindframe_exception_handler(request: Request, exc: MindframeException) -> JSONResponse:
    """
    Handle all Mindframe custom exceptions

    Args:
        request: The request
        exc: The exception

    Returns:
        JSON response with error details
    """
    # Log error
    logger.error(
        f"MindframeException: {exc.code} - {exc.message} | "
        f"Path: {request.url.path} | "
        f"Method: {request.method} | "
        f"Details: {exc.details}"
    )

    # Log to Sentry (if configured)
    try:
        import sentry_sdk
        sentry_sdk.capture_exception(exc)
    except:
        pass

    # Get request ID from header
    request_id = request.headers.get("X-Request-ID")

    # Format error response
    error_response = ErrorResponse.format(
        error=exc,
        request_id=request_id,
        include_traceback=False  # Never include traceback in production
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle FastAPI HTTP exceptions

    Args:
        request: The request
        exc: The exception

    Returns:
        JSON response with error details
    """
    # Log error
    logger.warning(
        f"HTTPException: {exc.status_code} - {exc.detail} | "
        f"Path: {request.url.path} | "
        f"Method: {request.method}"
    )

    # Get request ID from header
    request_id = request.headers.get("X-Request-ID")

    error_response = {
        "error": {
            "message": exc.detail,
            "code": f"HTTP_{exc.status_code}",
            "timestamp": datetime.utcnow().isoformat(),
        }
    }

    if request_id:
        error_response["error"]["request_id"] = request_id

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle all unhandled exceptions

    Args:
        request: The request
        exc: The exception

    Returns:
        JSON response with error details
    """
    # Log error with full traceback
    logger.exception(
        f"Unhandled exception: {type(exc).__name__} - {str(exc)} | "
        f"Path: {request.url.path} | "
        f"Method: {request.method}"
    )

    # Log to Sentry (if configured)
    try:
        import sentry_sdk
        sentry_sdk.capture_exception(exc)
    except:
        pass

    # Get request ID from header
    request_id = request.headers.get("X-Request-ID")

    error_response = {
        "error": {
            "message": "An internal server error occurred",
            "code": ErrorCode.INTERNAL_ERROR,
            "timestamp": datetime.utcnow().isoformat(),
        }
    }

    if request_id:
        error_response["error"]["request_id"] = request_id

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response
    )


# ============================================================================
# SETUP ERROR HANDLERS
# ============================================================================

def setup_error_handlers(app):
    """
    Setup all error handlers for the FastAPI app

    Args:
        app: FastAPI application instance
    """
    from fastapi import HTTPException

    # Custom exceptions
    app.add_exception_handler(MindframeException, mindframe_exception_handler)

    # HTTP exceptions
    app.add_exception_handler(HTTPException, http_exception_handler)

    # General exceptions
    app.add_exception_handler(Exception, general_exception_handler)

    logger.info("Error handlers configured successfully")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def log_and_raise(
    error_class: type[MindframeException],
    message: str,
    **kwargs
) -> None:
    """
    Log an error and raise it

    Args:
        error_class: The exception class to raise
        message: Error message
        **kwargs: Additional arguments for the exception

    Raises:
        The specified exception
    """
    logger.error(message)
    raise error_class(message, **kwargs)


def handle_external_service_error(service: str, error: Exception) -> None:
    """
    Handle error from external service

    Args:
        service: Name of the service (Stripe, SendGrid, etc.)
        error: The exception

    Raises:
        ExternalServiceError
    """
    logger.error(f"{service} error: {str(error)}")
    raise ExternalServiceError(
        service=service,
        message=str(error),
        details={"original_error": type(error).__name__}
    )


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    # Error codes
    'ErrorCode',

    # Exceptions
    'MindframeException',
    'AuthenticationError',
    'InvalidCredentialsError',
    'TokenExpiredError',
    'PermissionDeniedError',
    'ValidationError',
    'ResourceNotFoundError',
    'ResourceAlreadyExistsError',
    'RateLimitExceededError',
    'PaymentRequiredError',
    'ExternalServiceError',
    'DatabaseError',

    # Handlers
    'setup_error_handlers',
    'ErrorResponse',

    # Helpers
    'log_and_raise',
    'handle_external_service_error',
]
