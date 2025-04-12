from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

def mount_frontend(app: FastAPI):
    """Configure the FastAPI app to serve the frontend"""
    # Serve static files from the frontend build
    static_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
    if os.path.exists(static_dir):
        # Mount the assets directory for static files (JS, CSS, etc.)
        app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")
        
        @app.get("/{full_path:path}")
        async def serve_frontend(full_path: str):
            # Don't handle API routes
            if full_path.startswith("api/"):
                raise HTTPException(status_code=404, detail="Not found")
            # Serve index.html for all other routes
            return FileResponse(os.path.join(static_dir, "index.html"))