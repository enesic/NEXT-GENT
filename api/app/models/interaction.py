from datetime import datetime
from sqlalchemy import String, DateTime, Boolean, Text, Enum as SQLEnum, Index, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
import enum

from app.models.base import Base, UUIDMixin, TimestampMixin, TenantMixin


class InteractionStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


class Interaction(Base, UUIDMixin, TimestampMixin, TenantMixin):
    __tablename__ = "interactions"
    
    # Database-level race condition prevention
    # Partial unique index: prevents double-booking for active interactions
    __table_args__ = (
        Index(
            'idx_interactions_no_overlap',
            'tenant_id', 'start_time', 'end_time',
            unique=True,
            postgresql_where=text("status IN ('PENDING', 'CONFIRMED')")
        ),
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Interaction Type (appointment, court_hearing, property_viewing, etc.)
    type: Mapped[str] = mapped_column(String(50), default="appointment", nullable=False, index=True)
    
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    
    # User/Client information
    client_name: Mapped[str] = mapped_column(String(255), nullable=False)
    client_email: Mapped[str] = mapped_column(String(255), nullable=False)
    client_phone: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Status tracking
    status: Mapped[InteractionStatus] = mapped_column(
        SQLEnum(InteractionStatus, name="interaction_status"),
        default=InteractionStatus.PENDING,
        nullable=False
    )
    
    # Universal Integration: Metadata for sector-specific data
    # Medical: { "patient_id": "123", "policy_no": "ABC" }
    # Legal: { "case_no": "2024/1", "court": "Family Court" }
    meta_data: Mapped[dict] = mapped_column(JSONB, nullable=True)
    
    # External Integration IDs
    google_calendar_event_id: Mapped[str] = mapped_column(String(255), nullable=True)
    
    # Concurrency control (optimistic locking for updates)
    version: Mapped[int] = mapped_column(default=1, nullable=False)
