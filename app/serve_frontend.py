from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import logging
import mimetypes

# Ensure correct MIME types are set
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("image/svg+xml", ".svg")

logger = logging.getLogger(__name__)

def mount_frontend(app: FastAPI):
    """Configure the FastAPI app to serve the frontend"""
    static_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
    
    if not os.path.exists(static_dir):
        logger.error(f"Frontend build directory not found at {static_dir}")
        return
    
    logger.info(f"Mounting frontend from {static_dir}")
    
    # Mount the static files directory for assets
    assets_dir = os.path.join(static_dir, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir, html=False), name="static")
    
    # Serve favicon.svg directly from static directory
    @app.get("/favicon.svg")
    async def serve_favicon():
        favicon_path = os.path.join(static_dir, "favicon.svg")
        if os.path.exists(favicon_path):
            return FileResponse(favicon_path, media_type="image/svg+xml")
        raise HTTPException(status_code=404)

    # Serve vite.svg directly from static directory
    @app.get("/vite.svg")
    async def serve_vite():
        vite_path = os.path.join(static_dir, "vite.svg")
        if os.path.exists(vite_path):
            return FileResponse(vite_path, media_type="image/svg+xml")
        raise HTTPException(status_code=404)
    
    # Serve index.html for the root path
    @app.get("/")
    async def serve_root():
        return FileResponse(os.path.join(static_dir, "index.html"), media_type="text/html")
    
    # Catch-all route for SPA routing
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Skip API routes
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404)
            
        # Try to serve static files first
        file_path = os.path.join(static_dir, full_path)
        if os.path.isfile(file_path):
            content_type, _ = mimetypes.guess_type(file_path)
            return FileResponse(file_path, media_type=content_type)
            
        # Fall back to index.html for client-side routing
        return FileResponse(os.path.join(static_dir, "index.html"), media_type="text/html")