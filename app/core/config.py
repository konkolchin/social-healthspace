from decouple import config

class Settings:
    PROJECT_NAME: str = "Social HealthSpace"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Try DATABASE_URL first, then SQLALCHEMY_DATABASE_URI
    DATABASE_URL: str = config('DATABASE_URL', default=None)
    SQLALCHEMY_DATABASE_URI: str = config('SQLALCHEMY_DATABASE_URI', default=None)
    
    # Make individual Postgres settings optional
    POSTGRES_SERVER: str = config('POSTGRES_SERVER', default=None)
    POSTGRES_USER: str = config('POSTGRES_USER', default=None)
    POSTGRES_PASSWORD: str = config('POSTGRES_PASSWORD', default=None)
    POSTGRES_DB: str = config('POSTGRES_DB', default=None)
    
    @property
    def database_url(self) -> str:
        """Get the database URL with proper error handling."""
        if not self.DATABASE_URL:
            raise ValueError(
                "DATABASE_URL environment variable is not set. "
                "Please set it using: fly secrets set DATABASE_URL=your_database_url"
            )
        return self.DATABASE_URL
    
    JWT_SECRET_KEY: str = config('JWT_SECRET_KEY')
    JWT_ALGORITHM: str = config('JWT_ALGORITHM', default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config('ACCESS_TOKEN_EXPIRE_MINUTES', default=30, cast=int)

settings = Settings() 