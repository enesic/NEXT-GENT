from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import Dict, Any

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events to prevent memory leaks.
    """
    # Startup
    print("🚀 Starting up application (Expert Fix)...")
    print("✅ Redis connection pool initialized")
    print("✅ HTTP client pool initialized")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down application...")
    
    # Close Redis connections
    try:
        from app.core.redis import redis_manager
        await redis_manager.close()
        print("✅ Redis connections closed")
    except Exception as e:
        print(f"⚠️ Error closing Redis: {e}")
    
    # Close HTTP client
    try:
        from app.core.http_client import http_client_manager
        await http_client_manager.close()
        print("✅ HTTP client closed")
    except Exception as e:
        print(f"⚠️ Error closing HTTP client: {e}")
    
    # Close database connections
    try:
        from app.core.database import engine
        await engine.dispose()
        print("✅ Database connections closed")
    except Exception as e:
        print(f"⚠️ Error closing database: {e}")
    
    print("✅ Shutdown complete")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG,
    lifespan=lifespan  # Add lifespan manager
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
# Allows frontend (port 5173) and custom tenant headers
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS] + ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost", "http://127.0.0.1", "http://localhost:80"],
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
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
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
        await redis_client.ping()
        health_status["checks"]["redis"] = {
            "status": "healthy",
            "message": "Redis connection successful"
        }
    except Exception as e:
        overall_healthy = False
        health_status["checks"]["redis"] = {
            "status": "unhealthy",
            "message": f"Redis connection failed: {str(e)}"
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

