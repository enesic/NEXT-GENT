"""
Document schemas for API requests and responses.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class DocumentBase(BaseModel):
    """Base schema for document"""
    filename: str
    file_type: str
    size: int


class DocumentCreate(DocumentBase):
    """Schema for creating a document"""
    file_url: Optional[str] = None


class DocumentResponse(DocumentBase):
    """Schema for document response"""
    id: UUID
    tenant_id: UUID
    file_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentUploadResponse(BaseModel):
    """Schema for upload response"""
    id: UUID
    filename: str
    file_type: str
    size: int
    message: str
