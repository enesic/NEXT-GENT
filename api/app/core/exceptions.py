from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Any, Dict

class TenantNotFoundException(Exception):
    pass

class InvalidTenantException(Exception):
    pass

async def tenant_not_found_exception_handler(request: Request, exc: TenantNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "Tenant not found or invalid tenant ID"},
    )

async def invalid_tenant_exception_handler(request: Request, exc: InvalidTenantException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "Invalid Tenant ID format"},
    )

async def global_exception_handler(request: Request, exc: Exception):
    # Log the error here if needed
    print(f"Global error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )
