# src/main.py

import os

# CRITICAL: Load environment variables FIRST, before any other imports
# that might use them at import time
from dotenv import load_dotenv

load_dotenv()

# Now safe to import modules that use environment variables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router

app = FastAPI(
    title="Website Redesign Agent",
    description="AI-powered website redesign generator using Cua and Gemini",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "Website Redesign Agent API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "/api/redesign": "POST - Redesign a website",
            "/api/screenshot": "POST - Capture website screenshots",
            "/api/health": "GET - Health check",
            "/docs": "GET - Interactive API documentation",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )

