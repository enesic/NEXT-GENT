"""
Customer Portal API endpoints.
"""
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from pydantic import BaseModel
import uuid as uuid_pkg

from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.core.logger import get_logger
from app.models.tenant import Tenant
from app.models.customer import Customer
from app.models.interaction import Interaction
from app.models.vapi_call import VAPICall
from app.models.subscription_plan import SubscriptionPlan

router = APIRouter()
logger = get_logger(__name__)


# Schemas
class AppointmentResponse(BaseModel):
    id: str
    title: str
    date: datetime
    status: str
    customer_name: str
    notes: Optional[str]


class MessageResponse(BaseModel):
    id: str
    message: str
    direction: str  # inbound, outbound
    channel: str  # whatsapp, sms, email
    created_at: datetime


class CallResponse(BaseModel):
    id: str
    duration: int
    status: str
    summary: Optional[str]
    created_at: datetime


class SubscriptionResponse(BaseModel):
    id: str
    card_name: str
    status: str
    billing_cycle: str
    amount: float
    next_billing_date: Optional[datetime]
    current_usage: dict


@router.get("/appointments", response_model=List[AppointmentResponse])
async def get_customer_appointments(
    status: Optional[str] = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Get customer's appointments.
    """
    try:
        if not current_tenant:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Giriş yapmanız gerekiyor"
            )
        
        # Get interactions of type 'appointment'
        query = select(Interaction).where(
            and_(
                Interaction.tenant_id == current_tenant.id,
                Interaction.type == "appointment"
            )
        )
        
        if status:
            # Filter by metadata status if provided
            pass  # Implement metadata filtering
        
        query = query.order_by(desc(Interaction.created_at)).limit(limit)
        
        result = await db.execute(query)
        interactions = result.scalars().all()
        
        appointments = []
        for interaction in interactions:
            metadata = interaction.meta_data or {}
            appointments.append(AppointmentResponse(
                id=str(interaction.id),
                title=metadata.get("title", "Randevu"),
                date=interaction.created_at,
                status=metadata.get("status", "scheduled"),
                customer_name=metadata.get("customer_name", "Müşteri"),
                notes=metadata.get("notes")
            ))
        
        return appointments
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_appointments_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Randevular alınamadı"
        )


@router.get("/messages", response_model=List[MessageResponse])
async def get_customer_messages(
    channel: Optional[str] = None,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Get customer's message history.
    """
    try:
        if not current_tenant:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Giriş yapmanız gerekiyor"
            )
        
        query = select(Interaction).where(
            and_(
                Interaction.tenant_id == current_tenant.id,
                Interaction.type.in_(["whatsapp", "sms", "email"])
            )
        )
        
        if channel:
            query = query.where(Interaction.type == channel)
        
        query = query.order_by(desc(Interaction.created_at)).limit(limit)
        
        result = await db.execute(query)
        interactions = result.scalars().all()
        
        messages = []
        for interaction in interactions:
            metadata = interaction.meta_data or {}
            messages.append(MessageResponse(
                id=str(interaction.id),
                message=metadata.get("message", interaction.summary or ""),
                direction=metadata.get("direction", "inbound"),
                channel=interaction.type,
                created_at=interaction.created_at
            ))
        
        return messages
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_messages_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Mesajlar alınamadı"
        )


@router.get("/calls", response_model=List[CallResponse])
async def get_customer_calls(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Get customer's call summaries.
    """
    try:
        if not current_tenant:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Giriş yapmanız gerekiyor"
            )
        
        result = await db.execute(
            select(VAPICall)
            .where(VAPICall.tenant_id == current_tenant.id)
            .order_by(desc(VAPICall.created_at))
            .limit(limit)
        )
        calls = result.scalars().all()
        
        return [
            CallResponse(
                id=str(call.id),
                duration=call.call_duration_seconds or 0,
                status=call.call_status,
                summary=call.summary,
                created_at=call.created_at
            )
            for call in calls
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_calls_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Aramalar alınamadı"
        )


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_customer_subscription(
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Get customer's subscription details.
    """
    try:
        if not current_tenant:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Giriş yapmanız gerekiyor"
            )
        
        # Get active subscription
        result = await db.execute(
            select(SubscriptionPlan)
            .where(
                and_(
                    SubscriptionPlan.tenant_id == current_tenant.id,
                    SubscriptionPlan.status == "active"
                )
            )
            .limit(1)
        )
        subscription = result.scalar_one_or_none()
        
        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aktif abonelik bulunamadı"
            )
        
        # Get card details
        from app.models.card import Card
        card_result = await db.execute(
            select(Card).where(Card.id == subscription.card_id)
        )
        card = card_result.scalar_one_or_none()
        
        return SubscriptionResponse(
            id=str(subscription.id),
            card_name=card.display_name if card else "Unknown",
            status=subscription.status,
            billing_cycle=subscription.billing_cycle,
            amount=float(subscription.amount),
            next_billing_date=subscription.next_billing_date,
            current_usage={
                "users": subscription.current_users,
                "calls": subscription.current_calls_this_month,
                "tokens": subscription.current_tokens_this_month
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_subscription_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Abonelik bilgisi alınamadı"
        )


@router.get("/reports")
async def get_customer_reports(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Get customer's reports and analytics.
    """
    try:
        if not current_tenant:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Giriş yapmanız gerekiyor"
            )
        
        # Default to last 30 days
        if not end_date:
            end_date = datetime.utcnow()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        # Get call statistics
        calls_result = await db.execute(
            select(VAPICall)
            .where(
                and_(
                    VAPICall.tenant_id == current_tenant.id,
                    VAPICall.created_at >= start_date,
                    VAPICall.created_at <= end_date
                )
            )
        )
        calls = calls_result.scalars().all()
        
        # Get interaction statistics
        interactions_result = await db.execute(
            select(Interaction)
            .where(
                and_(
                    Interaction.tenant_id == current_tenant.id,
                    Interaction.created_at >= start_date,
                    Interaction.created_at <= end_date
                )
            )
        )
        interactions = interactions_result.scalars().all()
        
        return {
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "calls": {
                "total": len(calls),
                "total_duration": sum(call.duration or 0 for call in calls),
                "average_duration": sum(call.duration or 0 for call in calls) / len(calls) if calls else 0
            },
            "interactions": {
                "total": len(interactions),
                "by_type": {
                    "whatsapp": len([i for i in interactions if i.type == "whatsapp"]),
                    "sms": len([i for i in interactions if i.type == "sms"]),
                    "email": len([i for i in interactions if i.type == "email"]),
                    "appointment": len([i for i in interactions if i.type == "appointment"])
                }
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_reports_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Raporlar alınamadı"
        )
