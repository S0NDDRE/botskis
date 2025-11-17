"""
Rate Limiting Configuration for Mindframe API

Defines rate limits for different endpoint categories to prevent abuse
and ensure fair usage of system resources.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from functools import wraps
from typing import Callable
import redis
from config.settings import settings

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200/hour"],  # Default limit for all endpoints
    storage_uri=getattr(settings, 'redis_url', 'memory://'),  # Use Redis if available
    enabled=not getattr(settings, 'disable_rate_limiting', False)
)


# ============================================================================
# RATE LIMIT CONFIGURATIONS
# ============================================================================

class RateLimits:
    """
    Centralized rate limit definitions for different endpoint categories

    Format: "X per Y"
    Where X = number of requests, Y = time period (second, minute, hour, day)
    """

    # Authentication endpoints (stricter limits to prevent brute force)
    AUTH_LOGIN = "5/minute"  # 5 login attempts per minute
    AUTH_REGISTER = "3/hour"  # 3 registrations per hour
    AUTH_PASSWORD_RESET = "3/hour"  # 3 password reset requests per hour
    AUTH_REFRESH_TOKEN = "10/minute"  # 10 token refreshes per minute

    # Public endpoints (moderate limits)
    PUBLIC_READ = "100/hour"  # Read-only public endpoints
    PUBLIC_WRITE = "30/hour"  # Write operations for unauthenticated users

    # Authenticated user endpoints
    USER_READ = "300/hour"  # Read operations for authenticated users
    USER_WRITE = "100/hour"  # Write operations for authenticated users
    USER_DELETE = "20/hour"  # Delete operations (more restrictive)

    # AI/ML endpoints (expensive operations)
    AI_GENERATION = "10/minute"  # AI agent generation
    AI_PREDICTION = "30/minute"  # AI predictions/analysis
    AI_TRAINING = "5/hour"  # Model training requests

    # Voice AI endpoints (expensive Twilio operations)
    VOICE_CALL_OUTBOUND = "10/hour"  # Outbound calls
    VOICE_FLOW_GENERATION = "20/hour"  # Voice flow generation
    VOICE_TESTING = "30/hour"  # Voice testing

    # Marketplace endpoints
    MARKETPLACE_READ = "200/hour"  # Browse marketplace
    MARKETPLACE_DEPLOY = "50/hour"  # Deploy agents
    MARKETPLACE_PUBLISH = "10/hour"  # Publish new agents

    # Academy endpoints
    ACADEMY_READ = "300/hour"  # Read course content
    ACADEMY_QUIZ = "100/hour"  # Submit quiz answers
    ACADEMY_AI_ASSISTANT = "50/hour"  # Ask AI course assistant

    # Meta-AI Guardian endpoints (admin/premium only)
    META_AI_ANALYZE = "10/hour"  # Code analysis
    META_AI_FIX = "5/hour"  # Auto-fix issues
    META_AI_REPORT = "20/hour"  # Generate reports

    # WebSocket connections
    WEBSOCKET_CONNECT = "100/hour"  # WebSocket connection attempts
    WEBSOCKET_MESSAGE = "1000/hour"  # Messages per hour per connection

    # Monitoring endpoints
    MONITORING_READ = "500/hour"  # Read monitoring data
    MONITORING_WRITE = "100/hour"  # Write monitoring events

    # Health check (very generous)
    HEALTH_CHECK = "1000/hour"  # Health check endpoint


# ============================================================================
# RATE LIMIT DECORATORS
# ============================================================================

def rate_limit(limit: str):
    """
    Decorator to apply rate limiting to an endpoint

    Usage:
        @app.get("/api/v1/example")
        @rate_limit(RateLimits.USER_READ)
        async def example():
            pass

    Args:
        limit: Rate limit string (e.g., "10/minute")

    Returns:
        Decorated function with rate limiting applied
    """
    def decorator(func: Callable):
        @wraps(func)
        @limiter.limit(limit)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def get_rate_limit_for_tier(tier: str, base_limit: str) -> str:
    """
    Adjust rate limit based on subscription tier

    Args:
        tier: Subscription tier (free, pro, enterprise)
        base_limit: Base rate limit string

    Returns:
        Adjusted rate limit string
    """
    # Parse base limit
    count, period = base_limit.split("/")
    count = int(count)

    # Multipliers for different tiers
    multipliers = {
        "free": 1.0,
        "pro": 5.0,  # 5x more requests
        "enterprise": 20.0  # 20x more requests
    }

    multiplier = multipliers.get(tier.lower(), 1.0)
    new_count = int(count * multiplier)

    return f"{new_count}/{period}"


def apply_tiered_rate_limit(tier: str, limit: str):
    """
    Apply rate limit that scales with subscription tier

    Usage:
        @app.get("/api/v1/premium")
        @apply_tiered_rate_limit("pro", RateLimits.AI_GENERATION)
        async def premium_endpoint(current_user: User):
            pass
    """
    def decorator(func: Callable):
        adjusted_limit = get_rate_limit_for_tier(tier, limit)
        return rate_limit(adjusted_limit)(func)
    return decorator


# ============================================================================
# CUSTOM RATE LIMIT KEY FUNCTIONS
# ============================================================================

def get_user_id_key(request) -> str:
    """
    Rate limit by user ID instead of IP address

    Use this for authenticated endpoints to prevent multi-IP abuse
    """
    try:
        # Try to get user from request state (set by auth middleware)
        if hasattr(request.state, "user"):
            return f"user:{request.state.user.id}"
    except:
        pass

    # Fallback to IP address
    return get_remote_address(request)


def get_api_key_key(request) -> str:
    """
    Rate limit by API key

    Use this for API key-based authentication
    """
    api_key = request.headers.get("X-API-Key", "")
    if api_key:
        return f"apikey:{api_key}"

    # Fallback to IP address
    return get_remote_address(request)


# ============================================================================
# RATE LIMIT BYPASS (for testing)
# ============================================================================

def bypass_rate_limit_if_testing():
    """
    Decorator to bypass rate limiting in test environment

    Usage:
        @app.get("/api/v1/example")
        @bypass_rate_limit_if_testing()
        @rate_limit(RateLimits.USER_READ)
        async def example():
            pass
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Check if in test mode
            if getattr(settings, 'environment', '') == 'test':
                return await func(*args, **kwargs)

            # Normal rate limiting applies
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# ============================================================================
# RATE LIMIT INFO ENDPOINT HELPERS
# ============================================================================

