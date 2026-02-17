from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.models.tenant import Tenant
from app.schemas.tenant import TenantResponse, TenantCreate

router = APIRouter()

@router.get("/me", response_model=TenantResponse)
async def read_current_tenant(
    current_tenant: Tenant = Depends(get_current_tenant),
) -> Any:
    """
    Get current tenant information based on X-Tenant-ID header.
    """
    return current_tenant

@router.post("/", response_model=TenantResponse)
async def create_tenant(
    *,
    db: AsyncSession = Depends(get_db),
    tenant_in: TenantCreate,
) -> Any:
    """
    Create a new tenant (Public endpoint for demo purposes).
    In real app, this should be an admin endpoint.
    """
    # Check if slug exists
    query = select(Tenant).where(Tenant.slug == tenant_in.slug)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="The tenant with this slug already exists in the system.",
        )
    
    tenant = Tenant(**tenant_in.model_dump())
    db.add(tenant)
    await db.commit()
    await db.refresh(tenant)
    return tenant
