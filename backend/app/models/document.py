"""
Document model for file management.
"""
from datetime import datetime
from uuid import UUID
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin, TenantMixin


class Document(Base, UUIDMixin, TimestampMixin, TenantMixin):
    __tablename__ = "documents"

    # File metadata
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_url: Mapped[str] = mapped_column(String(512), nullable=True)  # S3 URL or local path
    file_type: Mapped[str] = mapped_column(String(100), nullable=False)  # MIME type
    size: Mapped[int] = mapped_column(Integer, nullable=False)  # Size in bytes

    # Relationships
    # tenant relationship will be added when we have proper FK setup
    
    def __repr__(self):
        return f"<Document {self.filename} ({self.file_type})>"
