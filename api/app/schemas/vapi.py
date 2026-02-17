from typing import Optional
from pydantic import BaseModel, Field


class VapiWebhookRequest(BaseModel):
    """
    Schema for incoming Vapi.ai webhook request.
    """
    assistant_id: str = Field(..., description="Vapi assistant ID")
    customer_number: str = Field(..., description="Customer phone number")
    call_id: Optional[str] = Field(None, description="Call ID")
    
    # Additional Vapi fields
    type: Optional[str] = Field(None, description="Webhook type")
    timestamp: Optional[str] = Field(None, description="Timestamp")


class VapiAssistantModel(BaseModel):
    """Schema for Vapi assistant model configuration."""
    provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 500


class VapiAssistantConfig(BaseModel):
    """Schema for Vapi assistant configuration."""
    model: VapiAssistantModel
    systemPrompt: str = Field(..., description="System prompt for the assistant")
    
    # Optional voice settings
    voice: Optional[dict] = None
    firstMessage: Optional[str] = None


class VapiWebhookResponse(BaseModel):
    """
    Schema for Vapi.ai webhook response.
    
    Format required by Vapi:
    {
        "assistant": {
            "model": {...},
            "systemPrompt": "..."
        }
    }
    """
    assistant: VapiAssistantConfig


class VapiPerformanceLog(BaseModel):
    """Schema for performance logging."""
    call_id: str
    customer_number: str
    customer_segment: Optional[str]
    redis_hit: bool
    response_time_ms: float
    warning: Optional[str] = None
