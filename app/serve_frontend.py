from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import logging

logger = logging.getLogger(__name__)

def mount_frontend(app: FastAPI):
    """Configure the FastAPI app to serve the frontend"""
    # Serve static files from the frontend build
    static_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
    
    if not os.path.exists(static_dir):
        logger.error(f"Frontend build directory not found at {static_dir}")
        return
    
    logger.info(f"Mounting frontend from {static_dir}")
    
    # Mount the assets directory for static files (JS, CSS, etc.)
    assets_dir = os.path.join(static_dir, "assets")
    if os.path.exists(assets_dir):
        logger.info(f"Mounting assets from {assets_dir}")
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    
    @app.get("/")
    async def serve_root():
        logger.info("Serving root path")
        return FileResponse(os.path.join(static_dir, "index.html"))
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        logger.info(f"Serving path: {full_path}")
        
        # Don't handle API routes
        if full_path.startswith("api/"):
            logger.debug(f"Skipping API route: {full_path}")
            raise HTTPException(status_code=404, detail="Not found")
        
        # Check if the path exists as a file (for assets)
        file_path = os.path.join(static_dir, full_path)
        if os.path.isfile(file_path):
            logger.debug(f"Serving file: {file_path}")
            return FileResponse(file_path)
        
        # Serve index.html for all other routes (SPA routing)
        logger.debug(f"Serving index.html for path: {full_path}")
        return FileResponse(os.path.join(static_dir, "index.html"))