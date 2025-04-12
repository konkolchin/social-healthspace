from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import mimetypes
import logging

logger = logging.getLogger(__name__)

# Ensure correct MIME types for Vite assets
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("application/javascript", ".mjs")
mimetypes.add_type("text/css", ".css")

def mount_frontend(app: FastAPI):
    """Configure the FastAPI app to serve the frontend"""
    static_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
    
    if not os.path.exists(static_dir):
        logger.error(f"Frontend build directory not found at {static_dir}")
        return
    
    logger.info(f"Mounting frontend from {static_dir}")
    
    # Mount the static files directory
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets"), html=True), name="assets")
    
    @app.get("/")
    async def serve_spa(request):
        return FileResponse(os.path.join(static_dir, "index.html"))
    
    @app.get("/{full_path:path}")
    async def serve_spa_paths(full_path: str):
        # Skip API routes
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not found")
            
        # Try to serve the exact file if it exists
        file_path = os.path.join(static_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path, media_type=mimetypes.guess_type(file_path)[0])
            
        # Fall back to index.html for client-side routing
        return FileResponse(os.path.join(static_dir, "index.html"))