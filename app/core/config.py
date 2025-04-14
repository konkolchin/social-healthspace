from functools import lru_cache
from typing import Optional
from pydantic import BaseSettings  # Note: Use BaseSettings instead of BaseModel for Pydantic v1
import os
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    PROJECT_NAME: str = "Social HealthSpace"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database configuration
    DATABASE_URL: Optional[str] = os.getenv('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI: Optional[str] = os.getenv('SQLALCHEMY_DATABASE_URI')
    
    # JWT Configuration (keep these)
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', 'your-secret-key')  # Default for development
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))

    @property
    def database_url(self) -> str:
        """Get the database URL with proper protocol handling"""
        url = self.DATABASE_URL or self.SQLALCHEMY_DATABASE_URI
        if not url:
            raise ValueError("No database URL configured")
        return url.replace('postgres://', 'postgresql://', 1)

    class Config:
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()