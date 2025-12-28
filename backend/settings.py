"""Centralized application settings using Pydantic BaseSettings.

Loads environment variables from a .env file (already handled early in main)
but provides a single import location to access configuration across the
backend.
"""

from functools import lru_cache
from typing import Optional

from pydantic import Field

try:
    from pydantic_settings import BaseSettings  # Pydantic v2 separate package
except ImportError:  # Fallback if installed differently
    from pydantic import BaseSettings  # type: ignore


class Settings(BaseSettings):
    """Application configuration settings loaded from environment variables."""

    # Core API / LLM
    openai_api_key: Optional[str] = Field(
        default=None, alias="OPENAI_API_KEY", description="OpenAI API key"
    )

    # Langfuse observability
    langfuse_public_key: Optional[str] = Field(
        default=None,
        alias="LANGFUSE_PUBLIC_KEY",
        description="Langfuse public key",
    )
    langfuse_secret_key: Optional[str] = Field(
        default=None,
        alias="LANGFUSE_SECRET_KEY",
        description="Langfuse secret key",
    )
    langfuse_host: Optional[str] = Field(
        default=None,
        alias="LANGFUSE_HOST",
        description="Langfuse host base URL",
    )

    # Application metadata
    app_name: str = "Trip Planner Agent API"
    environment: str = Field(
        default="local",
        alias="ENVIRONMENT",
        description="Deployment environment",
    )

    class Config:
        env_file = ".env"
        case_sensitive = False
        populate_by_name = True
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:  # pragma: no cover - trivial wrapper
    return Settings()  # type: ignore[arg-type]


settings = get_settings()
