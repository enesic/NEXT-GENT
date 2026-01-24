from fastapi import APIRouter
from app.api.v1.endpoints import tenants, interactions, customers, analytics, webhooks, websocket, metrics, helpdesk, auth, satisfaction, callcenter

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(interactions.router, prefix="/interactions", tags=["interactions"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
api_router.include_router(helpdesk.router, prefix="/helpdesk", tags=["helpdesk"])
api_router.include_router(satisfaction.router, prefix="/satisfaction", tags=["satisfaction"])
api_router.include_router(callcenter.router, prefix="/callcenter", tags=["callcenter"])