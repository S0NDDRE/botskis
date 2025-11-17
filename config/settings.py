"""
Application settings and configuration
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # App
    app_name: str = "Mindframe"
    environment: str = "development"
    debug: bool = True
    secret_key: str
    api_version: str = "v1"

    # Database
    database_url: str
    database_pool_size: int = 20
    database_max_overflow: int = 0

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # AI
    openai_api_key: str
    # Default model for OpenAI requests. Set to Raptor mini (Preview) to use the new lightweight model for all clients.
    openai_model: str = "raptor-mini-preview"
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-opus-20240229"

    # Stripe
    stripe_secret_key: str
    stripe_publishable_key: str
    stripe_webhook_secret: str

    # Email
    sendgrid_api_key: str
    from_email: str = "noreply@mindframe.ai"

    # Monitoring
    sentry_dsn: Optional[str] = None
    prometheus_port: int = 9090

    # Features
    enable_marketplace: bool = True
    enable_auto_healing: bool = True
    enable_analytics: bool = True

    # Server
    port: int = 8000
    workers: int = 4
    log_level: str = "info"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
