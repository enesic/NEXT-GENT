"""
Audit Log Model - KVKK Compliant Logging System
All PII data is hashed/masked before storage
"""
from sqlalchemy import String, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timedelta
from app.models.base import Base, UUIDMixin, TimestampMixin


class ActionType(str):
    """Audit action types"""
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    EXPORT = "EXPORT"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    ANONYMIZE = "ANONYMIZE"
    PASSWORD_CHANGE = "PASSWORD_CHANGE"


class AuditLog(Base, UUIDMixin, TimestampMixin):
    """
    KVKK-compliant audit log.
    Stores administrative actions with automatic retention policy.
    """
    __tablename__ = "audit_logs"
    
    # Action Details
    action_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String, nullable=False, index=True)  # e.g., "customer", "admin", "call"
    resource_id_hash: Mapped[str] = mapped_column(String, nullable=True, index=True)  # Hashed ID for privacy
    
    # Actor Information
    admin_user_id: Mapped[str] = mapped_column(String, nullable=True, index=True)  # Admin who performed action
    ip_address: Mapped[str] = mapped_column(String, nullable=True)
    user_agent: Mapped[str] = mapped_column(String, nullable=True)
    
    # Change Details (masked)
    # Example: {
    #   "before": {"email": "te***@example.com", "name": "A*** Y***"},
    #   "after": {"email": "ne***@example.com", "name": "A*** Y***"},
    #   "action_details": "Email updated by admin"
    # }
    changes: Mapped[dict] = mapped_column(JSONB, nullable=True)
    
    # KVKK Retention (6 months by default)
    retention_until: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False,
        default=lambda: datetime.utcnow() + timedelta(days=180)
    )
    
    # Status
    is_visible: Mapped[bool] = mapped_column(default=True, nullable=False)  # For soft delete
    
    __table_args__ = (
        Index('idx_audit_created_at', 'created_at'),
        Index('idx_audit_retention', 'retention_until'),
        Index('idx_audit_admin_action', 'admin_user_id', 'action_type'),
    )
    
    def __repr__(self):
        return f"<AuditLog {self.action_type} on {self.resource_type}>"
    
    def is_expired(self) -> bool:
        """Check if log has passed retention period"""
        return datetime.utcnow() > self.retention_until
    
    @classmethod
    def create_log(
        cls, 
        action_type: str,
        resource_type: str,
        admin_user_id: str = None,
        resource_id: str = None,
        ip_address: str = None,
        user_agent: str = None,
        changes: dict = None
    ):
        """
        Factory method to create audit log with hashed resource ID
        """
        from app.core.pii_masker import pii_masker
        
        resource_id_hash = None
        if resource_id:
            resource_id_hash = pii_masker.hash_pii(resource_id)
        
        # Mask changes if present
        masked_changes = None
        if changes:
            masked_changes = pii_masker.mask_dict(changes)
        
        return cls(
            action_type=action_type,
            resource_type=resource_type,
            resource_id_hash=resource_id_hash,
            admin_user_id=admin_user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            changes=masked_changes
        )
