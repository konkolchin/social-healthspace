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
    engine = create_engine(settings.DATABASE_URL)
    connection = engine.connect()
    print("Database connection successful!")
    connection.close()
except SQLAlchemyError as e:
    print(f"Database connection failed: {str(e)}")

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

# Include API router
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

@app.get(f"{settings.API_V1_STR}/health")
async def health_check():
    logger.debug("Health check endpoint called")
    try:
        # Perform actual database check
        db_status = "healthy"
        try:
            engine = create_engine(settings.DATABASE_URL)
            with engine.connect() as connection:
                connection.execute("SELECT 1")  # Simple query to test connection
        except SQLAlchemyError as e:
            logger.error(f"Database health check failed: {str(e)}")
            db_status = "unhealthy"
        
        return {
            "status": "healthy",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "port": os.getenv("PORT", "8000"),
            "database": db_status
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