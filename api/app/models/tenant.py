from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base, UUIDMixin, TimestampMixin

class Tenant(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String, index=True)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    domain: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Universal Integration: Tenant Configuration
    # { 
    #   "sector": "medical",
    #   "validation_rules": { ... },
    #   "privacy_rules": [ "patient_id", "diagnosis" ]
    # }
    config: Mapped[dict] = mapped_column(JSONB, nullable=True)
    
    # Webhook URL for external integrations (n8n, Zapier, etc.)
    webhook_url: Mapped[str] = mapped_column(String, nullable=True)
    
    # System prompt for Vapi.ai voice assistant
    system_prompt: Mapped[str] = mapped_column(String, nullable=True)
