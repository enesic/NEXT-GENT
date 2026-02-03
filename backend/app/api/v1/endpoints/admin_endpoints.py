"""
Admin-specific API endpoints for NextGent management.
"""
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from pydantic import BaseModel

from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.core.logger import get_logger
from app.models.tenant import Tenant
from app.models.customer import Customer
from app.models.subscription_plan import SubscriptionPlan
from app.models.card import Card
from app.models.vapi_call import VAPICall
from app.models.interaction import Interaction
from app.models.flow import Flow, FlowExecution
from app.models.audit_log import AuditLog, ActionType
from app.models.token_usage import TokenUsage
from app.api.v1.endpoints.auth_endpoints import get_current_admin

router = APIRouter()
logger = get_logger(__name__)


# Schemas
class DashboardStats(BaseModel):
    total_customers: int
    monthly_revenue: float
    token_consumption: int
    total_calls: int
    active_subscriptions: int
    growth_rate: float


class TrafficData(BaseModel):
    date: str
    calls: int
    whatsapp: int
    automation: int


class CardResponse(BaseModel):
    id: str
    name: str
    display_name: str
    tier_level: int
    monthly_price: float
    annual_price: Optional[float]
    features: dict
    max_users: Optional[int]
    max_calls_per_month: Optional[int]
    is_active: bool
    is_popular: bool
    description: Optional[str]
    color_primary: Optional[str]
    color_accent: Optional[str]


