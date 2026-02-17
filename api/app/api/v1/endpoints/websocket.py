from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket import manager

router = APIRouter()

@router.websocket("/{tenant_id}")
async def websocket_endpoint(websocket: WebSocket, tenant_id: str):
    """
    WebSocket endpoint for real-time notifications.
    Isolated by tenant_id.
    """
    await manager.connect(websocket, tenant_id)
    try:
        while True:
            # Just keep the connection alive and listen for messages (ping/pong)
            # We don't expect much upstream traffic from client, mostly downstream notifications
            data = await websocket.receive_text()
            # Optional: handle client-side heartbeats or messages
            # await websocket.send_text(f"Message received: {data}")
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, tenant_id)
    except Exception as e:
        print(f"⚠️ WebSocket Error for tenant {tenant_id}: {e}")
        manager.disconnect(websocket, tenant_id)
