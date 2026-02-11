"""
Enterprise-grade middleware for security, performance, and observability.
"""
import time
import uuid
from typing import Callable
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.logger import get_logger
from app.core.redis import redis_manager

logger = get_logger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Adds unique request ID to every request for tracing.
    """
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate or get request ID
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        
        # Add to request state
        request.state.request_id = request_id
        
        # Process request
        response = await call_next(request)
        
        # Add to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adds security headers to all responses.
    """
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using Redis.
    Limits requests per tenant per minute.
    """
    RATE_LIMIT_PER_MINUTE = 100  # Requests per minute per tenant
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip rate limiting for health checks
        if request.url.path.endswith("/health"):
            return await call_next(request)
        
        # Get tenant ID from header
        tenant_id = request.headers.get("X-Tenant-ID")
        if not tenant_id:
            return await call_next(request)  # No tenant = no rate limit
        
        try:
            redis_client = await redis_manager.get_client()
            rate_limit_key = f"rate_limit:{tenant_id}:{int(time.time() / 60)}"
            
            # Increment counter
            current_count = await redis_client.incr(rate_limit_key)
            
            # Set expiration (1 minute)
            if current_count == 1:
                await redis_client.expire(rate_limit_key, 60)
            
            # Check limit
            if current_count > self.RATE_LIMIT_PER_MINUTE:
                logger.warning(
                    "rate_limit_exceeded",
                    tenant_id=tenant_id,
                    count=current_count,
                    limit=self.RATE_LIMIT_PER_MINUTE,
                    request_id=getattr(request.state, "request_id", "unknown")
                )
                
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "detail": "Rate limit exceeded",
                        "retry_after": 60,
                        "limit": self.RATE_LIMIT_PER_MINUTE
                    },
                    headers={
                        "X-RateLimit-Limit": str(self.RATE_LIMIT_PER_MINUTE),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(time.time()) + 60),
                        "Retry-After": "60"
                    }
                )
            
            # Add rate limit headers
            response = await call_next(request)
            response.headers["X-RateLimit-Limit"] = str(self.RATE_LIMIT_PER_MINUTE)
            response.headers["X-RateLimit-Remaining"] = str(self.RATE_LIMIT_PER_MINUTE - current_count)
            response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)
            
            return response
            
        except Exception as e:
            # If Redis fails, allow request (fail open)
            logger.error("rate_limit_error", error=str(e))
            return await call_next(request)


class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """
    Monitors request performance and logs slow requests.
    """
    SLOW_REQUEST_THRESHOLD_MS = 1000  # 1 second
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        request_id = getattr(request.state, "request_id", "unknown")
        tenant_id = request.headers.get("X-Tenant-ID", "unknown")
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000
        
        # Log performance
        if duration_ms > self.SLOW_REQUEST_THRESHOLD_MS:
            logger.warning(
                "slow_request",
                method=request.method,
                path=request.url.path,
                duration_ms=round(duration_ms, 2),
                status_code=response.status_code,
                tenant_id=tenant_id,
                request_id=request_id
            )
        else:
            logger.info(
                "request_completed",
                method=request.method,
                path=request.url.path,
                duration_ms=round(duration_ms, 2),
                status_code=response.status_code,
                tenant_id=tenant_id,
                request_id=request_id
            )
        
        # Add performance header
        response.headers["X-Response-Time-Ms"] = str(round(duration_ms, 2))
        
        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Catches unhandled exceptions and returns proper error responses.
    """
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            request_id = getattr(request.state, "request_id", "unknown")
            tenant_id = request.headers.get("X-Tenant-ID", "unknown")
            
            logger.error(
                "unhandled_exception",
                error=str(e),
                error_type=type(e).__name__,
                method=request.method,
                path=request.url.path,
                tenant_id=tenant_id,
                request_id=request_id
            )
            
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Internal server error",
                    "request_id": request_id,
                    "error_type": type(e).__name__
                }
            )



