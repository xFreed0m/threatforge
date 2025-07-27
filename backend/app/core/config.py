"""Application configuration settings."""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""
    
    # API Keys
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key for GPT models"
    )
    anthropic_api_key: Optional[str] = Field(
        default=None,
        description="Anthropic API key for Claude models"
    )
    
    # Database
    database_url: str = "sqlite:///./threatforge.db"
    
    # Security
    secret_key: str = Field(
        default="test-secret-key-for-development",
        description="Secret key for JWT tokens and encryption"
    )
    
    # App
    environment: str = Field(
        default="development",
        description="Application environment (development, production, etc.)"
    )
    app_name: str = Field(
        default="ThreatForge",
        description="Application name"
    )
    
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Global settings instance
settings = Settings()
