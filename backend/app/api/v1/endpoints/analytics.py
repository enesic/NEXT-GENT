from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.models.tenant import Tenant
from app.services.analytics_service import AnalyticsService

from sqlalchemy import func, select, and_, or_
from app.models.vapi_call import VAPICall, CallStatus
from app.models.customer import Customer
from app.models.interaction import Interaction

router = APIRouter()


@router.get("/pulse", response_model=Dict[str, Any])
async def get_live_pulse(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
):
    """
    Get live pulse data for the dashboard (Real-time).
    """
    # 1. Active Calls (real-time)
    active_calls_query = select(func.count()).where(
        VAPICall.tenant_id == current_tenant.id,
        VAPICall.call_status == CallStatus.IN_PROGRESS
    )
    active_calls = (await db.execute(active_calls_query)).scalar() or 0
    
    # 2. Today's Clients (New or Interacted)
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    today_clients_query = select(func.count(func.distinct(Interaction.client_email))).where(
        Interaction.tenant_id == current_tenant.id,
        Interaction.start_time >= today_start
    )
    today_clients = (await db.execute(today_clients_query)).scalar() or 0
    
    # 3. Pending Appointments
    pending_apps_query = select(func.count()).where(
        Interaction.tenant_id == current_tenant.id,
        Interaction.status == 'PENDING',
        Interaction.start_time >= datetime.utcnow()
    )
    pending_appointments = (await db.execute(pending_apps_query)).scalar() or 0
    
    # 4. Conversion Rate (Today) - Confirmed / Total
    total_apps_query = select(func.count()).where(
        Interaction.tenant_id == current_tenant.id,
        Interaction.start_time >= today_start
    )
    confirmed_apps_query = select(func.count()).where(
        Interaction.tenant_id == current_tenant.id,
        Interaction.status == 'CONFIRMED',
        Interaction.start_time >= today_start
    )
    
    total_apps = (await db.execute(total_apps_query)).scalar() or 0
    confirmed_apps = (await db.execute(confirmed_apps_query)).scalar() or 0
    
    conversion_rate = 0.0
    if total_apps > 0:
        conversion_rate = round((confirmed_apps / total_apps) * 100, 1)

    return {
        "activeCalls": active_calls,
        "conversionRate": conversion_rate,
        "todayClients": today_clients,
        "pendingAppointments": pending_appointments
    }



@router.get("/stats", response_model=Dict[str, Any])
async def get_dashboard_stats(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
):
    """
    Get real-time dashboard stats: revenue, active calls, satisfaction.
    """
    # In a real app, these would come from the database/redis
    # For now, we return mock data that matches the user request
    return {
        "daily_revenue": 15420.00,
        "active_calls": 3,
        "customer_satisfaction": 98.5,
        "total_appointments": 24,
        "completed_appointments": 18,
        "waiting_appointments": 4,
        "cancelled_appointments": 2
    }


