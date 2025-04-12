from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.api_v1.api import api_router
from app.serve_frontend import mount_frontend  # Add this import
import os
import logging
import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Configure logging to stdout
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Print basic startup info
print("="*50)
print("Starting application...")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")
print("="*50)

# Test database connection
try:
    print("="*50)
    print("Attempting database connection...")
    db_url = settings.get_database_url
    # Create a safe version for logging that hides credentials
    safe_db_url = db_url.replace(db_url.split("@")[0], "postgresql://****:****")
    print(f"Database URL format: {safe_db_url}")
    
    engine = create_engine(db_url)
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        print("Database connection test query successful!")
    print("Database connection successful!")
    print("="*50)
except ValueError as e:
    print("="*50)
    print("Database configuration error:")
    print(str(e))
    print("="*50)
except SQLAlchemyError as e:
    print("="*50)
    print("Database connection error:")
    print(str(e))
    print("="*50)
except Exception as e:
    print("="*50)
    print("Unexpected error during database connection:")
    print(str(e))
    print("="*50)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for the Social HealthSpace social network",
    version=settings.VERSION,
)

# Log startup information
logger.debug(f"Starting application with settings: {settings}")
logger.debug(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
logger.debug(f"PORT: {os.getenv('PORT', '8000')}")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# mou
mount_frontend(app)

# Move the health check endpoint before including the API router
@app.get("/health")  # This will be the main health check endpoint
async def health_check():
    logger.debug("Health check endpoint called")
    try:
        # Get database URL and create a safe version for logging
        db_url = settings.get_database_url
        # Create a safe version that hides credentials
        safe_db_url = db_url.replace(db_url.split("@")[0], "postgresql://****:****")
        logger.debug(f"Database URL format: {safe_db_url}")
        
        # Perform actual database check
        db_status = "healthy"
        try:
            engine = create_engine(db_url)
            with engine.connect() as connection:
                connection.execute("SELECT 1")
        except SQLAlchemyError as e:
            logger.error(f"Database health check failed: {str(e)}")
            db_status = "unhealthy"
        
        return {
            "status": "healthy",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "port": os.getenv("PORT", "8000"),
            "database": db_status,
            "database_url_format": safe_db_url  # This will show the format without credentials
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )

# Include API router after defining the health check
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

@app.get("/")
async def root():
    logger.debug("Root endpoint called")
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"} 