from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    tenants,
    customers,
    interactions,
    analytics,
    helpdesk,
    satisfaction,
    vapi,  # New
    webhooks,
    websocket,
    metrics,
    callcenter
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["Tenants"])
api_router.include_router(interactions.router, prefix="/interactions", tags=["Interactions"])
api_router.include_router(customers.router, prefix="/customers", tags=["Customers"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
api_router.include_router(helpdesk.router, prefix="/helpdesk", tags=["Helpdesk"])
api_router.include_router(satisfaction.router, prefix="/satisfaction", tags=["Satisfaction"])
api_router.include_router(vapi.router, prefix="/vapi", tags=["Voice AI"])  # New
api_router.include_router(callcenter.router, prefix="/callcenter", tags=["callcenter"])