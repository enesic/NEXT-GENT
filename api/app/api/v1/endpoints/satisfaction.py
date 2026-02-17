"""
Satisfaction endpoints - Customer satisfaction tracking.
"""
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.models.tenant import Tenant
from app.models.satisfaction import Satisfaction, SatisfactionType, SatisfactionChannel
from app.services.satisfaction_service import SatisfactionService

router = APIRouter()


class SatisfactionCreate(BaseModel):
    customer_id: Optional[UUID] = None
    interaction_id: Optional[UUID] = None
    call_id: Optional[str] = None
    survey_type: SatisfactionType = SatisfactionType.CSAT
    channel: SatisfactionChannel = SatisfactionChannel.IN_APP


class SatisfactionResponse(BaseModel):
    survey_id: UUID
    nps_score: Optional[int] = Field(None, ge=0, le=10)
    csat_score: Optional[int] = Field(None, ge=1, le=5)
    custom_rating: Optional[float] = Field(None, ge=0.0, le=10.0)
    feedback_text: Optional[str] = None


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_survey(
    survey_data: SatisfactionCreate,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """
    Create a satisfaction survey.
    """
    survey = await SatisfactionService.create_survey(
        db=db,
        tenant_id=current_tenant.id,
        customer_id=survey_data.customer_id,
        interaction_id=survey_data.interaction_id,
        call_id=survey_data.call_id,
        survey_type=survey_data.survey_type,
        channel=survey_data.channel
    )
    
    return {
        "survey_id": str(survey.id),
        "message": "Survey created successfully"
    }


@router.post("/{survey_id}/submit", status_code=status.HTTP_200_OK)
async def submit_survey_response(
    survey_id: UUID,
    response: SatisfactionResponse,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """
    Submit satisfaction survey response.
    Automatically triggers AI sentiment analysis.
    """
    satisfaction = await SatisfactionService.submit_response(
        db=db,
        survey_id=survey_id,
        nps_score=response.nps_score,
        csat_score=response.csat_score,
        custom_rating=response.custom_rating,
        feedback_text=response.feedback_text
    )
    
    return {
        "survey_id": str(satisfaction.id),
        "sentiment": satisfaction.sentiment,
        "sentiment_score": satisfaction.sentiment_score,
        "ai_summary": satisfaction.ai_summary,
        "message": "Response submitted successfully"
    }


@router.get("/metrics")
async def get_satisfaction_metrics(
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None)
):
    """
    Get satisfaction metrics (NPS, CSAT, sentiment distribution).
    """
    metrics = await SatisfactionService.get_satisfaction_metrics(
        db=db,
        tenant_id=current_tenant.id,
        start_date=start_date,
        end_date=end_date
    )
    
    return metrics


@router.get("/trends")
async def get_satisfaction_trends(
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    days: int = Query(30, ge=1, le=365)
):
    """
    Get satisfaction trends over time (for charts).
    """
    trends = await SatisfactionService.get_satisfaction_trends(
        db=db,
        tenant_id=current_tenant.id,
        days=days
    )
    
    return trends
