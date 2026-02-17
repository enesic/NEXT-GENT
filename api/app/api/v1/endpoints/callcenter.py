"""
Callcenter endpoints - Real-time call monitoring and management.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from pydantic import BaseModel

from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.models.tenant import Tenant
from app.models.interaction import Interaction, InteractionStatus
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


class CallStatus(BaseModel):
    call_id: str
    customer_name: str
    customer_phone: str
    status: str  # active, completed, failed
    duration_seconds: Optional[int] = None
    sentiment: Optional[str] = None
    transcript: Optional[str] = None
    started_at: datetime
    ended_at: Optional[datetime] = None


@router.get("/active-calls")
async def get_active_calls(
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """
    Get list of currently active calls.
    """
    # Query interactions with type="voice_call" and status="CONFIRMED" or "PENDING"
    query = select(Interaction).where(
        and_(
            Interaction.tenant_id == current_tenant.id,
            Interaction.type == "voice_call",
            Interaction.status.in_([InteractionStatus.CONFIRMED, InteractionStatus.PENDING]),
            Interaction.start_time <= datetime.utcnow(),
            Interaction.end_time >= datetime.utcnow()
        )
    ).order_by(Interaction.start_time.desc())
    
    result = await db.execute(query)
    interactions = result.scalars().all()
    
    calls = []
    for interaction in interactions:
        # Calculate duration
        duration = None
        if interaction.start_time:
            duration = int((datetime.utcnow() - interaction.start_time).total_seconds())
        
        calls.append({
            "call_id": str(interaction.id),
            "customer_name": interaction.client_name,
            "customer_phone": interaction.client_phone,
            "status": "active",
            "duration_seconds": duration,
            "sentiment": interaction.meta_data.get("sentiment") if interaction.meta_data else None,
            "transcript": interaction.meta_data.get("transcript") if interaction.meta_data else None,
            "started_at": interaction.start_time.isoformat(),
            "ended_at": None
        })
    
    return {
        "active_calls": calls,
        "count": len(calls)
    }


@router.get("/call-history")
async def get_call_history(
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    """
    Get call history with sentiment analysis.
    """
    query = select(Interaction).where(
        and_(
            Interaction.tenant_id == current_tenant.id,
            Interaction.type == "voice_call"
        )
    ).order_by(Interaction.start_time.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    interactions = result.scalars().all()
    
    calls = []
    for interaction in interactions:
        duration = None
        if interaction.start_time and interaction.end_time:
            duration = int((interaction.end_time - interaction.start_time).total_seconds())
        
        calls.append({
            "call_id": str(interaction.id),
            "customer_name": interaction.client_name,
            "customer_phone": interaction.client_phone,
            "status": interaction.status.value.lower(),
            "duration_seconds": duration,
            "sentiment": interaction.meta_data.get("sentiment") if interaction.meta_data else None,
            "transcript": interaction.meta_data.get("transcript")[:200] if interaction.meta_data and interaction.meta_data.get("transcript") else None,
            "started_at": interaction.start_time.isoformat(),
            "ended_at": interaction.end_time.isoformat() if interaction.end_time else None
        })
    
    return {
        "calls": calls,
        "total": len(calls)
    }


@router.get("/call-metrics")
async def get_call_metrics(
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    days: int = Query(30, ge=1, le=365)
):
    """
    Get call center metrics.
    """
    from datetime import timedelta
    from sqlalchemy import func
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Total calls
    total_query = select(func.count(Interaction.id)).where(
        and_(
            Interaction.tenant_id == current_tenant.id,
            Interaction.type == "voice_call",
            Interaction.created_at >= start_date
        )
    )
    total_result = await db.execute(total_query)
    total_calls = total_result.scalar() or 0
    
    # Average duration
    duration_query = select(
        func.avg(
            func.extract('epoch', Interaction.end_time - Interaction.start_time)
        )
    ).where(
        and_(
            Interaction.tenant_id == current_tenant.id,
            Interaction.type == "voice_call",
            Interaction.end_time.isnot(None),
            Interaction.created_at >= start_date
        )
    )
    duration_result = await db.execute(duration_query)
    avg_duration = duration_result.scalar() or 0
    
    # Sentiment distribution
    sentiment_query = select(
        func.count(Interaction.id)
    ).where(
        and_(
            Interaction.tenant_id == current_tenant.id,
            Interaction.type == "voice_call",
            Interaction.meta_data['sentiment'].astext == 'positive',
            Interaction.created_at >= start_date
        )
    )
    positive_result = await db.execute(sentiment_query)
    positive_calls = positive_result.scalar() or 0
    
    return {
        "total_calls": total_calls,
        "average_duration_seconds": round(float(avg_duration), 2),
        "positive_sentiment_count": positive_calls,
        "positive_sentiment_percentage": round((positive_calls / total_calls * 100) if total_calls > 0 else 0, 2),
        "period_days": days
    }
