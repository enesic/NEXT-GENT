from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, Field
from enum import Enum


class InteractionStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


class InteractionBase(BaseModel):
    title: str
    description: Optional[str] = None
    type: str = "appointment"
    start_time: datetime
    end_time: datetime
    client_name: str
    client_email: EmailStr
    client_phone: Optional[str] = None
    
    # Universal Integration: Flexible metadata
    metadata: Optional[Dict[str, Any]] = Field(default=None, alias="meta_data")

    @field_validator('end_time')
    def validate_end_time(cls, v, info):
        if 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('end_time must be after start_time')
        return v


class InteractionCreate(InteractionBase):
    """Schema for creating a new interaction"""
    pass


class InteractionUpdate(BaseModel):
    """Schema for updating an interaction"""
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    client_name: Optional[str] = None
    client_email: Optional[EmailStr] = None
    client_phone: Optional[str] = None
    status: Optional[InteractionStatus] = None
    metadata: Optional[Dict[str, Any]] = None


class InteractionResponse(InteractionBase):
    """Schema for interaction response"""
    id: UUID
    tenant_id: UUID
    status: InteractionStatus
    google_calendar_event_id: Optional[str] = None
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InteractionConflict(BaseModel):
    """Schema for interaction conflict information"""
    conflicting_interaction_id: UUID
    start_time: datetime
    end_time: datetime
    title: str
