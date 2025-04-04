from decouple import config

class Settings:
    PROJECT_NAME: str = "Social HealthSpace"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_SERVER: str = config('POSTGRES_SERVER')
    POSTGRES_USER: str = config('POSTGRES_USER')
    POSTGRES_PASSWORD: str = config('POSTGRES_PASSWORD')
    POSTGRES_DB: str = config('POSTGRES_DB')
    SQLALCHEMY_DATABASE_URI: str = config('SQLALCHEMY_DATABASE_URI', default=None)
    
    @property
    def get_database_url(self) -> str:
        if self.SQLALCHEMY_DATABASE_URI:
            return self.SQLALCHEMY_DATABASE_URI
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
    
    JWT_SECRET_KEY: str = config('JWT_SECRET_KEY')
    JWT_ALGORITHM: str = config('JWT_ALGORITHM', default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config('ACCESS_TOKEN_EXPIRE_MINUTES', default=30, cast=int)

settings = Settings() 