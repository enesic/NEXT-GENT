from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TenantBase(BaseModel):
    name: str
    slug: str
    domain: Optional[str] = None
    is_active: bool = True
    webhook_url: Optional[str] = None

class TenantCreate(TenantBase):
    pass

class TenantUpdate(TenantBase):
    name: Optional[str] = None
    slug: Optional[str] = None
    is_active: Optional[bool] = None

class TenantResponse(TenantBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
