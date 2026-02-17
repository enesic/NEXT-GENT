from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    tenants,
    customers,
    interactions,
    analytics,
    helpdesk,
    satisfaction,
    vapi,
    webhooks,
    # websocket,  # WebSocket is now a separate service on Railway
    metrics,
    callcenter,
    admin_endpoints,
    auth_endpoints,
    user_management_endpoints,
    flow_engine,
    portal_endpoints,
    documents
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["Tenants"])
api_router.include_router(interactions.router, prefix="/interactions", tags=["Interactions"])
api_router.include_router(customers.router, prefix="/customers", tags=["Customers"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
# WebSocket endpoint removed - now running as separate service on Railway
# api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
api_router.include_router(helpdesk.router, prefix="/helpdesk", tags=["Helpdesk"])
api_router.include_router(satisfaction.router, prefix="/satisfaction", tags=["Satisfaction"])
api_router.include_router(vapi.router, prefix="/vapi", tags=["Voice AI"])
api_router.include_router(callcenter.router, prefix="/callcenter", tags=["callcenter"])
# New endpoints
api_router.include_router(admin_endpoints.router, prefix="/admin", tags=["Admin"])
api_router.include_router(auth_endpoints.router, prefix="/auth/admin", tags=["Admin Auth"])
api_router.include_router(user_management_endpoints.router, prefix="/admin", tags=["User Management"])
api_router.include_router(flow_engine.router, prefix="/flow", tags=["Flow Engine"])
api_router.include_router(portal_endpoints.router, prefix="/portal", tags=["Portal"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])