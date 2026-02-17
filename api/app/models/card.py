"""
Card tier model for NextGent subscription tiers.
"""
from sqlalchemy import String, Integer, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base, UUIDMixin, TimestampMixin


class Card(Base, UUIDMixin, TimestampMixin):
    """
    Card tier model representing subscription levels.
    Tiers: Black, Purple, Gold
    """
    __tablename__ = "cards"

    name: Mapped[str] = mapped_column(String, nullable=False)  # Black, Purple, Gold
    display_name: Mapped[str] = mapped_column(String, nullable=False)  # Display name in Turkish
    tier_level: Mapped[int] = mapped_column(Integer, nullable=False)  # 1=Black, 2=Purple, 3=Gold
    
    # Pricing
    monthly_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    annual_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    
    # Features included in this tier
    # {
    #   "max_users": 10,
    #   "max_calls_per_month": 1000,
    #   "ai_features": true,
    #   "priority_support": false,
    #   "custom_branding": false,
    #   "api_access": true,
    #   "webhook_integrations": true,
    #   "advanced_analytics": false
    # }
    features: Mapped[dict] = mapped_column(JSONB, nullable=False, default={})
    
    # Limits
    max_users: Mapped[int] = mapped_column(Integer, nullable=True)
    max_calls_per_month: Mapped[int] = mapped_column(Integer, nullable=True)
    max_tokens_per_month: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_popular: Mapped[bool] = mapped_column(Boolean, default=False)  # Show "Most Popular" badge
    
    # Description
    description: Mapped[str] = mapped_column(String, nullable=True)
    
    # Color theme for UI
    color_primary: Mapped[str] = mapped_column(String, nullable=True)  # e.g., "#000000" for Black
    color_accent: Mapped[str] = mapped_column(String, nullable=True)  # e.g., "#FFD700" for Gold
