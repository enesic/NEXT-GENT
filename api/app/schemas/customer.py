from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from enum import Enum


class CustomerSegment(str, Enum):
    VIP = "vip"
    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"
    REGULAR = "regular"


class CustomerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
    DEBT = "debt"


class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    notes: Optional[str] = None


class CustomerCreate(CustomerBase):
    """Schema for creating a new customer"""
    pass


class CustomerUpdate(BaseModel):
    """Schema for updating a customer"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    segment: Optional[CustomerSegment] = None
    status: Optional[CustomerStatus] = None
    notes: Optional[str] = None


class CustomerResponse(CustomerBase):
    """Schema for customer response"""
    id: UUID
    tenant_id: UUID
    segment: CustomerSegment
    status: CustomerStatus
    total_orders: int
    total_spent: float
    lifetime_value: float
    debt_amount: float
    last_order_date: Optional[datetime] = None
    last_contact_date: Optional[datetime] = None
    referral_code: Optional[str] = None
    referred_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CustomerStatusCheck(BaseModel):
    """Schema for customer status check result"""
    customer_id: UUID
    phone: str
    full_name: str
    segment: CustomerSegment
    status: CustomerStatus
    is_vip: bool
    is_gold: bool
    has_debt: bool
    is_inactive: bool
    is_blocked: bool
    total_orders: int
    total_spent: float
    debt_amount: float
    last_order_date: Optional[datetime] = None
    days_since_last_order: Optional[int] = None
    recommendation: str  # Önerilen aksiyon


class CustomerSegmentationResult(BaseModel):
    """Schema for customer segmentation result"""
    customer_id: UUID
    previous_segment: CustomerSegment
    new_segment: CustomerSegment
    reason: str
    metrics: dict
