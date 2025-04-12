from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.api_v1.api import api_router
from app.serve_frontend import mount_frontend
import os
import logging
import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
import mimetypes

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
    db_url = settings.get_database_url()
    
    # Create a safe version for logging that hides credentials
    try:
        safe_db_url = db_url.replace(db_url.split("@")[0], "postgresql://****:****")
        print(f"Database URL format: {safe_db_url}")
    except Exception:
        print("Unable to parse database URL for safe logging")
    
    engine = create_engine(db_url)
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("Database connection test query successful!")
    print("Database connection successful!")
    print("="*50)
except ValueError as e:
    print("="*50)
    print(f"Database configuration error: {str(e)}")
    print("="*50)
except SQLAlchemyError as e:
    print("="*50)
    print(f"Database connection error: {str(e)}")
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

# Mount frontend first
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
logger.info(f"Checking frontend directory: {frontend_dir}")
if os.path.exists(frontend_dir):
    logger.info(f"Frontend directory exists. Contents: {os.listdir(frontend_dir)}")
    assets_dir = os.path.join(frontend_dir, "assets")
    if os.path.exists(assets_dir):
        logger.info(f"Assets directory exists. Contents: {os.listdir(assets_dir)}")
    mount_frontend(app)
else:
    logger.error("Frontend directory not found!")

# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        # Test database connection
        engine = create_engine(settings.get_database_url())
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        db_status = "unhealthy"

    return {
        "status": "healthy",
        "database": db_status,
        "environment": os.getenv("ENVIRONMENT", "development")
    }

# Include API router last
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