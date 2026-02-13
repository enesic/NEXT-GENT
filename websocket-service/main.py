"""
Minimal WebSocket Service for Railway Deployment
Handles real-time notifications only - REST API is on Vercel
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import os

app = FastAPI(title="NextGent WebSocket Service", version="1.0.0")

# CORS Configuration
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost",
    os.getenv("FRONTEND_URL", "https://nextgent.vercel.app"),
]

# Add environment CORS origins
cors_origins_env = os.getenv("BACKEND_CORS_ORIGINS", "")
if cors_origins_env:
    allowed_origins.extend([origin.strip() for origin in cors_origins_env.split(",")])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# WebSocket Connection Manager
class ConnectionManager:
    """Manages WebSocket connections with multi-tenant isolation."""
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, tenant_id: str):
        """Accept WebSocket connection for a tenant."""
        await websocket.accept()
        if tenant_id not in self.active_connections:
            self.active_connections[tenant_id] = []
        self.active_connections[tenant_id].append(websocket)
        print(f"✅ WebSocket Connected: Tenant {tenant_id}")

    def disconnect(self, websocket: WebSocket, tenant_id: str):
        """Remove WebSocket connection."""
        if tenant_id in self.active_connections:
            if websocket in self.active_connections[tenant_id]:
                self.active_connections[tenant_id].remove(websocket)
                print(f"❌ WebSocket Disconnected: Tenant {tenant_id}")
            
            if not self.active_connections[tenant_id]:
                del self.active_connections[tenant_id]

    async def broadcast_to_tenant(self, tenant_id: str, message: dict):
        """Broadcast message to all tenant connections."""
        if tenant_id in self.active_connections:
            connections = self.active_connections[tenant_id][:]
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"⚠️ Error broadcasting to {tenant_id}: {e}")
                    self.disconnect(connection, tenant_id)

manager = ConnectionManager()

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "NextGent WebSocket Service",
        "status": "running",
        "endpoints": {
            "websocket": "/ws/{tenant_id}",
            "health": "/health"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "websocket",
        "active_tenants": len(manager.active_connections),
        "total_connections": sum(len(conns) for conns in manager.active_connections.values())
    }

@app.websocket("/ws/{tenant_id}")
async def websocket_endpoint(websocket: WebSocket, tenant_id: str):
    """WebSocket endpoint for real-time notifications."""
    await manager.connect(websocket, tenant_id)
    try:
        while True:
            # Keep connection alive and handle client messages
            data = await websocket.receive_text()
            # Optional: handle ping/pong or client messages
            # For now, just keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket, tenant_id)
    except Exception as e:
        print(f"⚠️ WebSocket Error for tenant {tenant_id}: {e}")
        manager.disconnect(websocket, tenant_id)
