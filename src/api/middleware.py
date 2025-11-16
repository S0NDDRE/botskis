"""
API Middleware - Rate limiting, logging, error handling
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import time
import sys

# Configure loguru
logger.remove()  # Remove default handler
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    "logs/app.log",
    rotation="500 MB",
    retention="10 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG"
)
logger.add(
    "logs/error.log",
    rotation="500 MB",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="ERROR"
)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging all requests and responses
    """

    async def dispatch(self, request: Request, call_next):
        """Log requests and responses"""
        start_time = time.time()

        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )

        try:
            response = await call_next(request)

            # Calculate duration
            duration = time.time() - start_time

            # Log response
            logger.info(
                f"Response: {request.method} {request.url.path} "
                f"status={response.status_code} duration={duration:.3f}s"
            )

            # Add custom headers
            response.headers["X-Process-Time"] = str(duration)

            return response

        except Exception as e:
            logger.error(
                f"Error processing request: {request.method} {request.url.path} "
                f"error={str(e)}"
            )
            raise


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for catching and handling all exceptions
    """

    async def dispatch(self, request: Request, call_next):
        """Handle all exceptions"""
        try:
            return await call_next(request)

        except HTTPException as e:
            # Re-raise HTTP exceptions (already handled by FastAPI)
            raise

        except ValueError as e:
            logger.error(f"ValueError: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Invalid input",
                    "detail": str(e)
                }
            )

        except Exception as e:
            logger.exception(f"Unhandled exception: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal server error",
                    "detail": "An unexpected error occurred"
                }
            )


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware for adding security headers
    """

    async def dispatch(self, request: Request, call_next):
        """Add security headers to response"""
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response


def setup_middleware(app):
    """
    Setup all middleware for the application

    Args:
        app: FastAPI application instance
    """
    # Add middleware (order matters - last added is executed first)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(LoggingMiddleware)

    # Add rate limiter
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    logger.info("Middleware configured successfully")


# Custom logger for specific use cases
def log_agent_action(agent_id: int, action: str, user_id: int, details: dict = None):
    """
    Log agent-specific actions

    Args:
        agent_id: Agent ID
        action: Action performed
        user_id: User who performed action
        details: Additional details
    """
    logger.info(
        f"Agent Action | agent_id={agent_id} user_id={user_id} "
        f"action={action} details={details or {}}"
    )


def log_error(error: Exception, context: dict = None):
    """
    Log error with context

    Args:
        error: Exception that occurred
        context: Additional context
    """
    logger.error(
        f"Error: {type(error).__name__} - {str(error)} "
        f"context={context or {}}"
    )


def log_security_event(event_type: str, user_id: int = None, details: dict = None):
    """
    Log security-related events

    Args:
        event_type: Type of security event
        user_id: User involved (if applicable)
        details: Additional details
    """
    logger.warning(
        f"Security Event | type={event_type} user_id={user_id} "
        f"details={details or {}}"
    )