@router.get("/dashboard", response_model=DashboardStats)
async def get_admin_dashboard(
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Get admin dashboard statistics.
    """
    try:
        # Total customers
        customers_result = await db.execute(
            select(func.count(Customer.id))
        )
        total_customers = customers_result.scalar() or 0
        
        # Active subscriptions
        subscriptions_result = await db.execute(
            select(func.count(SubscriptionPlan.id)).where(
                SubscriptionPlan.status == "active"
            )
        )
        active_subscriptions = subscriptions_result.scalar() or 0
        
        # Monthly revenue (sum of active subscriptions)
        revenue_result = await db.execute(
            select(func.sum(SubscriptionPlan.amount)).where(
                and_(
                    SubscriptionPlan.status == "active",
                    SubscriptionPlan.billing_cycle == "monthly"
                )
            )
        )
        monthly_revenue = float(revenue_result.scalar() or 0)
        
        # Total calls this month
        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        calls_result = await db.execute(
            select(func.count(VAPICall.id)).where(
                VAPICall.created_at >= start_of_month
            )
        )
        total_calls = calls_result.scalar() or 0
        
        # Token consumption (placeholder - implement based on your token tracking)
        token_consumption = total_calls * 150  # Rough estimate
        
        # Growth rate (placeholder - calculate based on previous month)
        growth_rate = 12.5
        
        return DashboardStats(
            total_customers=total_customers,
            monthly_revenue=monthly_revenue,
            token_consumption=token_consumption,
            total_calls=total_calls,
            active_subscriptions=active_subscriptions,
            growth_rate=growth_rate
        )
        
    except Exception as e:
        logger.error("admin_dashboard_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Dashboard verisi alınamadı"
        )


@router.get("/cards", response_model=List[CardResponse])
async def get_cards(
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Get all card tiers.
    """
    try:
        result = await db.execute(
            select(Card).where(Card.is_active == True).order_by(Card.tier_level)
        )
        cards = result.scalars().all()
        
        return [
            CardResponse(
                id=str(card.id),
                name=card.name,
                display_name=card.display_name,
                tier_level=card.tier_level,
                monthly_price=float(card.monthly_price),
                annual_price=float(card.annual_price) if card.annual_price else None,
                features=card.features,
                max_users=card.max_users,
                max_calls_per_month=card.max_calls_per_month,
                is_active=card.is_active,
                is_popular=card.is_popular,
                description=card.description,
                color_primary=card.color_primary,
                color_accent=card.color_accent
            )
            for card in cards
        ]
        
    except Exception as e:
        logger.error("get_cards_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Kart bilgileri alınamadı"
        )


@router.get("/traffic", response_model=List[TrafficData])
async def get_traffic_data(
    days: int = 7,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Get traffic data for the last N days.
    """
    try:
        traffic_data = []
        
        for i in range(days):
            date = datetime.utcnow() - timedelta(days=days - i - 1)
            date_str = date.strftime("%a")  # Day name
            
            # Get calls for this day
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)
            
            calls_result = await db.execute(
                select(func.count(VAPICall.id)).where(
                    and_(
                        VAPICall.created_at >= start_of_day,
                        VAPICall.created_at < end_of_day
                    )
                )
            )
            calls = calls_result.scalar() or 0
            
            # WhatsApp and automation are placeholders
            # Implement based on your interaction types
            whatsapp = int(calls * 0.6)  # Rough estimate
            automation = int(calls * 0.3)  # Rough estimate
            
            traffic_data.append(TrafficData(
                date=date_str,
                calls=calls,
                whatsapp=whatsapp,
                automation=automation
            ))
        
        return traffic_data
        
    except Exception as e:
        logger.error("get_traffic_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Trafik verileri alınamadı"
        )


@router.get("/tokens")
async def get_token_consumption(
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Get token consumption analytics.
    """
    try:
        # Get total tokens this month
        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        calls_result = await db.execute(
            select(func.count(VAPICall.id)).where(
                VAPICall.created_at >= start_of_month
            )
        )
        total_calls = calls_result.scalar() or 0
        
        # Rough token estimation (replace with actual token tracking)
        tokens_per_call = 150
        total_tokens = total_calls * tokens_per_call
        
        return {
            "total_tokens_this_month": total_tokens,
            "total_calls": total_calls,
            "average_tokens_per_call": tokens_per_call,
            "estimated_cost": total_tokens * 0.002  # $0.002 per 1K tokens
        }
        
    except Exception as e:
        logger.error("get_tokens_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token verileri alınamadı"
        )


@router.get("/logs")
async def get_audit_logs(
    page: int = 1,
    page_size: int = 50,
    action_type: Optional[str] = None,
    resource_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    """
    Get audit logs with filtering and pagination.
    KVKK compliant - all PII is masked.
    """
    try:
        query = select(AuditLog).where(AuditLog.is_visible == True)
        
        # Apply filters
        if action_type:
            query = query.where(AuditLog.action_type == action_type)
        if resource_type:
            query = query.where(AuditLog.resource_type == resource_type)
        
        # Order by most recent first
        query = query.order_by(AuditLog.created_at.desc())
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        result = await db.execute(query)
        logs = result.scalars().all()
        
        return {
            "logs": [
                {
                    "id": str(log.id),
                    "action_type": log.action_type,
                    "resource_type": log.resource_type,
                    "admin_user_id": log.admin_user_id,
                    "ip_address": log.ip_address,
                    "changes": log.changes,
                    "created_at": log.created_at.isoformat() if log.created_at else None
                }
                for log in logs
            ],
            "total": total,
            "page": page,
            "page_size": page_size
        }
    except Exception as e:
        logger.error("get_logs_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Log verileri alınamadı"
        )


@router.get("/token-analytics")
async def get_token_analytics(
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    """
    Get detailed token usage analytics.
    """
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Total tokens and cost
        total_result = await db.execute(
            select(
                func.sum(TokenUsage.total_tokens),
                func.sum(TokenUsage.estimated_cost),
                func.count(TokenUsage.id)
            ).where(TokenUsage.created_at >= start_date)
        )
        total_row = total_result.one()
        total_tokens = total_row[0] or 0
        total_cost = float(total_row[1] or 0)
        total_calls = total_row[2] or 0
        
        # Model breakdown
        model_result = await db.execute(
            select(
                TokenUsage.model_name,
                func.sum(TokenUsage.total_tokens),
                func.sum(TokenUsage.estimated_cost),
                func.count(TokenUsage.id)
            )
            .where(TokenUsage.created_at >= start_date)
            .group_by(TokenUsage.model_name)
        )
        
        model_breakdown = [
            {
                "model": row[0],
                "total_tokens": row[1] or 0,
                "total_cost": float(row[2] or 0),
                "call_count": row[3] or 0
            }
            for row in model_result
        ]
        
        # Daily usage (last 7 days for chart)
        daily_data = []
        for i in range(7):
            day_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=6-i)
            day_end = day_start + timedelta(days=1)
            
            day_result = await db.execute(
                select(
                    func.sum(TokenUsage.total_tokens),
                    func.sum(TokenUsage.estimated_cost)
                ).where(
                    and_(
                        TokenUsage.created_at >= day_start,
                        TokenUsage.created_at < day_end
                    )
                )
            )
            day_row = day_result.one()
            
            daily_data.append({
                "date": day_start.strftime("%Y-%m-%d"),
                "tokens": day_row[0] or 0,
                "cost": float(day_row[1] or 0)
            })
        
        return {
            "summary": {
                "total_tokens": total_tokens,
                "total_cost_usd": round(total_cost, 4),
                "total_calls": total_calls,
                "average_tokens_per_call": round(total_tokens / total_calls, 2) if total_calls > 0 else 0,
                "period_days": days
            },
            "model_breakdown": model_breakdown,
            "daily_usage": daily_data
        }
        
    except Exception as e:
        logger.error("get_token_analytics_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token analytics alınamadı"
        )
