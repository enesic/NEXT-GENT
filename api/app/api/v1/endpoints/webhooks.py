from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Body, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.tenant import Tenant
from app.services.interaction_service import InteractionService
from app.schemas.interaction import InteractionCreate

router = APIRouter()

@router.post("/{source}/{tenant_slug}", status_code=status.HTTP_200_OK)
async def receive_webhook(
    source: str = Path(..., description="Source of the webhook (n8n, vapi, whatsapp)"),
    tenant_slug: str = Path(..., description="Slug of the tenant receiving the data"),
    payload: Dict[str, Any] = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Generic Webhook Gateway.
    Receives data from external sources and converts it into Interactions.
    Also handles real-time events (transcript, function calls) for Vapi.
    """
    from app.core.websocket import manager

    # 1. Resolve Tenant
    query = select(Tenant).where(Tenant.slug == tenant_slug)
    result = await db.execute(query)
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
        
    # 2. Map payload to Interaction schema based on source
    interaction_data = None
    
    try:
        if source == "vapi-realtime":
            # Real-time events from Vapi (transcript, function-call, etc.)
            message = payload.get("message", {})
            msg_type = message.get("type")
            
            # Broadcast to frontend via WebSocket
            if msg_type == "transcript":
                await manager.broadcast_to_tenant(str(tenant.id), {
                    "type": "TRANSCRIPT",
                    "data": {
                        "role": message.get("role", "ai"),
                        "text": message.get("transcript", ""),
                        "is_final": message.get("transcriptType") == "final"
                    }
                })
            
            elif msg_type == "function-call":
                # Check for "action signals" like booking confirmation
                function_name = message.get("functionCall", {}).get("name")
                if function_name in ["bookInteraction", "confirmDetails"]:
                    await manager.broadcast_to_tenant(str(tenant.id), {
                        "type": "ACTION_SIGNAL",
                        "data": {
                            "action": "CONFIRMATION",
                            "details": f"Function called: {function_name}"
                        }
                    })
                
                await manager.broadcast_to_tenant(str(tenant.id), {
                    "type": "FUNCTION_CALL",
                    "data": message.get("functionCall")
                })

            return {"status": "success", "message": "Realtime event processed"}

        elif source == "n8n":
            # Generic n8n payload structure expected:
            # { "title": "...", "client_name": "...", "client_email": "...", "metadata": {...} }
            interaction_data = InteractionCreate(
                title=payload.get("title", "New Interaction (n8n)"),
                description=payload.get("description"),
                type=payload.get("type", "general"),
                start_time=payload.get("start_time") or datetime.now(),
                end_time=payload.get("end_time") or (datetime.now() + timedelta(minutes=30)),
                client_name=payload.get("client_name", "Unknown Client"),
                client_email=payload.get("client_email", "unknown@example.com"),
                client_phone=payload.get("client_phone"),
                metadata=payload.get("metadata", {})
            )
            
        elif source == "vapi":
            # Vapi.ai call summary payload (End of Call)
            # { "message": { "call": { "customer": {...}, "analysis": {...} } } }
            call = payload.get("message", {}).get("call", {})
            customer = call.get("customer", {})
            analysis = call.get("analysis", {})
            
            interaction_data = InteractionCreate(
                title=f"Voice Call: {analysis.get('summary', 'New Call')[:50]}...",
                description=analysis.get('summary'),
                type="voice_call",
                start_time=datetime.now(), # Approximate, Vapi might send timestamp
                end_time=datetime.now() + timedelta(minutes=5), # Placeholder
                client_name=customer.get("name", "Voice Caller"),
                client_email=customer.get("number", "") + "@phone.com", # Mock email if missing
                client_phone=customer.get("number"),
                metadata={
                    "vapi_call_id": call.get("id"),
                    "recording_url": call.get("recordingUrl"),
                    "transcript": call.get("transcript"),
                    "sentiment": analysis.get("sentiment")
                }
            )
            
            # Broadcast new call to frontend
            await manager.broadcast_to_tenant(str(tenant.id), {
                "type": "NEW_CALL",
                "customer": {
                    "name": customer.get("name", "Voice Caller"),
                    "phone": customer.get("number"),
                    # Add mock segment/history if needed for demo
                    "segment": "Standard", 
                    "history": [] 
                }
            })
            
        elif source == "whatsapp":
            # WhatsApp Business API payload (simplified)
            # { "messages": [ { "from": "...", "text": { "body": "..." } } ] }
            msg = payload.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}).get("messages", [{}])[0]
            sender_id = msg.get("from")
            body = msg.get("text", {}).get("body", "")
            
            interaction_data = InteractionCreate(
                title="WhatsApp Message",
                description=body,
                type="message",
                start_time=datetime.now(),
                end_time=datetime.now() + timedelta(minutes=5),
                client_name=f"WhatsApp User {sender_id}",
                client_email=f"{sender_id}@whatsapp.com",
                client_phone=sender_id,
                metadata={
                    "whatsapp_id": msg.get("id"),
                    "raw_body": body
                }
            )
            
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported webhook source: {source}"
            )
            
        # 3. Create Interaction
        # Note: We rely on InteractionService which does conflict checking.
        # For external sources, we might want to skip strict time conflict checks or handle them gracefully.
        # Here we attempt creation.
        
        await InteractionService.create_interaction(
            db=db,
            tenant_id=tenant.id,
            interaction_data=interaction_data
        )
        
        return {"status": "success", "message": f"Interaction created from {source}"}
        
    except Exception as e:
        # Log error in real app
        print(f"Webhook Error ({source}): {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process webhook: {str(e)}"
        )
