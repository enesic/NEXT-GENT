"""
Subscription plan model for customer subscriptions.
"""
from sqlalchemy import String, Integer, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.models.base import Base, UUIDMixin, TimestampMixin
import uuid


class SubscriptionPlan(Base, UUIDMixin, TimestampMixin):
    """
    Subscription plan model linking customers to card tiers.
    """
    __tablename__ = "subscription_plans"

    # Foreign keys
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    card_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cards.id"), nullable=False, index=True)
    
    # Subscription details
    status: Mapped[str] = mapped_column(String, nullable=False, default="active")  # active, cancelled, expired, trial
    billing_cycle: Mapped[str] = mapped_column(String, nullable=False, default="monthly")  # monthly, annual
    
    # Dates
    start_date: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[datetime] = mapped_column(nullable=True)
    trial_end_date: Mapped[datetime] = mapped_column(nullable=True)
    next_billing_date: Mapped[datetime] = mapped_column(nullable=True)
    
    # Usage tracking
    current_users: Mapped[int] = mapped_column(Integer, default=0)
    current_calls_this_month: Mapped[int] = mapped_column(Integer, default=0)
    current_tokens_this_month: Mapped[int] = mapped_column(Integer, default=0)
    
    # Payment
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String, default="TRY")
    
    # Additional configuration
    # {
    #   "auto_renew": true,
    #   "payment_method": "credit_card",
    #   "custom_features": {...}
    # }
    config: Mapped[dict] = mapped_column(JSONB, nullable=True, default={})
    
    # Cancellation
    cancelled_at: Mapped[datetime] = mapped_column(nullable=True)
    cancellation_reason: Mapped[str] = mapped_column(String, nullable=True)
    
    # Relationships
    # tenant = relationship("Tenant", back_populates="subscriptions")
    # card = relationship("Card")