def get_rate_limit_status(request) -> dict:
    """
    Get current rate limit status for a request

    Returns:
        dict with:
            - limit: Total allowed requests
            - remaining: Requests remaining
            - reset: Time when limit resets
    """
    # This would integrate with slowapi to get current status
    # For now, return structure
    return {
        "limit": 100,
        "remaining": 95,
        "reset": "2024-01-01T12:00:00Z"
    }


# ============================================================================
# REDIS-BASED RATE LIMITING (for distributed systems)
# ============================================================================

class RedisRateLimiter:
    """
    Redis-based rate limiter for distributed systems

    Use this when running multiple API instances
    """

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def check_rate_limit(
        self,
        key: str,
        limit: int,
        window_seconds: int
    ) -> bool:
        """
        Check if request is within rate limit

        Args:
            key: Unique key for this rate limit (e.g., user ID, IP)
            limit: Maximum requests allowed
            window_seconds: Time window in seconds

        Returns:
            True if within limit, False if exceeded
        """
        current_time = int(time.time())
        window_key = f"ratelimit:{key}:{current_time // window_seconds}"

        # Increment counter
        current_count = self.redis.incr(window_key)

        # Set expiry on first request
        if current_count == 1:
            self.redis.expire(window_key, window_seconds)

        # Check if within limit
        return current_count <= limit

    async def get_remaining(
        self,
        key: str,
        limit: int,
        window_seconds: int
    ) -> int:
        """Get remaining requests in current window"""
        current_time = int(time.time())
        window_key = f"ratelimit:{key}:{current_time // window_seconds}"

        current_count = self.redis.get(window_key)
        current_count = int(current_count) if current_count else 0

        remaining = max(0, limit - current_count)
        return remaining


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'limiter',
    'RateLimits',
    'rate_limit',
    'apply_tiered_rate_limit',
    'get_rate_limit_for_tier',
    'get_user_id_key',
    'get_api_key_key',
    'bypass_rate_limit_if_testing',
    'get_rate_limit_status',
    'RedisRateLimiter'
]
