from datetime import datetime
from sqlalchemy import String, Text, Integer, Enum as SQLEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.models.base import Base, UUIDMixin, TimestampMixin, TenantMixin


class WebhookStatus(str, enum.Enum):
    PENDING = "pending"
    FAILED = "failed"
    RETRYING = "retrying"
    MANUALLY_SENT = "manually_sent"


class FailedWebhook(Base, UUIDMixin, TimestampMixin, TenantMixin):
    """
    Failed webhook log for manual retry from admin panel.
    Stores webhook attempts that failed after all retries.
    """
    __tablename__ = "failed_webhooks"

    # Webhook details
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    webhook_url: Mapped[str] = mapped_column(String(500), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    
    # Failure tracking
    status: Mapped[WebhookStatus] = mapped_column(
        SQLEnum(WebhookStatus, name="webhook_status"),
        default=WebhookStatus.FAILED,
        nullable=False,
        index=True
    )
    
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_error: Mapped[str] = mapped_column(Text, nullable=True)
    last_status_code: Mapped[int] = mapped_column(Integer, nullable=True)
    last_attempt_at: Mapped[datetime] = mapped_column(nullable=True)
    
    # Related entity (for context)
    related_entity_type: Mapped[str] = mapped_column(String(50), nullable=True)  # e.g., "appointment"
    related_entity_id: Mapped[str] = mapped_column(String(100), nullable=True, index=True)
    
    # Manual retry tracking
    manually_retried_at: Mapped[datetime] = mapped_column(nullable=True)
    manually_retried_by: Mapped[str] = mapped_column(String(100), nullable=True)
