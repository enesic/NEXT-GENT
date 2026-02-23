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
from app.schemas.customer import CustomerCreate
from app.schemas.interaction import InteractionCreate

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
    customer_name: Optional[str] = None
    message: str
    direction: str  # inbound, outbound
    channel: str  # whatsapp, sms, email
    status: str = "read"
    created_at: datetime


class CallResponse(BaseModel):
    id: str
    customer_name: Optional[str] = None
    phone: Optional[str] = None
    duration: int
    duration_formatted: Optional[str] = None
    status: str
    summary: Optional[str]
    timestamp: Optional[datetime] = None
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


@router.get("/messages")
async def get_customer_messages(
    channel: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Get customer's message/interaction history with pagination.
    Uses the real Interaction schema: title, client_name, meta_data, type.
    Returns all interaction types except voice calls.
    """
    try:
        if not current_tenant:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Giriş yapmanız gerekiyor"
            )
        
        limit = min(limit, 20)
        offset = (page - 1) * limit
        
        # Show all interaction types (they are all message/appointment communications)
        base_filter = Interaction.tenant_id == current_tenant.id
        if channel:
            base_filter = and_(base_filter, Interaction.type == channel)
        
        from sqlalchemy import func
        count_result = await db.execute(
            select(func.count(Interaction.id)).where(base_filter)
        )
        total = count_result.scalar() or 0
        
        result = await db.execute(
            select(Interaction)
            .where(base_filter)
            .order_by(desc(Interaction.created_at))
            .offset(offset)
            .limit(limit)
        )
        interactions = result.scalars().all()
        
        channel_map = {
            "whatsapp": "WhatsApp",
            "sms": "SMS",
            "email": "E-posta",
            "chat": "Canlı Chat",
            "appointment": "Randevu",
            "inquiry": "Sorgu",
            "complaint": "Şikayet",
            "feedback": "Geri Bildirim",
        }
        
        messages_out = []
        for interaction in interactions:
            meta = interaction.meta_data or {}
            # Use client_name from model (real schema field)
            raw_name = getattr(interaction, 'client_name', None) or meta.get('customer_name', 'Müşteri')
            if raw_name and raw_name.lower() in ('sistem', 'system', 'admin'):
                raw_name = 'Müşteri'
            
            channel_label = channel_map.get(interaction.type, interaction.type or "Mesaj")
            msg_text = (
                meta.get('message') or
                getattr(interaction, 'title', None) or
                getattr(interaction, 'description', None) or
                interaction.type or ""
            )
            
            messages_out.append(MessageResponse(
                id=str(interaction.id),
                customer_name=raw_name,
                message=msg_text,
                direction=meta.get('direction', 'inbound'),
                channel=channel_label,
                status=meta.get('status', 'read'),
                created_at=interaction.created_at
            ))
        
        return {
            "status": "success",
            "data": messages_out,
            "pagination": {"page": page, "limit": limit, "total": total}
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_messages_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Mesajlar alınamadı"
        )


@router.get("/calls")
async def get_customer_calls(
    page: int = 1,
    limit: int = 10,
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
        
        # Cap limit to prevent excessive data
        limit = min(limit, 20)
        offset = (page - 1) * limit
        
        # Count total for pagination
        from sqlalchemy import func
        count_query = select(func.count(VAPICall.id)).where(
            VAPICall.tenant_id == current_tenant.id
        )
        count_result = await db.execute(count_query)
        total = count_result.scalar() or 0
        
        result = await db.execute(
            select(VAPICall)
            .where(VAPICall.tenant_id == current_tenant.id)
            .order_by(desc(VAPICall.created_at))
            .offset(offset)
            .limit(limit)
        )
        calls = result.scalars().all()
        
        call_responses = []
        for call in calls:
            dur_sec = call.call_duration_seconds or 0
            dur_min = dur_sec // 60
            dur_rem = dur_sec % 60
            
            # Try to get customer name, filter Sistem
            cust_name = getattr(call, 'customer_name', None)
            if cust_name and cust_name.lower() in ('sistem', 'system', 'admin'):
                cust_name = None
            
            call_responses.append(CallResponse(
                id=str(call.id),
                customer_name=cust_name or 'Müşteri',
                phone=None,  # KVKK: do not expose phone
                duration=dur_sec,
                duration_formatted=f"{dur_min}m {dur_rem}s",
                status=call.call_status or 'completed',
                summary=None,  # VAPICall has no summary field
                timestamp=call.created_at,
                created_at=call.created_at
            ))
        
        return {
            "status": "success",
            "data": call_responses,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total
            }
        }
        
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


@router.post("/customers")
async def create_portal_customer(
    customer_in: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Hızlı müşteri kaydı oluşturur.
    """
    try:
        if not current_tenant:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Giriş yapmanız gerekiyor"
            )
        
        # Telefon numarasını hashle
        customer = Customer(
            **customer_in.model_dump(exclude={"phone"}),
            tenant_id=current_tenant.id,
            status="active",
            segment="regular"
        )
        customer.set_phone(customer_in.phone)
        
        db.add(customer)
        await db.commit()
        await db.refresh(customer)
        
        return {"status": "success", "id": str(customer.id)}
        
    except Exception as e:
        logger.error("create_customer_error", error=str(e))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Müşteri kaydedilemedi"
        )


@router.post("/appointments")
async def create_portal_appointment(
    interaction_in: InteractionCreate,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Yeni randevu (interaction) oluşturur.
    """
    try:
        if not current_tenant:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Giriş yapmanız gerekiyor"
            )
        
        interaction = Interaction(
            **interaction_in.model_dump(exclude={"meta_data"}),
            tenant_id=current_tenant.id,
            status="PENDING",
            version=1
        )
        
        if interaction_in.metadata:
            interaction.meta_data = interaction_in.metadata
        else:
            interaction.meta_data = {
                "title": interaction_in.title,
                "customer_name": interaction_in.client_name,
                "status": "pending"
            }
        
        db.add(interaction)
        await db.commit()
        await db.refresh(interaction)
        
        return {"status": "success", "id": str(interaction.id)}
        
    except Exception as e:
        logger.error("create_appointment_error", error=str(e))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Randevu kaydedilemedi"
        )
