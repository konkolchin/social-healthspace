from functools import lru_cache
from typing import Optional
from pydantic import BaseModel
import os
import logging

logger = logging.getLogger(__name__)

class Settings(BaseModel):
    PROJECT_NAME: str = "Social HealthSpace"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Try DATABASE_URL first, then SQLALCHEMY_DATABASE_URI
    DATABASE_URL: Optional[str] = os.getenv('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI: str = os.getenv('SQLALCHEMY_DATABASE_URI')
    
    # Make individual Postgres settings optional
    POSTGRES_SERVER: Optional[str] = os.getenv('POSTGRES_SERVER')
    POSTGRES_USER: Optional[str] = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: Optional[str] = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB: Optional[str] = os.getenv('POSTGRES_DB')
    POSTGRES_PORT: Optional[str] = os.getenv('POSTGRES_PORT')

    def get_database_url(self) -> str:
        """
        Get the database URL, converting postgres:// to postgresql:// if needed
        """
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            logger.info("Using DATABASE_URL environment variable")
        else:
            # Construct from individual components
            if not all([self.POSTGRES_USER, self.POSTGRES_PASSWORD, 
                       self.POSTGRES_SERVER, self.POSTGRES_PORT, self.POSTGRES_DB]):
                raise ValueError(
                    "Database configuration incomplete. Either set DATABASE_URL "
                    "or all of: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_SERVER, "
                    "POSTGRES_PORT, POSTGRES_DB"
                )
            url = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@" \
                  f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            logger.info("Using individual Postgres credentials")

        # Convert postgres:// to postgresql:// if needed
        if url.startswith('postgres://'):
            url = url.replace('postgres://', 'postgresql://', 1)
            logger.info("Converted postgres:// to postgresql:// in database URL")

        return url

    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', 'your-secret-key')  # Default for development
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))

    class Config:
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings() 