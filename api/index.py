"""
Vercel Serverless Function for NextGent Backend
Main entry point that handles all API routes
"""
import os
import sys

# Set environment variables for production
os.environ["ENVIRONMENT"] = "production"
os.environ["DEBUG"] = "false"

# Database configuration from Neon.tech
os.environ["DATABASE_URL"] = "postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

# Security keys
os.environ["SECRET_KEY"] = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
os.environ["ENCRYPTION_KEY"] = "fXACJ43AmGdLJSumrunA2mUtLpD12RTqaAMsu5CEzsU="

# CORS
os.environ["BACKEND_CORS_ORIGINS"] = "https://www.nextgent.co,https://nextgent.co,http://localhost:5173"

# Optional Redis (empty for Vercel)
os.environ["REDIS_HOST"] = ""
os.environ["REDIS_PORT"] = "6379"
os.environ["REDIS_PASSWORD"] = ""

try:
    from app.main import app
    from mangum import Mangum
    
    # Create Mangum handler for Vercel
    handler = Mangum(app, lifespan="off")
    
except Exception as e:
    print(f"Error importing FastAPI app: {e}")
    
    # Fallback minimal app
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    from mangum import Mangum
    
    fallback_app = FastAPI(title="NextGent API - Error State")
    
    @fallback_app.get("/api/v1/health")
    async def health_error():
        return JSONResponse({
            "status": "error",
            "message": f"Backend initialization failed: {str(e)}",
            "database": "disconnected"
        }, status_code=503)
    
    handler = Mangum(fallback_app, lifespan="off")