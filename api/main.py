"""
Main Vercel Serverless Function - FastAPI Backend
Handles all API routes for NextGent system
"""
import os
import sys
from pathlib import Path

# Add backend to Python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Set environment variables for production
os.environ["ENVIRONMENT"] = "production"
os.environ["DEBUG"] = "false"
os.environ["DATABASE_URL"] = "postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"
os.environ["SECRET_KEY"] = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
os.environ["ENCRYPTION_KEY"] = "fXACJ43AmGdLJSumrunA2mUtLpD12RTqaAMsu5CEzsU="
os.environ["BACKEND_CORS_ORIGINS"] = "https://www.nextgent.co,https://nextgent.co,http://localhost:5173"
os.environ["REDIS_HOST"] = ""
os.environ["REDIS_PORT"] = "6379"
os.environ["REDIS_PASSWORD"] = ""

try:
    # Import the full FastAPI app
    from app.main import app
    from mangum import Mangum
    
    # Create Mangum handler for Vercel
    handler = Mangum(app, lifespan="off")
    
    # Export the app for direct access too
    app = app
    
except Exception as e:
    print(f"Error importing FastAPI app: {e}")
    import traceback
    traceback.print_exc()
    
    # Fallback minimal app
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from mangum import Mangum
    
    app = FastAPI(
        title="NextGent API - Fallback",
        description="Fallback API when main app fails to load",
        version="1.0.0"
    )
    
    # Add CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://www.nextgent.co", "https://nextgent.co", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/api/v1/health")
    async def health_error():
        return JSONResponse({
            "status": "error",
            "message": f"Backend initialization failed: {str(e)}",
            "database": "disconnected"
        }, status_code=503)
    
    handler = Mangum(app, lifespan="off")