from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# Add connection pool settings
engine = create_engine(
    settings.get_database_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,  # 30 seconds
    pool_recycle=1800  # 30 minutes
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        # Test the connection
        db.execute(text("SELECT 1"))
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database connection error: {str(e)}")
        raise
    finally:
        db.close() 