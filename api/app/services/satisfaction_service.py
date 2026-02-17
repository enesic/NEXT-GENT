"""
Satisfaction Service - Customer satisfaction tracking and analysis.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy import select, func, and_, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.satisfaction import Satisfaction, SatisfactionType, SatisfactionChannel
from app.services.ai_service import AIService
from app.core.logger import get_logger

logger = get_logger(__name__)


class SatisfactionService:
    """
    Service for managing customer satisfaction surveys and analysis.
    """
    
    @staticmethod
    async def create_survey(
        db: AsyncSession,
        tenant_id: UUID,
        customer_id: Optional[UUID],
        interaction_id: Optional[UUID],
        call_id: Optional[str],
        survey_type: SatisfactionType = SatisfactionType.CSAT,
        channel: SatisfactionChannel = SatisfactionChannel.IN_APP
    ) -> Satisfaction:
        """
        Create a satisfaction survey.
        """
        satisfaction = Satisfaction(
            tenant_id=tenant_id,
            customer_id=str(customer_id) if customer_id else None,
            interaction_id=str(interaction_id) if interaction_id else None,
            call_id=call_id,
            survey_type=survey_type,
            channel=channel,
            survey_sent_at=datetime.utcnow()
        )
        
        db.add(satisfaction)
        await db.commit()
        await db.refresh(satisfaction)
        
        logger.info("satisfaction_survey_created", survey_id=str(satisfaction.id), tenant_id=str(tenant_id))
        
        return satisfaction
    
    @staticmethod
    async def submit_response(
        db: AsyncSession,
        survey_id: UUID,
        nps_score: Optional[int] = None,
        csat_score: Optional[int] = None,
        custom_rating: Optional[float] = None,
        feedback_text: Optional[str] = None
    ) -> Satisfaction:
        """
        Submit satisfaction survey response.
        Automatically triggers AI sentiment analysis.
        """
        query = select(Satisfaction).where(Satisfaction.id == survey_id)
        result = await db.execute(query)
        satisfaction = result.scalar_one_or_none()
        
        if not satisfaction:
            raise ValueError("Survey not found")
        
        # Update scores
        satisfaction.nps_score = nps_score
        satisfaction.csat_score = csat_score
        satisfaction.custom_rating = custom_rating
        satisfaction.feedback_text = feedback_text
        satisfaction.responded_at = datetime.utcnow()
        
        # AI Sentiment Analysis (if feedback provided)
        if feedback_text:
            try:
                sentiment_result = await AIService.analyze_sentiment(
                    text=feedback_text,
                    context=f"Customer satisfaction survey response. Score: {csat_score or nps_score}"
                )
                
                satisfaction.sentiment = sentiment_result.get("sentiment")
                satisfaction.sentiment_score = sentiment_result.get("score", 0.5)
                satisfaction.ai_summary = sentiment_result.get("summary", "")
                
            except Exception as e:
                logger.error("sentiment_analysis_error", error=str(e))
        
        await db.commit()
        await db.refresh(satisfaction)
        
        logger.info("satisfaction_response_submitted", survey_id=str(survey_id))
        
        return satisfaction
    
    @staticmethod
    async def get_satisfaction_metrics(
        db: AsyncSession,
        tenant_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get satisfaction metrics (NPS, CSAT, trends).
        """
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()
        
        # NPS Calculation
        nps_query = select(
            func.count(Satisfaction.id).label('total'),
            func.sum(case((Satisfaction.nps_score >= 9, 1), else_=0)).label('promoters'),
            func.sum(case((Satisfaction.nps_score <= 6, 1), else_=0)).label('detractors')
        ).where(
            and_(
                Satisfaction.tenant_id == tenant_id,
                Satisfaction.nps_score.isnot(None),
                Satisfaction.responded_at >= start_date,
                Satisfaction.responded_at <= end_date
            )
        )
        
        nps_result = await db.execute(nps_query)
        nps_data = nps_result.one()
        
        total_nps = nps_data.total or 0
        promoters = nps_data.promoters or 0
        detractors = nps_data.detractors or 0
        
        nps_score = 0.0
        if total_nps > 0:
            promoter_pct = (promoters / total_nps) * 100
            detractor_pct = (detractors / total_nps) * 100
            nps_score = promoter_pct - detractor_pct
        
        # CSAT Calculation
        csat_query = select(
            func.avg(Satisfaction.csat_score).label('avg_csat'),
            func.count(Satisfaction.id).label('total')
        ).where(
            and_(
                Satisfaction.tenant_id == tenant_id,
                Satisfaction.csat_score.isnot(None),
                Satisfaction.responded_at >= start_date,
                Satisfaction.responded_at <= end_date
            )
        )
        
        csat_result = await db.execute(csat_query)
        csat_data = csat_result.one()
        
        avg_csat = float(csat_data.avg_csat or 0)
        total_csat = csat_data.total or 0
        
        # Sentiment Distribution
        sentiment_query = select(
            Satisfaction.sentiment,
            func.count(Satisfaction.id).label('count')
        ).where(
            and_(
                Satisfaction.tenant_id == tenant_id,
                Satisfaction.sentiment.isnot(None),
                Satisfaction.responded_at >= start_date,
                Satisfaction.responded_at <= end_date
            )
        ).group_by(Satisfaction.sentiment)
        
        sentiment_result = await db.execute(sentiment_query)
        sentiment_rows = sentiment_result.all()
        
        sentiment_dist = {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }
        
        for row in sentiment_rows:
            if row.sentiment:
                sentiment_dist[row.sentiment] = row.count
        
        return {
            "nps": {
                "score": round(nps_score, 2),
                "total_responses": total_nps,
                "promoters": promoters,
                "detractors": detractors
            },
            "csat": {
                "average": round(avg_csat, 2),
                "total_responses": total_csat
            },
            "sentiment": sentiment_dist,
            "period": {
                "start_date": start_date.strftime('%Y-%m-%d'),
                "end_date": end_date.strftime('%Y-%m-%d')
            }
        }
    
    @staticmethod
    async def get_satisfaction_trends(
        db: AsyncSession,
        tenant_id: UUID,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get satisfaction trends over time (for charts).
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Daily NPS trend
        nps_trend_query = select(
            func.date(Satisfaction.responded_at).label('date'),
            func.avg(Satisfaction.nps_score).label('avg_nps')
        ).where(
            and_(
                Satisfaction.tenant_id == tenant_id,
                Satisfaction.nps_score.isnot(None),
                Satisfaction.responded_at >= start_date,
                Satisfaction.responded_at <= end_date
            )
        ).group_by(
            func.date(Satisfaction.responded_at)
        ).order_by(
            func.date(Satisfaction.responded_at)
        )
        
        nps_result = await db.execute(nps_trend_query)
        nps_rows = nps_result.all()
        
        # Daily CSAT trend
        csat_trend_query = select(
            func.date(Satisfaction.responded_at).label('date'),
            func.avg(Satisfaction.csat_score).label('avg_csat')
        ).where(
            and_(
                Satisfaction.tenant_id == tenant_id,
                Satisfaction.csat_score.isnot(None),
                Satisfaction.responded_at >= start_date,
                Satisfaction.responded_at <= end_date
            )
        ).group_by(
            func.date(Satisfaction.responded_at)
        ).order_by(
            func.date(Satisfaction.responded_at)
        )
        
        csat_result = await db.execute(csat_trend_query)
        csat_rows = csat_result.all()
        
        # Format for ApexCharts
        dates = []
        nps_data = []
        csat_data = []
        
        # Combine dates
        all_dates = set()
        for row in nps_rows:
            all_dates.add(row.date)
        for row in csat_rows:
            all_dates.add(row.date)
        
        sorted_dates = sorted(all_dates)
        
        # Build data arrays
        nps_dict = {row.date: row.avg_nps for row in nps_rows}
        csat_dict = {row.date: row.avg_csat for row in csat_rows}
        
        for date in sorted_dates:
            dates.append(date.strftime('%Y-%m-%d'))
            nps_data.append(round(float(nps_dict.get(date, 0)), 2))
            csat_data.append(round(float(csat_dict.get(date, 0)), 2))
        
        return {
            "series": [
                {
                    "name": "NPS Score",
                    "data": nps_data
                },
                {
                    "name": "CSAT Score",
                    "data": csat_data
                }
            ],
            "categories": dates
        }
