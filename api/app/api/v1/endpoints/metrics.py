"""
Metrics endpoint for observability.
"""
from typing import Optional
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.core.metrics import metrics
from app.models.tenant import Tenant

router = APIRouter()


@router.get("/")
async def get_metrics(
    current_tenant: Tenant = Depends(get_current_tenant),
    tenant_id: Optional[UUID] = Query(None, description="Filter by tenant ID (admin only)")
):
    """
    Get application metrics.
    Returns counters, timings, and gauges.
    """
    # For now, only return metrics for current tenant
    # In future, add admin role check for cross-tenant metrics
    metrics_data = await metrics.get_metrics_summary(tenant_id=current_tenant.id)
    
    return {
        "tenant_id": str(current_tenant.id),
        "metrics": metrics_data,
        "timestamp": datetime.utcnow().isoformat()
    }