@router.get("/daily-conversation-duration", response_model=Dict[str, Any])
async def get_daily_conversation_duration(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    start_date: Optional[datetime] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[datetime] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """
    Get daily conversation duration in minutes.
    
    Returns ApexCharts line chart format:
    ```json
    {
        "series": [{"name": "Duration", "data": [120, 150, 180]}],
        "categories": ["2026-01-01", "2026-01-02", "2026-01-03"]
    }
    ```
    
    Example:
    ```
    GET /api/v1/analytics/daily-conversation-duration?start_date=2026-01-01&end_date=2026-01-31
    ```
    """
    # Default to last 30 days if not provided
    if not start_date:
        start_date = datetime.utcnow() - timedelta(days=30)
    if not end_date:
        end_date = datetime.utcnow()
    
    return await AnalyticsService.get_daily_conversation_duration(
        db=db,
        tenant_id=current_tenant.id,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/unique-person-count", response_model=Dict[str, Any])
async def get_unique_person_count(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    start_date: datetime = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: datetime = Query(..., description="End date (YYYY-MM-DD)"),
):
    """
    Get daily unique person count (distinct customers).
    
    Returns ApexCharts line chart format.
    """
    return await AnalyticsService.get_unique_person_count(
        db=db,
        tenant_id=current_tenant.id,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/conversion-rate", response_model=Dict[str, Any])
async def get_conversion_rate(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    start_date: datetime = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: datetime = Query(..., description="End date (YYYY-MM-DD)"),
):
    """
    Get daily conversion rate (confirmed / total appointments).
    
    Returns ApexCharts line chart format with percentage:
    ```json
    {
        "series": [{"name": "Conversion Rate (%)", "data": [75.5, 80.2, 85.0]}],
        "categories": ["2026-01-01", "2026-01-02", "2026-01-03"]
    }
    ```
    """
    return await AnalyticsService.get_conversion_rate(
        db=db,
        tenant_id=current_tenant.id,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/appointment-status-breakdown", response_model=Dict[str, Any])
async def get_appointment_status_breakdown(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    start_date: datetime = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: datetime = Query(..., description="End date (YYYY-MM-DD)"),
):
    """
    Get appointment status breakdown for pie chart.
    
    Returns ApexCharts pie chart format:
    ```json
    {
        "series": [10, 20, 30, 5],
        "labels": ["Pending", "Confirmed", "Cancelled", "Completed"]
    }
    ```
    """
    return await AnalyticsService.get_appointment_status_breakdown(
        db=db,
        tenant_id=current_tenant.id,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/customer-segment-distribution", response_model=Dict[str, Any])
async def get_customer_segment_distribution(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
):
    """
    Get customer segment distribution for pie chart.
    
    Returns ApexCharts pie chart format:
    ```json
    {
        "series": [5, 10, 15, 20, 50],
        "labels": ["VIP", "GOLD", "SILVER", "BRONZE", "REGULAR"]
    }
    ```
    """
    return await AnalyticsService.get_customer_segment_distribution(
        db=db,
        tenant_id=current_tenant.id
    )


@router.get("/revenue-by-segment", response_model=Dict[str, Any])
async def get_revenue_by_segment(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    start_date: datetime = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: datetime = Query(..., description="End date (YYYY-MM-DD)"),
):
    """
    Get revenue breakdown by customer segment for bar chart.
    
    Returns ApexCharts bar chart format:
    ```json
    {
        "series": [{"name": "Revenue ($)", "data": [50000, 30000, 15000, 8000, 5000]}],
        "categories": ["VIP", "GOLD", "SILVER", "BRONZE", "REGULAR"]
    }
    ```
    """
    return await AnalyticsService.get_revenue_by_segment(
        db=db,
        tenant_id=current_tenant.id,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/dashboard-summary", response_model=Dict[str, Any])
async def get_dashboard_summary(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    start_date: datetime = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: datetime = Query(..., description="End date (YYYY-MM-DD)"),
):
    """
    Get dashboard summary with key metrics.
    
    Returns summary statistics:
    ```json
    {
        "total_appointments": 150,
        "confirmed_appointments": 120,
        "total_customers": 85,
        "total_revenue": 45000.00,
        "conversion_rate": 80.00,
        "period": {
            "start_date": "2026-01-01",
            "end_date": "2026-01-31"
        }
    }
    ```
    """
    return await AnalyticsService.get_dashboard_summary(
        db=db,
        tenant_id=current_tenant.id,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/hourly-distribution", response_model=Dict[str, Any])
async def get_hourly_appointment_distribution(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    start_date: datetime = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: datetime = Query(..., description="End date (YYYY-MM-DD)"),
):
    """
    Get hourly appointment distribution for heatmap.
    
    Returns ApexCharts column chart format:
    ```json
    {
        "series": [{"name": "Appointments", "data": [5, 8, 12, 15, 20, ...]}],
        "categories": ["00:00", "01:00", "02:00", ...]
    }
    ```
    """
    return await AnalyticsService.get_hourly_appointment_distribution(
        db=db,
        tenant_id=current_tenant.id,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/quick-stats")
async def get_quick_stats(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    days: int = Query(30, description="Number of days to look back"),
):
    """
    Get quick stats for the last N days (default: 30).
    
    Convenience endpoint that returns dashboard summary for last N days.
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    return await AnalyticsService.get_dashboard_summary(
        db=db,
        tenant_id=current_tenant.id,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/kpis", response_model=List[Dict[str, Any]])
async def get_sectoral_kpis(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
):
    """
    Get sector-specific KPIs for the Luxury Dashboard.
    """
    # Assuming sector is stored in tenant config, fallback to 'medical' or generic
    sector = "medical"
    if current_tenant.config and "sector" in current_tenant.config:
        sector = current_tenant.config["sector"]
        
    return await AnalyticsService.get_sectoral_kpis(
        db=db,
        tenant_id=current_tenant.id,
        sector=sector
    )


@router.get("/insights", response_model=List[Dict[str, Any]])
async def get_ai_insights(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
):
    """
    Get AI-driven strategic insights.
    """
    return await AnalyticsService.get_ai_insights(
        db=db,
        tenant_id=current_tenant.id
    )


@router.get("/satisfaction", response_model=Dict[str, Any])
async def get_satisfaction_analytics(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    days: int = Query(30, ge=1, le=365)
):
    """
    Get satisfaction analytics (NPS, CSAT, trends).
    """
    from app.services.satisfaction_service import SatisfactionService
    
    metrics = await SatisfactionService.get_satisfaction_metrics(
        db=db,
        tenant_id=current_tenant.id,
        start_date=datetime.utcnow() - timedelta(days=days),
        end_date=datetime.utcnow()
    )
    
    trends = await SatisfactionService.get_satisfaction_trends(
        db=db,
        tenant_id=current_tenant.id,
        days=days
    )
    
    return {
        "metrics": metrics,
        "trends": trends
    }
