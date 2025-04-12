from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings
from decouple import config
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    PROJECT_NAME: str = "Social HealthSpace"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Try DATABASE_URL first, then SQLALCHEMY_DATABASE_URI
    DATABASE_URL: Optional[str] = config('DATABASE_URL', default=None)
    SQLALCHEMY_DATABASE_URI: str = config('SQLALCHEMY_DATABASE_URI', default=None)
    
    # Make individual Postgres settings optional
    POSTGRES_SERVER: Optional[str] = config('POSTGRES_SERVER', default=None)
    POSTGRES_USER: Optional[str] = config('POSTGRES_USER', default=None)
    POSTGRES_PASSWORD: Optional[str] = config('POSTGRES_PASSWORD', default=None)
    POSTGRES_DB: Optional[str] = config('POSTGRES_DB', default=None)
    POSTGRES_PORT: Optional[str] = config('POSTGRES_PORT', default=None)

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

    JWT_SECRET_KEY: str = config('JWT_SECRET_KEY')
    JWT_ALGORITHM: str = config('JWT_ALGORITHM', default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config('ACCESS_TOKEN_EXPIRE_MINUTES', default=30, cast=int)

    class Config:
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings() 