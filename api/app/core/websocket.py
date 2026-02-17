from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    """
    Manages WebSocket connections with multi-tenant isolation.
    """
    def __init__(self):
        # tenant_id -> List[WebSocket]
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, tenant_id: str):
        """
        Accepts a WebSocket connection and associates it with a tenant_id.
        """
        await websocket.accept()
        if tenant_id not in self.active_connections:
            self.active_connections[tenant_id] = []
        self.active_connections[tenant_id].append(websocket)
        print(f"✅ WebSocket Connected: Tenant {tenant_id}")

    def disconnect(self, websocket: WebSocket, tenant_id: str):
        """
        Removes a WebSocket connection.
        """
        if tenant_id in self.active_connections:
            if websocket in self.active_connections[tenant_id]:
                self.active_connections[tenant_id].remove(websocket)
                print(f"❌ WebSocket Disconnected: Tenant {tenant_id}")
            
            # Clean up empty lists
            if not self.active_connections[tenant_id]:
                del self.active_connections[tenant_id]

    async def broadcast_to_tenant(self, tenant_id: str, message: dict):
        """
        Broadcasts a message to all connected clients of a specific tenant.
        """
        if tenant_id in self.active_connections:
            # Copy list to separate object to avoid modification during iteration issues
            # though unlikely with async/await here, it's safer
            connections = self.active_connections[tenant_id][:]
            
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"⚠️ Error broadcasting to {tenant_id}: {e}")
                    # Could optionally disconnect here if the connection is dead
                    self.disconnect(connection, tenant_id)
        else:
            print(f"ℹ️ No active connections for tenant {tenant_id}")

# Global instance
manager = ConnectionManager()
