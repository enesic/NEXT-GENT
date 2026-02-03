# NEXT-GENT Frontend Development Setup

## Quick Start

### Development Mode (Recommended)
```bash
cd frontend
npm run dev
```

Frontend will be available at: **http://localhost:5173**

### API Configuration

The Vite dev server is configured with a proxy to automatically forward all `/api/v1` requests to the backend at `http://localhost:8001`.

**You don't need to manually configure API URLs** - the proxy handles it automatically:
- Frontend: `http://localhost:5173`
- API requests from frontend: `/api/v1/*` → auto-proxied to `http://localhost:8001/api/v1/*`

### Environment Variables

**`.env.development`** (already configured):
```env
VITE_API_BASE_URL=http://localhost:8001/api/v1
```

**Production Build:**
```bash
npm run build
npm run preview
```

## Troubleshooting

### 401 Unauthorized Error on Login

**Problem:** Frontend requesting `http://localhost/api/v1` instead of `http://localhost:8001/api/v1`

**Solution 1 - Use Dev Server (Recommended):**
```bash
# Stop any production build
# Start dev server
cd frontend
npm run dev
```

**Solution 2 - Check Backend Status:**
```bash
curl http://localhost:8001/api/v1/health
```

**Solution 3 - Clear Cache:**
```bash
# Clear browser cache and localStorage
# Restart dev server
```

### CORS Errors

If you see CORS errors, ensure:
1. Backend is running on port 8001
2. Frontend dev server is running on port 5173
3. Vite proxy is configured (see `vite.config.js`)

### Port Already in Use

```bash
# Find process using port 5173
netstat -ano | findstr :5173

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Restart dev server
npm run dev
```

## Backend Requirements

Ensure backend is running:
```bash
cd backend
uvicorn app.main:app --reload --port 8001
```

Check health:
```bash
curl http://localhost:8001/api/v1/health
```

## Login Credentials

Check `backend/seed_*.py` files for test credentials.
