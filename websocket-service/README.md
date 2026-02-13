# NextGent WebSocket Service

Minimal FastAPI WebSocket service for real-time notifications.
Designed to run on Railway alongside Vercel REST API.

## Features

- Multi-tenant WebSocket connections
- Isolated connections per tenant_id
- Health check endpoint
- CORS configured for Vercel frontend

## Endpoints

- `GET /` - Service info
- `GET /health` - Health check
- `WS /ws/{tenant_id}` - WebSocket connection

## Deployment to Railway

1. Push to GitHub
2. Connect Railway to this repository
3. Set root directory to `websocket-service`
4. Railway will auto-detect Dockerfile
5. Set environment variables:
   - `FRONTEND_URL`: Your Vercel frontend URL
   - `BACKEND_CORS_ORIGINS`: Additional CORS origins

## Local Testing

```bash
cd websocket-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Test WebSocket:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/your-tenant-id');
ws.onmessage = (event) => console.log(event.data);
```

## Integration with Main API

The main REST API (on Vercel) can trigger WebSocket notifications by:
1. Maintaining a reference to the Railway WebSocket service URL
2. Sending HTTP POST requests to a broadcast endpoint (to be added)
3. Or using a shared Redis pub/sub channel (future enhancement)

For now, WebSocket connections are maintained separately from REST API.
