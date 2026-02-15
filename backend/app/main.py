from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any
from sqlalchemy import text

from app.core.config import settings
from app.core.exceptions import (
    TenantNotFoundException,
    InvalidTenantException,
    tenant_not_found_exception_handler,
    invalid_tenant_exception_handler,
    global_exception_handler
)
from app.core.middleware import (
    RequestIDMiddleware,
    SecurityHeadersMiddleware,
    RateLimitMiddleware,
    PerformanceMonitoringMiddleware,
    ErrorHandlingMiddleware
)
from app.api.v1.api import api_router

# Serverless-optimized FastAPI app
# No lifespan manager needed - Vercel handles function lifecycle
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG,
)

# ============================================================================
# ENTERPRISE MIDDLEWARE STACK
# ============================================================================
# Order matters! Middleware is executed in reverse order (last added = first executed)
# 1. ErrorHandlingMiddleware (outermost - catches all errors)
# 2. PerformanceMonitoringMiddleware (tracks request time)
# 3. RateLimitMiddleware (rate limiting)
# 4. SecurityHeadersMiddleware (security headers)
# 5. RequestIDMiddleware (innermost - adds request ID)

app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(PerformanceMonitoringMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestIDMiddleware)

# ============================================================================
# ENTERPRISE CORS CONFIGURATION
# ============================================================================
# Configure CORS with enterprise-level security settings
# Supports both local development and production (Vercel) deployments
# 
# For production deployment:
# Set BACKEND_CORS_ORIGINS environment variable with your domains:
# BACKEND_CORS_ORIGINS=https://your-domain.vercel.app,https://your-custom-domain.com

# Build allowed origins list
allowed_origins = [
    "http://localhost:5173",      # Local dev (Vite)
    "http://127.0.0.1:5173",
    "http://localhost",            # Local dev (Docker)
    "http://127.0.0.1",
    "http://localhost:80",
    "https://nextgent.co",         # Production
    "https://www.nextgent.co",     # Production (www)
]

# Add configured origins from environment
if settings.BACKEND_CORS_ORIGINS:
    allowed_origins.extend([str(origin) for origin in settings.BACKEND_CORS_ORIGINS])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-Tenant-ID",  # Custom tenant identification header
        "X-Request-ID",
        "Accept",
        "Origin",
        "User-Agent",
        "DNT",
        "Cache-Control",
        "X-Requested-With",
    ],
    expose_headers=[
        "X-Request-ID",
        "X-Tenant-ID",
        "X-RateLimit-Limit",
        "X-RateLimit-Remaining",
        "X-RateLimit-Reset",
    ],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Exception Handlers
app.add_exception_handler(TenantNotFoundException, tenant_not_found_exception_handler)
app.add_exception_handler(InvalidTenantException, invalid_tenant_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

@app.get("/")
async def root():
    """Root endpoint - API welcome message"""
    return {
        "message": "Welcome to NextGent API",
        "version": "1.0.0",
        "docs": f"{settings.API_V1_STR}/docs",
        "health": f"{settings.API_V1_STR}/health"
    }


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================
@app.get(f"{settings.API_V1_STR}/health", tags=["Health"])
async def health_check() -> JSONResponse:
    """
    Enterprise health check endpoint.
    Monitors database and Redis connectivity status.
    
    Returns:
        JSONResponse: Comprehensive health status including:
            - Overall status
            - Database connection status
            - Redis connection status
            - Timestamp
    """
    health_status: Dict[str, Any] = {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "checks": {}
    }
    
    overall_healthy = True
    
    # Check Database Connection
    try:
        from app.core.database import engine
        if engine is None:
            overall_healthy = False
            health_status["checks"]["database"] = {
                "status": "unhealthy",
                "message": "Database is not configured"
            }
        else:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            health_status["checks"]["database"] = {
                "status": "healthy",
                "message": "PostgreSQL connection successful"
            }
    except Exception as e:
        overall_healthy = False
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}"
        }
    
    # Check Redis Connection
    try:
        from app.core.redis import redis_manager
        redis_client = await redis_manager.get_client()
        if redis_client is None:
            health_status["checks"]["redis"] = {
                "status": "optional",
                "message": "Redis not configured; continuing without cache"
            }
        else:
            await redis_client.ping()
            health_status["checks"]["redis"] = {
                "status": "healthy",
                "message": "Redis connection successful"
            }
    except Exception as e:
        health_status["checks"]["redis"] = {
            "status": "optional_error",
            "message": f"Redis unavailable; continuing without cache: {str(e)}"
        }
    
    # Set overall status
    if not overall_healthy:
        health_status["status"] = "degraded"
    
    # Return appropriate status code
    status_code = status.HTTP_200_OK if overall_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return JSONResponse(
        status_code=status_code,
        content=health_status
    )

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Vercel serverless function export
# This makes the app compatible with Vercel's Python runtime
handler = app