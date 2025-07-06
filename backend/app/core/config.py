from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Database
    database_url: str = "sqlite:///./threatforge.db"
    
    # Security
    secret_key: str
    
    # App
    environment: str = "development"
    app_name: str = "ThreatForge"
    
    class Config:
        env_file = ".env"

settings = Settings()
