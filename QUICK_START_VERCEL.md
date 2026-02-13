# Quick Start - Vercel Deployment

This is a quick reference guide for deploying NextGent from Docker to Vercel. For detailed instructions, see [VERCEL_DEPLOYMENT_GUIDE.md](VERCEL_DEPLOYMENT_GUIDE.md).

## Prerequisites Checklist

- [ ] GitHub account
- [ ] Vercel account (https://vercel.com)
- [ ] Railway account (https://railway.app) OR Render account (https://render.com)
- [ ] Vercel CLI installed: `npm i -g vercel`
- [ ] Docker running (for database export)
- [ ] PostgreSQL client tools installed (for database import)

## 5-Step Deployment Process

### Step 1: Setup Vercel Storage (10 minutes)

1. **Create Vercel Postgres**:
   - Go to https://vercel.com/dashboard → Storage → Create Database → Postgres
   - Name: `nextgent-db`, Region: `Frankfurt (fra1)`
   - Copy connection string

2. **Create Vercel KV (Redis)**:
   - Storage → Create Database → KV
   - Name: `nextgent-redis`, Same region
   - Copy connection details

### Step 2: Export & Import Database (15 minutes)

**Export from Docker**:
```powershell
# Windows
.\scripts\export-database.ps1

# Linux/Mac
./scripts/export-database.sh
```

**Import to Vercel Postgres**:
```powershell
# Windows (replace with your actual connection string)
.\scripts\import-database.ps1 "postgres://user:pass@host.vercel-storage.com:5432/verceldb" ".\backups\nextgent_backup_XXXXXX.dump"

# Linux/Mac
pg_restore -d "postgres://user:pass@host.vercel-storage.com:5432/verceldb" -v ./backups/nextgent_backup_XXXXXX.dump
```

### Step 3: Deploy Backend to Railway (20 minutes)

1. Go to https://railway.app → New Project → Deploy from GitHub
2. Select your NextGent repository
3. Root Directory: `backend`
4. Add environment variables (see below)
5. Deploy
6. Copy the public URL (e.g., `https://nextgent-backend.up.railway.app`)

**Required Environment Variables**:
```env
PROJECT_NAME=NextGent
API_V1_STR=/api/v1
ENVIRONMENT=production
DEBUG=false

# Generate new keys!
SECRET_KEY=<generate-with-script-below>
ENCRYPTION_KEY=<generate-with-script-below>

# From Vercel Postgres
POSTGRES_SERVER=<your-host>.vercel-storage.com
POSTGRES_USER=default
POSTGRES_PASSWORD=<your-password>
POSTGRES_DB=verceldb
POSTGRES_PORT=5432
DATABASE_URL=<full-connection-string>

# From Vercel KV
REDIS_HOST=<your-redis-host>.vercel-storage.com
REDIS_PORT=6379
REDIS_PASSWORD=<your-password>
REDIS_URL=<full-redis-url>

# Update after getting Vercel frontend URL
BACKEND_CORS_ORIGINS=http://localhost:5173,https://your-domain.vercel.app

# Optional: OpenAI
OPENAI_API_KEY=your-key
AI_MODEL=gpt-4o-mini
AI_ENABLED=true
```

**Generate Secret Keys**:
```bash
# SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# ENCRYPTION_KEY
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### Step 4: Deploy Frontend to Vercel (10 minutes)

1. **Update Backend URL**:
   Edit `frontend/.env.production`:
   ```env
   VITE_API_BASE_URL=https://nextgent-backend.up.railway.app/api/v1
   ```

2. **Deploy to Vercel**:
   ```bash
   cd c:\Users\icene\Desktop\NEXT-GENT
   vercel --prod
   ```
   
   Or use Vercel Dashboard:
   - Import Git Repository → Select your repo
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/dist`
   - Environment Variable: `VITE_API_BASE_URL=https://your-backend.railway.app/api/v1`

3. Copy Vercel URL (e.g., `https://nextgent.vercel.app`)

### Step 5: Update CORS & Test (10 minutes)

1. **Update Backend CORS**:
   In Railway dashboard, update `BACKEND_CORS_ORIGINS`:
   ```
   https://nextgent.vercel.app,https://your-custom-domain.com
   ```
   Redeploy backend.

2. **Test Deployment**:
   - Visit: `https://nextgent.vercel.app`
   - Login with test credentials:
     - Beauty: `BEA-000001` / PIN: `1234`
     - Hotel: `HOS-000001` / PIN: `1234`
     - Medical: `MED-000001` / PIN: `1234`
   - Check dashboard loads
   - Verify API calls work (check Network tab)
   - Check WebSocket connection (bottom-right indicator)

## Optional: Custom Domain

1. **Add Domain to Vercel**:
   - Project Settings → Domains → Add
   - Enter your domain

2. **Update DNS**:
   - A Record: `@` → `76.76.21.21`
   - Or CNAME: `www` → `cname.vercel-dns.com`

3. **Update CORS**:
   Add custom domain to `BACKEND_CORS_ORIGINS`

## Quick Reference

### Files Created/Modified

✅ `vercel.json` - Vercel configuration
✅ `frontend/.env.production` - Production environment variables
✅ `backend/app/main.py` - Updated CORS
✅ `backend/.env.example` - Production examples
✅ `frontend/src/composables/useWebSocket.js` - WebSocket configuration

### Scripts Available

- `.\scripts\export-database.ps1` - Export Docker database
- `.\scripts\import-database.ps1` - Import to Vercel Postgres
- `.\scripts\export-database.sh` - Linux/Mac version

### URLs to Bookmark

- Vercel Dashboard: https://vercel.com/dashboard
- Railway Dashboard: https://railway.app/dashboard
- Vercel Storage: https://vercel.com/dashboard/stores

## Troubleshooting

### CORS Errors
→ Update `BACKEND_CORS_ORIGINS` in Railway with your Vercel URL

### Database Connection Failed
→ Verify Vercel Postgres connection string in Railway environment variables

### WebSocket Not Connecting
→ Check console logs, ensure backend WebSocket endpoint is accessible

### Build Failed
→ Check Vercel build logs, verify `vercel.json` configuration

## Cost Estimate

- Vercel (Free/Hobby): $0
- Vercel Postgres: ~$5-10/month
- Vercel KV: $0-1/month
- Railway: $5-20/month

**Total**: ~$10-30/month for production-ready setup

## Rollback Plan

1. Keep Docker Compose running
2. Keep database backup: `backups/nextgent_backup_*.dump`
3. Vercel instant rollback: Dashboard → Deployments → Rollback
4. DNS revert: Point domain back to old server

## Need Help?

- Detailed guide: [VERCEL_DEPLOYMENT_GUIDE.md](VERCEL_DEPLOYMENT_GUIDE.md)
- Vercel docs: https://vercel.com/docs
- Railway docs: https://docs.railway.app

---

**Status**: Ready to deploy! 🚀

All configuration files have been created. Follow the 5 steps above to complete your migration.
