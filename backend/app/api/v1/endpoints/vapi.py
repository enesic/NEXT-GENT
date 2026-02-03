from datetime import datetime
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.core.database import get_db
from app.core.encryption import encryption_service
from app.models.vapi_call import VAPICall, CallStatus
from app.models.tenant import Tenant
from app.models.customer import Customer
from app.services.webhook_service import WebhookService

router = APIRouter()

# --- Schemas ---

class VAPIArtifact(BaseModel):
    recordingUrl: Optional[str] = None
    transcript: Optional[str] = None
    
class VAPIAnalysis(BaseModel):
    summary: Optional[str] = None
    structuredData: Optional[Dict[str, Any]] = None
    successEvaluation: Optional[str] = None # boolean as string sometimes

class VAPIMessage(BaseModel):
    role: str
    message: str
    time: Optional[float] = None
    
class VAPIWebhookPayload(BaseModel):
    """
    Structure of webhook payload from VAPI
    Ref: https://docs.vapi.ai/server-url/events
    """
    type: str # e.g. "call.ended"
    call: Dict[str, Any]
    transcript: Optional[str] = None
    messages: Optional[List[VAPIMessage]] = None
    analysis: Optional[VAPIAnalysis] = None
    
    class Config:
        extra = "allow" # Allow extra fields from VAPI


# --- Endpoints ---

@router.post("/webhook")
async def vapi_webhook(
    payload: VAPIWebhookPayload,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Receives events from VAPI (voice AI provider).
    
    Handles:
    - call.ended: Process transcript, encrypt PII, save to DB
    - call.analysis: Detailed analysis
    
    Data Privacy:
    - Encrypts caller name, phone, transcript
    - Hashes phone for search
    """
    event_type = payload.type
    
    if event_type == "call.ended":
        background_tasks.add_task(process_call_ended, payload, db)
    elif event_type == "function-call":
        # Handle live function calls during call (e.g. check_appointment)
        # Note: Function calls might need synchronous response if Vapi waits for it.
        # But for heavy processing, we can offload.
        # However, Vapi expects a result from function calls usually.
        # Let's keep distinct logic: call.ended is fire-and-forget. function-call is sync.
        return await process_function_call(payload, db)
        
    return {"status": "received"}


# --- Processing Logic ---

async def process_call_ended(payload: VAPIWebhookPayload, db: AsyncSession):
    call_data = payload.call
    analysis = payload.analysis
    
    # 1. Extract PII
    caller_phone = call_data.get("customer", {}).get("number", "")
    caller_name = call_data.get("customer", {}).get("name", "Unknown")
    transcript = payload.transcript or ""
    
    # If transcript is empty, try to reconstruction from messages
    if not transcript and payload.messages:
        transcript = "\n".join([f"{m.role}: {m.message}" for m in payload.messages])

    # 2. Encrypt PII (KVKK Compliance)
    encrypted_phone = encryption_service.encrypt_pii(caller_phone)
    encrypted_name = encryption_service.encrypt_pii(caller_name)
    encrypted_transcript = encryption_service.encrypt_pii(transcript)
    
    # 3. Hash for lookup
    phone_hash = encryption_service.hash_phone_for_lookup(caller_phone)
    
    # 4. Extract Metadata
    vapi_call_id = call_data.get("id")
    started_at_str = call_data.get("startedAt")
    ended_at_str = call_data.get("endedAt")
    
    started_at = datetime.fromisoformat(started_at_str.replace('Z', '+00:00')) if started_at_str else datetime.utcnow()
    ended_at = datetime.fromisoformat(ended_at_str.replace('Z', '+00:00')) if ended_at_str else datetime.utcnow()
    
    duration = int((ended_at - started_at).total_seconds())
    
    # 5. Determine Resolution Status
    status = CallStatus.COMPLETED
    if analysis and analysis.successEvaluation == "false":
        status = CallStatus.FAILED
    
    # 6. Find Tenant (assuming passed in call metadata or default)
    # Since VAPI holds the phone number config, we might map phone -> tenant
    # For MVP, we will use the first active tenant or look for custom metadata
    assistant_overrides = call_data.get("assistantOverrides", {})
    metadata = assistant_overrides.get("metadata", {})
    tenant_id_str = metadata.get("tenant_id")
    
    tenant_id = None
    if tenant_id_str:
        tenant_id = tenant_id_str
    else:
        # Fallback: Get Default Tenant
        result = await db.execute(select(Tenant).limit(1))
        tenant = result.scalar_one_or_none()
        if tenant:
            tenant_id = tenant.id
            
    if not tenant_id:
        print("⚠️ Warning: No tenant found for VAPI call")
        return

    # 7. Find Customer (if exists)
    customer_id = None
    if phone_hash:
        # Check by phone hash (fast secure lookup with encrypted phone)
        customer_result = await db.execute(
            select(Customer).where(Customer.phone_hash == phone_hash)
        )
        customer = customer_result.scalar_one_or_none()
        if customer:
            customer_id = str(customer.id)

    # 8. Save Record
    vapi_record = VAPICall(
        tenant_id=tenant_id,
        vapi_call_id=vapi_call_id,
        
        caller_name_encrypted=encrypted_name,
        caller_phone_encrypted=encrypted_phone,
        transcript_encrypted=encrypted_transcript,
        
        phone_hash=phone_hash,
        
        started_at=started_at,
        ended_at=ended_at,
        call_duration_seconds=duration,
        call_status=status,
        
        customer_id=customer_id,
        
        # Analysis results
        resolution_type="ai_handled",
        ai_confidence_score=0.9, # Mock for now
        
        sentiment=analysis.summary if analysis else None # Using summary as placeholder
    )
    
    db.add(vapi_record)
    await db.commit()
    print(f"✅ VAPI Call saved: {vapi_call_id} (Duration: {duration}s)")


async def process_function_call(payload: VAPIWebhookPayload, db: AsyncSession):
    """
    Handle function calls from VAPI assistant
    Example: Check appointment availability
    """
    call = payload.call
    function_call = call.get("function", {})
    name = function_call.get("name")
    args = function_call.get("arguments", {}) # String or dict
    
    import json
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except json.JSONDecodeError:
            args = {}
            
    response = {"result": "Function not implemented"}
    
    if name == "checkAvailability":
        # Mock logic
        response = {"available": True, "slots": ["10:00", "14:00"]}
        
    elif name == "transferToAgent":
        # Handle Live Transfer
        reason = args.get("reason", "Customer requested agent")
        summary = args.get("summary", "")
        call_id = call.get("id")
        
        # Get tenant_id from metadata or fallback
        assistant_overrides = call.get("assistantOverrides", {})
        metadata = assistant_overrides.get("metadata", {})
        tenant_id = metadata.get("tenant_id", "demo-tenant-id")
        
        customer_phone = call.get("customer", {}).get("number", "Unknown")
        
        # Trigger WebSocket Broadcast
        from app.services.live_transfer_service import LiveTransferService
        await LiveTransferService.request_transfer(
            tenant_id=tenant_id,
            call_id=call_id,
            caller_phone=customer_phone,
            reason=reason,
            transcript_summary=summary
        )
        
        response = {"status": "transfer_initiated", "message": "Agent is being notified"}

    return response # VAPI expects JSON response
