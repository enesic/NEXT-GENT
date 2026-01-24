from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum


class MessageProvider(str, Enum):
    """Message provider types"""
    WHATSAPP = "whatsapp"
    VAPI = "vapi"
    TELEGRAM = "telegram"
    SMS = "sms"


class MessageIntent(str, Enum):
    """Message intent types"""
    APPOINTMENT_CREATE = "randevu_olustur"
    APPOINTMENT_CANCEL = "randevu_iptal"
    CUSTOMER_INFO = "musteri_bilgi"
    FALLBACK = "fallback"
    UNKNOWN = "unknown"


class IncomingWebhookMessage(BaseModel):
    """
    Schema for incoming webhook messages from WhatsApp/Vapi.
    
    Example WhatsApp payload:
    {
        "call_id": "123",
        "intent": "randevu_olustur",
        "name": "Ahmet Yılmaz",
        "date": "2026-01-22",
        "time": "10:00",
        "message": "Yarın saat 10'da randevu almak istiyorum"
    }
    """
    # Required fields
    call_id: str = Field(..., description="Unique call/message ID")
    message: str = Field(..., description="Message content")
    
    # Optional fields
    intent: Optional[str] = Field(None, description="Detected intent")
    name: Optional[str] = Field(None, description="Customer name")
    phone: Optional[str] = Field(None, description="Customer phone")
    date: Optional[str] = Field(None, description="Appointment date")
    time: Optional[str] = Field(None, description="Appointment time")
    
    # Metadata
    provider: MessageProvider = Field(MessageProvider.WHATSAPP, description="Message provider")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    # Raw data
    raw_data: Optional[Dict[str, Any]] = Field(None, description="Raw webhook data")
    
    @validator('intent', pre=True, always=True)
    def normalize_intent(cls, v):
        """Normalize intent to MessageIntent enum."""
        if not v:
            return MessageIntent.UNKNOWN.value
        
        # Map common intents
        intent_map = {
            "randevu_olustur": MessageIntent.APPOINTMENT_CREATE.value,
            "appointment_create": MessageIntent.APPOINTMENT_CREATE.value,
            "randevu_iptal": MessageIntent.APPOINTMENT_CANCEL.value,
            "appointment_cancel": MessageIntent.APPOINTMENT_CANCEL.value,
            "musteri_bilgi": MessageIntent.CUSTOMER_INFO.value,
            "customer_info": MessageIntent.CUSTOMER_INFO.value,
            "fallback": MessageIntent.FALLBACK.value,
        }
        
        return intent_map.get(v.lower(), MessageIntent.UNKNOWN.value)


class OutgoingWebhookMessage(BaseModel):
    """Schema for outgoing webhook messages."""
    call_id: str
    message: str
    intent: str
    success: bool = True
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MessageResponse(BaseModel):
    """Schema for message processing response."""
    call_id: str
    intent: MessageIntent
    response_message: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    processing_time_ms: Optional[float] = None
