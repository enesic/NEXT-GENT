"""
Automation flow engine model.
"""
from sqlalchemy import String, Integer, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base, UUIDMixin, TimestampMixin
import uuid


class Flow(Base, UUIDMixin, TimestampMixin):
    """
    Automation flow model for building custom workflows.
    """
    __tablename__ = "flows"

    # Foreign keys
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Basic info
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Flow configuration
    # {
    #   "trigger": {
    #     "type": "webhook" | "schedule" | "event",
    #     "config": {...}
    #   },
    #   "conditions": [
    #     {
    #       "field": "customer.segment",
    #       "operator": "equals",
    #       "value": "VIP"
    #     }
    #   ],
    #   "actions": [
    #     {
    #       "type": "send_sms" | "send_email" | "create_appointment" | "webhook",
    #       "config": {...}
    #     }
    #   ],
    #   "fallback_actions": [...]
    # }
    config: Mapped[dict] = mapped_column(JSONB, nullable=False, default={})
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_template: Mapped[bool] = mapped_column(Boolean, default=False)  # System template or custom
    
    # Execution stats
    total_executions: Mapped[int] = mapped_column(Integer, default=0)
    successful_executions: Mapped[int] = mapped_column(Integer, default=0)
    failed_executions: Mapped[int] = mapped_column(Integer, default=0)
    
    # Priority (for execution order)
    priority: Mapped[int] = mapped_column(Integer, default=0)  # Higher = more important
    
    # Category/tags for organization
    category: Mapped[str] = mapped_column(String, nullable=True)  # e.g., "customer_engagement", "appointment_management"
    tags: Mapped[list] = mapped_column(JSONB, nullable=True, default=[])
    
    # Relationships
    # tenant = relationship("Tenant", back_populates="flows")


class FlowExecution(Base, UUIDMixin, TimestampMixin):
    """
    Track individual flow executions for analytics and debugging.
    """
    __tablename__ = "flow_executions"

    # Foreign keys
    flow_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("flows.id"), nullable=False, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Execution details
    status: Mapped[str] = mapped_column(String, nullable=False)  # success, failed, partial
    
    # Input/output data
    input_data: Mapped[dict] = mapped_column(JSONB, nullable=True)
    output_data: Mapped[dict] = mapped_column(JSONB, nullable=True)
    
    # Error tracking
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    error_stack: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Performance metrics
    execution_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Which actions were executed
    executed_actions: Mapped[list] = mapped_column(JSONB, nullable=True, default=[])
    
    # Relationships
    # flow = relationship("Flow")
