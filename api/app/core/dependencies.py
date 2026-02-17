from typing import Optional
from uuid import UUID
from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.exceptions import TenantNotFoundException, InvalidTenantException
from app.models.tenant import Tenant

async def get_current_tenant(
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID"),
    db: AsyncSession = Depends(get_db)
) -> Tenant:
    """
    Validate X-Tenant-ID header and return valid Tenant object.
    If header is missing, returns the first active tenant (for demo purposes).
    Raises TenantNotFoundException or InvalidTenantException.
    """
    # If no tenant ID provided, use first active tenant (demo mode)
    if not x_tenant_id:
        result = await db.execute(
            select(Tenant).where(Tenant.is_active == True).limit(1)
        )
        tenant = result.scalar_one_or_none()
        
        if not tenant:
            raise TenantNotFoundException()
        
        return tenant
    
    # Original validation logic
    try:
        tenant_uuid = UUID(x_tenant_id)
    except ValueError:
        raise InvalidTenantException()

    # Query tenant from DB
    result = await db.execute(select(Tenant).where(Tenant.id == tenant_uuid))
    tenant = result.scalar_one_or_none()

    if not tenant:
        raise TenantNotFoundException()
    
    if not tenant.is_active:
        raise TenantNotFoundException()  # Treat inactive as not found for security

    return tenant
