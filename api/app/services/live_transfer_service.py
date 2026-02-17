from typing import Dict, Any, List, Optional
from uuid import UUID
from datetime import datetime
from app.core.websocket import manager

class LiveTransferService:
    """
    Manages live transfers from AI to Human Agents.
    Uses WebSocket to notify available agents.
    """
    
    @staticmethod
    async def request_transfer(
        tenant_id: str,
        call_id: str,
        caller_phone: str,
        reason: str,
        transcript_summary: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Broadcast incoming call transfer request to all connected agents of the tenant.
        """
        
        # 1. Structure the notification payload
        notification = {
            "type": "incoming_transfer",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "call_id": call_id,
                "caller_phone": caller_phone, # In prod, mask this!
                "reason": reason,
                "summary": transcript_summary,
                "context": context,
                "priority": "high",
                "timeout": 30 # seconds to accept
            }
        }
        
        # 2. Broadcast to tenant's agents
        # The manager handles finding the connections
        await manager.broadcast_to_tenant(tenant_id, notification)
        
        # 3. Log the transfer request (Simulated persistence)
        # In real app, save to 'Transfers' table
        print(f"🔥 Live Transfer Requested: {call_id} -> Tenant {tenant_id} (Reason: {reason})")
        
        return {
            "status": "broadcast_sent",
            "agents_notified": True # We assume best effort
        }

    @staticmethod
    async def agent_accepted_transfer(
        tenant_id: str,
        user_id: str,
        call_id: str
    ):
        """
        Handle agent accepting the call.
        Notify other agents that it's taken.
        """
        notification = {
            "type": "transfer_accepted",
            "data": {
                "call_id": call_id,
                "accepted_by": user_id
            }
        }
        await manager.broadcast_to_tenant(tenant_id, notification)
