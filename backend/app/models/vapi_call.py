"""
VAPI Call Tracking Model
Stores encrypted call data with KVKK compliance
"""
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.models.base import Base, UUIDMixin, TimestampMixin, TenantMixin


class CallStatus(str, enum.Enum):
    """Call resolution status"""
    IN_PROGRESS = "in_progress"
    RESOLVED_AI = "resolved_ai"          # AI successfully resolved the issue
    TRANSFERRED_HUMAN = "transferred_human"  # Transferred to live agent
    FAILED = "failed"                    # Call failed/dropped
    COMPLETED = "completed"              # Call completed successfully


class VAPICall(Base, UUIDMixin, TimestampMixin, TenantMixin):
    """
    VAPI Call Records with KVKK-compliant encryption.
    
    PII Fields (Encrypted):
    - caller_name_encrypted
    - caller_phone_encrypted
    - transcript_encrypted
    
    Searchable Fields (Hashed):
    - phone_hash (SHA-256)
    
    Metadata (Not PII):
    - call_duration_seconds
    - call_status
    - etc.
    """
    __tablename__ = "vapi_calls"
    
    # VAPI Integration
    vapi_call_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    # External VAPI call identifier
    
    # Encrypted PII (KVKK Compliant)
    caller_name_encrypted: Mapped[str] = mapped_column(Text, nullable=True)
    # AES-256 encrypted full name
    
    caller_phone_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    # AES-256 encrypted phone number
    
    transcript_encrypted: Mapped[str] = mapped_column(Text, nullable=True)
    # AES-256 encrypted full conversation transcript
    
    # Hashed for Lookup (Irreversible)
    phone_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    # SHA-256 hash of phone number for fast lookup without revealing actual number
    
    # Call Metadata (Not PII)
    call_duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    call_status: Mapped[CallStatus] = mapped_column(
        SQLEnum(CallStatus, name="call_status"),
        default=CallStatus.IN_PROGRESS,
        nullable=False,
        index=True
    )
    
    resolution_type: Mapped[str] = mapped_column(String(100), nullable=True)
    # Description of how the call was resolved
    
    ai_confidence_score: Mapped[float] = mapped_column(nullable=True)
    # AI confidence in resolution (0.0 - 1.0)
    
    # Transfer Information
    transferred_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    # When the call was transferred to human agent
    
    agent_id: Mapped[str] = mapped_column(String(255), nullable=True)
    # ID of the human agent who handled the transfer
    
    transfer_reason: Mapped[str] = mapped_column(Text, nullable=True)
    # Why the call was transferred
    
    # Timestamps
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ended_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Customer Link (if identified)
    customer_id: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    # Links to Customer.id if caller is identified
    
    # Sentiment Analysis (from AI)
    sentiment: Mapped[str] = mapped_column(String(20), nullable=True)
    # positive, neutral, negative
    
    sentiment_score: Mapped[float] = mapped_column(nullable=True)
    # 0.0 (very negative) to 1.0 (very positive)
    
    # Call Quality Metrics
    call_quality_score: Mapped[int] = mapped_column(Integer, nullable=True)
    # 1-5 rating
    
    # Notes (Encrypted)
    notes_encrypted: Mapped[str] = mapped_column(Text, nullable=True)
    # Any additional notes about the call (encrypted)
