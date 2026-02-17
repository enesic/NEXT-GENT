"""
Satisfaction Survey Model - Customer satisfaction tracking.
"""
from datetime import datetime
from sqlalchemy import String, Integer, Float, Text, Enum as SQLEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.models.base import Base, UUIDMixin, TimestampMixin, TenantMixin


class SatisfactionType(str, enum.Enum):
    """Satisfaction survey types"""
    NPS = "nps"  # Net Promoter Score (0-10)
    CSAT = "csat"  # Customer Satisfaction (1-5 stars)
    CUSTOM = "custom"  # Custom rating


class SatisfactionChannel(str, enum.Enum):
    """Survey delivery channels"""
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"
    CALL = "call"
    CHAT = "chat"


class Satisfaction(Base, UUIDMixin, TimestampMixin, TenantMixin):
    """
    Customer satisfaction survey responses.
    """
    __tablename__ = "satisfactions"
    
    # Related entities
    customer_id: Mapped[str] = mapped_column(String, nullable=True, index=True)  # Customer UUID as string
    interaction_id: Mapped[str] = mapped_column(String, nullable=True, index=True)  # Interaction UUID as string
    call_id: Mapped[str] = mapped_column(String, nullable=True, index=True)  # Call/chat ID
    
    # Survey type
    survey_type: Mapped[SatisfactionType] = mapped_column(
        SQLEnum(SatisfactionType, name="satisfaction_type"),
        default=SatisfactionType.CSAT,
        nullable=False
    )
    
    # Channel
    channel: Mapped[SatisfactionChannel] = mapped_column(
        SQLEnum(SatisfactionChannel, name="satisfaction_channel"),
        default=SatisfactionChannel.IN_APP,
        nullable=False
    )
    
    # Ratings
    nps_score: Mapped[int] = mapped_column(Integer, nullable=True)  # 0-10
    csat_score: Mapped[int] = mapped_column(Integer, nullable=True)  # 1-5
    custom_rating: Mapped[float] = mapped_column(Float, nullable=True)  # Custom scale
    
    # Feedback
    feedback_text: Mapped[str] = mapped_column(Text, nullable=True)
    
    # AI Analysis
    sentiment: Mapped[str] = mapped_column(String(20), nullable=True)  # positive, neutral, negative
    sentiment_score: Mapped[float] = mapped_column(Float, nullable=True)  # 0.0 - 1.0
    ai_summary: Mapped[str] = mapped_column(Text, nullable=True)  # AI-generated summary
    
    # Metadata
    responded_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    survey_sent_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
