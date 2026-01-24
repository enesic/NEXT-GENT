from fastapi import APIRouter, BackgroundTasks, HTTPException, status, Header, Depends
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
import time

from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.models.tenant import Tenant
from app.schemas.message import (
    IncomingWebhookMessage,
    MessageResponse,
    MessageProvider
)
from app.schemas.vapi import VapiWebhookRequest, VapiWebhookResponse
from app.services.message_service import MessageService
from app.services.vapi_service import VapiService

router = APIRouter()


@router.post("/whatsapp", response_model=MessageResponse)
async def whatsapp_webhook(
    *,
    message: IncomingWebhookMessage,
    background_tasks: BackgroundTasks,
    x_webhook_secret: Optional[str] = Header(None, description="Webhook secret for authentication"),
):
    """
    WhatsApp webhook endpoint.
    
    Receives messages from WhatsApp, processes them, and sends responses in background.
    
    Features:
    - Pydantic validation
    - Background task for response
    - Exponential backoff retry (3 attempts)
    - Intent routing
    
    Example payload:
    ```json
    {
        "call_id": "123456",
        "message": "Yarın saat 10'da randevu almak istiyorum",
        "intent": "randevu_olustur",
        "name": "Ahmet Yılmaz",
        "phone": "+905551234567",
        "date": "2026-01-22",
        "time": "10:00"
    }
    ```
    """
    start_time = time.time()
    
    # TODO: Validate webhook secret
    # if x_webhook_secret != settings.WEBHOOK_SECRET:
    #     raise HTTPException(status_code=401, detail="Invalid webhook secret")
    
    # Set provider
    message.provider = MessageProvider.WHATSAPP
    
    # Process message (synchronous part)
    response = await MessageService.process_incoming_message(message)
    
    # Send response in background (non-blocking)
    # TODO: Get webhook_url from configuration or message payload
    webhook_url = "https://your-webhook-url.com/response"  # Replace with actual URL
    
    background_tasks.add_task(
        MessageService.send_response_background,
        webhook_url=webhook_url,
        call_id=message.call_id,
        response_message=response.response_message,
        intent=response.intent.value,
        data=response.data
    )
    
    processing_time = (time.time() - start_time) * 1000
    response.processing_time_ms = processing_time
    
    return response


@router.post("/vapi", response_model=MessageResponse)
async def vapi_webhook(
    *,
    message: IncomingWebhookMessage,
    background_tasks: BackgroundTasks,
    x_webhook_secret: Optional[str] = Header(None, description="Webhook secret for authentication"),
):
    """
    Vapi webhook endpoint.
    
    Similar to WhatsApp webhook but for Vapi voice AI platform.
    """
    start_time = time.time()
    
    # Set provider
    message.provider = MessageProvider.VAPI
    
    # Process message
    response = await MessageService.process_incoming_message(message)
    
    # Send response in background
    webhook_url = "https://your-vapi-webhook-url.com/response"
    
    background_tasks.add_task(
        MessageService.send_response_background,
        webhook_url=webhook_url,
        call_id=message.call_id,
        response_message=response.response_message,
        intent=response.intent.value,
        data=response.data
    )
    
    processing_time = (time.time() - start_time) * 1000
    response.processing_time_ms = processing_time
    
    return response


@router.post("/generic", response_model=MessageResponse)
async def generic_webhook(
    *,
    message: IncomingWebhookMessage,
    background_tasks: BackgroundTasks,
    provider: MessageProvider = MessageProvider.WHATSAPP,
    response_webhook_url: Optional[str] = None,
):
    """
    Generic webhook endpoint for any messaging platform.
    
    Args:
        message: Incoming message
        provider: Message provider (whatsapp, vapi, telegram, sms)
        response_webhook_url: Optional webhook URL to send response to
    """
    start_time = time.time()
    
    message.provider = provider
    
    # Process message
    response = await MessageService.process_incoming_message(message)
    
    # Send response in background if webhook URL provided
    if response_webhook_url:
        background_tasks.add_task(
            MessageService.send_response_background,
            webhook_url=response_webhook_url,
            call_id=message.call_id,
            response_message=response.response_message,
            intent=response.intent.value,
            data=response.data
        )
    
    processing_time = (time.time() - start_time) * 1000
    response.processing_time_ms = processing_time
    
    return response


@router.post("/voice/vapi", response_model=VapiWebhookResponse)
async def vapi_voice_webhook(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    request: VapiWebhookRequest,
):
    """
    Vapi.ai voice webhook endpoint with Antigravity speed (< 200ms target).
    
    Workflow:
    1. Get customer segment from Redis (cache-first)
    2. Get tenant system prompt from Redis (cache-first)
    3. Customize prompt based on segment
    4. Return Vapi-compatible response
    5. Log performance (warn if > 200ms)
    
    Example request:
    ```json
    {
        "assistant_id": "asst_123",
        "customer_number": "+905551234567",
        "call_id": "call_456"
    }
    ```
    
    Example response:
    ```json
    {
        "assistant": {
            "model": {
                "provider": "openai",
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 500
            },
            "systemPrompt": "You are a helpful AI assistant..."
        }
    }
    ```
    
    Performance:
    - Target: < 200ms
    - Redis cache hit: ~5-20ms
    - Redis cache miss: ~50-150ms
    - Warning logged if > 200ms
    """
    # Process with Antigravity speed
    response, performance_log = await VapiService.process_vapi_webhook(
        db=db,
        tenant_id=current_tenant.id,
        request=request
    )
    
    # Log performance
    print(f"""
📊 Vapi Webhook Performance:
   Call ID: {performance_log.call_id}
   Customer: {performance_log.customer_number}
   Segment: {performance_log.customer_segment or 'Unknown'}
   Redis Hit: {'✅ YES' if performance_log.redis_hit else '❌ NO'}
   Response Time: {performance_log.response_time_ms}ms
   Status: {'⚡ FAST' if performance_log.response_time_ms < 200 else '⚠️ SLOW'}
    """)
    
    return response


@router.get("/health")
async def webhook_health():
    """Health check endpoint for webhooks."""
    return {
        "status": "healthy",
        "service": "webhook",
        "features": [
            "whatsapp",
            "vapi",
            "vapi_voice",  # NEW!
            "generic",
            "background_tasks",
            "exponential_backoff_retry",
            "antigravity_speed"  # NEW!
        ]
    }
