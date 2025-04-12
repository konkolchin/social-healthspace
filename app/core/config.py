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
    def get_database_url(self) -> str:
        # First try DATABASE_URL
        if self.DATABASE_URL:
            print("Using DATABASE_URL for database connection")
            return self.DATABASE_URL
            
        # Then try SQLALCHEMY_DATABASE_URI
        if self.SQLALCHEMY_DATABASE_URI:
            print("Using SQLALCHEMY_DATABASE_URI for database connection")
            return self.SQLALCHEMY_DATABASE_URI
            
        # Finally, try to build from individual components
        if all([self.POSTGRES_SERVER, self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_DB]):
            print("Using individual PostgreSQL credentials for database connection")
            return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
            
        raise ValueError("""No valid database configuration found. 
            Current configuration:
            - DATABASE_URL: {'set' if self.DATABASE_URL else 'not set'}
            - SQLALCHEMY_DATABASE_URI: {'set' if self.SQLALCHEMY_DATABASE_URI else 'not set'}
            - Individual credentials: {'all set' if all([self.POSTGRES_SERVER, self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_DB]) else 'missing some'}
            """)
    
    JWT_SECRET_KEY: str = config('JWT_SECRET_KEY')
    JWT_ALGORITHM: str = config('JWT_ALGORITHM', default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config('ACCESS_TOKEN_EXPIRE_MINUTES', default=30, cast=int)

settings = Settings() 