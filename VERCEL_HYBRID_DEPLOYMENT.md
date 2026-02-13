# 🚀 Vercel Hybrid Deployment Guide

## Architecture

```
┌─────────────┐
│  Frontend   │  ← Vercel (Static + SSR)
│   (Vercel)  │
└─────┬───────┘
      │
      ├──────────────────────────┐
      │                          │
      ▼                          ▼
┌─────────────┐          ┌──────────────┐
│  REST API   │          │  WebSocket   │
│  (Vercel)   │          │  (Railway)   │
└──────┬──────┘          └──────┬───────┘
       │                        │
       ├────────────────────────┤
       ▼                        ▼
┌──────────────┐        ┌──────────────┐
│   Supabase   │        │   Upstash    │
│  PostgreSQL  │        │    Redis     │
└──────────────┘        └──────────────┘
```

## ✅ Completed Steps

- [x] PostgreSQL client installed
- [x] Security keys generated (see `DEPLOYMENT_KEYS.txt`)
- [x] Vercel API structure created (`backend/api/index.py`)
- [x] FastAPI optimized for serverless
- [x] WebSocket service created (`websocket-service/`)
- [x] Frontend configuration updated for hybrid deployment

## 📋 Manual Steps Required

### Step 1: Supabase Database Import

**⏸️ WAITING: Need Supabase password**

Once you provide the password, I will:
```bash
"C:\Program Files\PostgreSQL\16\bin\pg_restore.exe" `
  -d "postgresql://postgres:YOUR-PASSWORD@db.kmuwxpyaqpkwfewnsijy.supabase.co:5432/postgres" `
  -v backups\nextgent_backup_20260212_110141.dump
```

### Step 2: Upstash Redis Setup

**🔴 ACTION NEEDED:**

1. Go to https://vercel.com/dashboard
2. Click on your project → Storage tab
3. Click "Create" → Select "Upstash Redis"
4. Create database → Copy credentials:
   - `REDIS_URL`
   - `REDIS_HOST`
   - `REDIS_PORT`
   - `REDIS_PASSWORD`

### Step 3: Vercel Backend Deployment

**I will do this automatically when ready:**

```bash
cd backend
vercel --prod
```

After deployment, copy the URL (e.g., `https://nextgent-backend.vercel.app`)

### Step 4: Railway WebSocket Deployment

**🔴 ACTION NEEDED:**

1. Go to https://railway.app
2. Login with GitHub
3. New Project → Deploy from GitHub repo
4. Select `NEXT-GENT` repository
5. Settings:
   - **Root Directory**: `websocket-service`
   - **Builder**: Docker
6. Add environment variables:
   ```
   FRONTEND_URL=https://nextgent.vercel.app
   BACKEND_CORS_ORIGINS=https://nextgent.vercel.app,https://your-domain.com
   ```
7. Deploy → Copy URL (e.g., `https://nextgent-ws.up.railway.app`)

### Step 5: Environment Variables Configuration

**🔴 ACTION NEEDED - Vercel Backend:**

Go to Vercel Dashboard → Project → Settings → Environment Variables

Add these variables:

```bash
# Project
PROJECT_NAME=NextGent
API_V1_STR=/api/v1
ENVIRONMENT=production
DEBUG=false

# Security (from DEPLOYMENT_KEYS.txt)
SECRET_KEY=Q8jlbbQUqykutPkRhg7HxTFgmn7BzLfXCbbwpLg_zY8
ENCRYPTION_KEY=fXACJ43AmGdLJSumrunA2mUtLpD12RTqaAMsu5CEzsU=

# Database - Supabase
POSTGRES_SERVER=db.kmuwxpyaqpkwfewnsijy.supabase.co
POSTGRES_USER=postgres
POSTGRES_PASSWORD=[YOUR-SUPABASE-PASSWORD]
POSTGRES_DB=postgres
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://postgres:[PASSWORD]@db.kmuwxpyaqpkwfewnsijy.supabase.co:5432/postgres

# Redis - Upstash (from Step 2)
REDIS_URL=[FROM-UPSTASH]
REDIS_HOST=[FROM-UPSTASH]
REDIS_PORT=[FROM-UPSTASH]
REDIS_PASSWORD=[FROM-UPSTASH]

# CORS
BACKEND_CORS_ORIGINS=https://nextgent.vercel.app,https://your-domain.com

# OpenAI (optional)
OPENAI_API_KEY=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
AI_MODEL=gpt-4o-mini
AI_ENABLED=true
```

### Step 6: Update Frontend URLs

**I will do this automatically after deployments:**

Update `frontend/.env.production`:
```bash
VITE_API_BASE_URL=https://[YOUR-VERCEL-BACKEND].vercel.app/api/v1
VITE_WS_URL=wss://[YOUR-RAILWAY-WS].up.railway.app
```

### Step 7: Redeploy Frontend

**I will do this automatically:**

```bash
cd frontend
vercel --prod
```

## 🧪 Testing Checklist

After all deployments:

- [ ] Backend Health Check: `curl https://[backend].vercel.app/api/v1/health`
- [ ] Frontend Login: https://nextgent.vercel.app
- [ ] Test login: BEA-000001 / 1234
- [ ] Dashboard loads
- [ ] API calls work (check Network tab)
- [ ] WebSocket connects (check Console)
- [ ] Real-time notifications work

## 🐛 Common Issues & Fixes

### Issue: "Database connection failed"
**Fix**: Check Vercel environment variables, ensure DATABASE_URL is correct

### Issue: "CORS error"
**Fix**: Add frontend URL to BACKEND_CORS_ORIGINS in Vercel

### Issue: "WebSocket won't connect"
**Fix**: Check Railway deployment status, ensure FRONTEND_URL is set

### Issue: "Login fails"
**Fix**: Check SECRET_KEY matches between backend and environment variables

## 📞 Next Actions

**What I need from you:**

1. ✅ Supabase password (for database import)
2. ✅ Upstash Redis credentials (after creating in Vercel)
3. ✅ Confirm Railway project created and environment variables set

**What I will do automatically:**

1. Import database to Supabase
2. Deploy backend to Vercel
3. Update frontend with deployment URLs
4. Redeploy frontend
5. Run all tests
6. Fix any issues found

## 🎯 Ready to Deploy?

Reply with:
- Supabase password
- "Upstash created" (with credentials)
- "Railway ready" (with WebSocket URL)

And I'll handle the rest! 🚀
