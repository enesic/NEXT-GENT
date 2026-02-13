# Vercel Deployment Guide - NextGent CRM

This guide will help you deploy your NextGent CRM system from Docker to Vercel (frontend) + Railway/Render (backend).

## Architecture Overview

```
┌─────────────────┐
│  Custom Domain  │
└────────┬────────┘
         │
         v
┌─────────────────┐       ┌──────────────────┐
│  Vercel         │──────>│  Railway/Render  │
│  (Frontend)     │  API  │  (Backend)       │
└─────────────────┘       └────────┬─────────┘
                                   │
                          ┌────────┴────────┐
                          │                 │
                   ┌──────v──────┐   ┌─────v─────┐
                   │   Vercel    │   │  Vercel   │
                   │  Postgres   │   │  KV       │
                   │  (Database) │   │  (Redis)  │
                   └─────────────┘   └───────────┘
```

## Prerequisites

- GitHub account
- Vercel account (sign up at https://vercel.com)
- Railway account (https://railway.app) OR Render account (https://render.com)
- Your domain (optional, but recommended)
- Vercel CLI installed: `npm i -g vercel`
- Docker running (for database export)

## Phase 1: Prepare Files (✅ COMPLETED)

The following files have been created/updated:

- ✅ `vercel.json` - Vercel configuration
- ✅ `frontend/.env.production` - Production environment variables
- ✅ `backend/app/main.py` - Updated CORS configuration
- ✅ `backend/.env.example` - Production configuration examples
- ✅ `frontend/src/composables/useWebSocket.js` - Updated WebSocket connection logic

## Phase 2: Setup Vercel Storage (Postgres + Redis)

### 2.1 Create Vercel Postgres Database

1. Go to https://vercel.com/dashboard
2. Navigate to **Storage** → **Create Database**
3. Select **Postgres**
4. Choose a name: `nextgent-db`
5. Select region: **Frankfurt (fra1)** (or closest to your users)
6. Click **Create**
7. Copy the connection details:
   - `POSTGRES_PRISMA_URL`
   - `POSTGRES_URL`
   - `POSTGRES_URL_NON_POOLING`
   - Individual credentials (host, user, password, database)

### 2.2 Create Vercel KV (Redis)

1. In Vercel Dashboard → **Storage** → **Create Database**
2. Select **KV** (Redis)
3. Choose a name: `nextgent-redis`
4. Select same region as Postgres
5. Click **Create**
6. Copy the connection details:
   - `KV_URL`
   - `KV_REST_API_URL`
   - `KV_REST_API_TOKEN`
   - `KV_REST_API_READ_ONLY_TOKEN`

## Phase 3: Migrate Data from Docker to Vercel Postgres

### 3.1 Export Current Database

Make sure your Docker containers are running:

```bash
# Check if containers are running
docker ps

# If not, start them
docker-compose up -d

# Export database
docker exec nextgent_db pg_dump -U postgres -d nextgent -F c -b -v -f /tmp/nextgent.dump

# Copy dump file to local machine
docker cp nextgent_db:/tmp/nextgent.dump ./nextgent_backup.dump
```

### 3.2 Import to Vercel Postgres

You'll need PostgreSQL client tools installed (`pg_restore`).

```bash
# Use the POSTGRES_URL from Vercel (non-pooling connection)
pg_restore --verbose --clean --no-acl --no-owner -d "postgres://user:pass@host.vercel-storage.com:5432/verceldb" nextgent_backup.dump

# Alternative: If pg_restore fails, use psql with SQL dump
docker exec nextgent_db pg_dump -U postgres -d nextgent > nextgent_backup.sql
psql "postgres://user:pass@host.vercel-storage.com:5432/verceldb" < nextgent_backup.sql
```

**Note**: Keep your `nextgent_backup.dump` file safe as a backup!

## Phase 4: Deploy Backend to Railway

### 4.1 Option A: Deploy to Railway.app (Recommended)

1. **Create Railway Account**: Go to https://railway.app and sign up
2. **Create New Project**: Click **"New Project"** → **"Deploy from GitHub repo"**
3. **Connect GitHub**: Authorize Railway to access your repository
4. **Select Repository**: Choose your NextGent repository
5. **Configure Service**:
   - Service Name: `nextgent-backend`
   - Root Directory: `backend`
   - Builder: **Dockerfile** (auto-detected)

6. **Add Environment Variables**: In Railway dashboard, go to **Variables** tab and add:

```env
# Application
PROJECT_NAME=NextGent
API_V1_STR=/api/v1
ENVIRONMENT=production
DEBUG=false

# Security (GENERATE NEW KEYS FOR PRODUCTION!)
SECRET_KEY=your-new-production-secret-key-change-this
ENCRYPTION_KEY=your-new-encryption-key-change-this

# Database (from Vercel Postgres)
POSTGRES_SERVER=your-postgres-host.vercel-storage.com
POSTGRES_USER=default
POSTGRES_PASSWORD=your-vercel-postgres-password
POSTGRES_DB=verceldb
POSTGRES_PORT=5432
DATABASE_URL=postgres://default:password@host.vercel-storage.com:5432/verceldb

# Redis (from Vercel KV)
REDIS_HOST=your-redis-host.vercel-storage.com
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
REDIS_URL=redis://default:password@host.vercel-storage.com:6379

# CORS (will update after deploying frontend)
BACKEND_CORS_ORIGINS=http://localhost:5173,https://your-domain.vercel.app

# OpenAI (if using AI features)
OPENAI_API_KEY=your-openai-api-key
AI_MODEL=gpt-4o-mini
AI_ENABLED=true
```

**Generate New Keys**:
```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate ENCRYPTION_KEY (Fernet key)
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

7. **Deploy**: Railway will automatically build and deploy
8. **Get Backend URL**: After deployment, copy the public URL (e.g., `https://nextgent-backend-production.up.railway.app`)
9. **Enable Public Networking**: Make sure the service is publicly accessible

### 4.2 Option B: Deploy to Render.com

1. Go to https://render.com and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - Name: `nextgent-backend`
   - Region: **Frankfurt** (or closest)
   - Root Directory: `backend`
   - Environment: **Docker**
   - Instance Type: **Starter** ($7/month) or **Free** (spins down after inactivity)
5. Add environment variables (same as Railway above)
6. Click **"Create Web Service"**
7. Copy the service URL

## Phase 5: Update Frontend Configuration

### 5.1 Update Backend URL

Edit `frontend/.env.production`:

```env
# Replace with your actual backend URL from Railway/Render
VITE_API_BASE_URL=https://nextgent-backend-production.up.railway.app/api/v1
```

### 5.2 Create .env.production.local (optional, for local testing)

```env
VITE_API_BASE_URL=https://nextgent-backend-production.up.railway.app/api/v1
```

Test locally:
```bash
cd frontend
npm run build
npm run preview
```

## Phase 6: Deploy Frontend to Vercel

### 6.1 Option A: Deploy via Vercel CLI

```bash
# Navigate to project root
cd c:\Users\icene\Desktop\NEXT-GENT

# Login to Vercel
vercel login

# Deploy to production
vercel --prod

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? nextgent (or your choice)
# - In which directory is your code? ./
# - Override settings? No
```

### 6.2 Option B: Deploy via GitHub Integration

1. **Connect Repository**:
   - Go to https://vercel.com/new
   - Click **"Import Git Repository"**
   - Select your NextGent repository

2. **Configure Project**:
   - Framework Preset: **Other**
   - Root Directory: `./`
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/dist`

3. **Add Environment Variable**:
   - Key: `VITE_API_BASE_URL`
   - Value: `https://your-backend-url.railway.app/api/v1`

4. **Deploy**: Click **"Deploy"**

5. **Connect Vercel Storage**:
   - Go to Project Settings → Storage
   - Connect the Postgres and KV databases you created earlier

### 6.3 Get Vercel URL

After deployment, you'll get a URL like:
- `https://nextgent.vercel.app` (or your custom subdomain)

## Phase 7: Update CORS Settings

Now that you have your Vercel frontend URL, update the backend CORS settings:

1. Go to Railway/Render dashboard
2. Update `BACKEND_CORS_ORIGINS` environment variable:
   ```
   https://your-domain.vercel.app,https://your-custom-domain.com
   ```
3. Redeploy the backend service

## Phase 8: Connect Custom Domain (Optional)

### 8.1 Add Domain to Vercel

1. In Vercel Dashboard → Your Project → **Settings** → **Domains**
2. Click **"Add"**
3. Enter your domain (e.g., `nextgent.com` or `app.nextgent.com`)
4. Click **"Add"**

### 8.2 Update DNS Records

In your domain registrar (GoDaddy, Namecheap, Cloudflare, etc.):

**For root domain (nextgent.com):**
- Type: **A**
- Name: **@** (or blank)
- Value: `76.76.21.21`
- TTL: 3600

**For subdomain (app.nextgent.com):**
- Type: **CNAME**
- Name: **app**
- Value: `cname.vercel-dns.com`
- TTL: 3600

### 8.3 Wait for SSL Certificate

Vercel automatically provisions SSL certificates. This takes 5-10 minutes.

### 8.4 Update CORS Again

Add your custom domain to backend CORS:

```env
BACKEND_CORS_ORIGINS=https://nextgent.vercel.app,https://nextgent.com,https://app.nextgent.com
```

Redeploy backend.

## Phase 9: Verification & Testing

### 9.1 Health Checks

Test all endpoints:

```bash
# Frontend
curl https://your-domain.vercel.app

# Backend API
curl https://your-backend.railway.app/api/v1/health

# Should return:
# {
#   "status": "healthy",
#   "service": "NextGent",
#   "environment": "production",
#   "checks": {
#     "database": {"status": "healthy"},
#     "redis": {"status": "healthy"}
#   }
# }
```

### 9.2 Test Critical Features

1. **Authentication**:
   - Visit your Vercel URL
   - Try logging in with test credentials:
     - Beauty: `BEA-000001` / PIN: `1234`
     - Hotel: `HOS-000001` / PIN: `1234`
     - Medical: `MED-000001` / PIN: `1234`

2. **Dashboard**:
   - Check if dashboard loads
   - Verify charts and data display
   - Check real-time WebSocket connection (bottom-right indicator)

3. **CRUD Operations**:
   - Create a new customer
   - Create an appointment
   - Check if data persists

4. **API Calls**:
   - Open browser DevTools → Network tab
   - Verify API calls go to backend URL
   - Check for CORS errors (there should be none)

5. **WebSocket**:
   - Check console for WebSocket connection logs
   - Should see: `🔌 Connecting to WebSocket: wss://your-backend.railway.app/api/v1/ws/...`

### 9.3 Performance Monitoring

- **Vercel Analytics**: Enable in Project Settings → Analytics
- **Railway Metrics**: Check in Railway dashboard
- **Database**: Monitor in Vercel Postgres dashboard

## Phase 10: Continuous Deployment

### 10.1 Setup Auto-Deploy

Both Vercel and Railway support auto-deploy from GitHub:

1. **Vercel**: Automatically deploys on push to `main` branch
2. **Railway**: Automatically deploys on push to connected branch

### 10.2 Environment-Specific Deployments

- **Production**: `main` branch → Vercel Production + Railway Production
- **Staging**: `develop` branch → Create separate Vercel/Railway projects
- **Development**: Local Docker setup

## Troubleshooting

### Issue: CORS Errors

**Solution**: Make sure backend `BACKEND_CORS_ORIGINS` includes your Vercel URL:
```bash
# Check backend environment variables
# Update BACKEND_CORS_ORIGINS
# Redeploy backend
```

### Issue: WebSocket Connection Failed

**Solution**: 
1. Check backend WebSocket endpoint: `https://backend-url/api/v1/ws/{tenant_id}`
2. Verify WebSocket is accessible (not blocked by firewall)
3. Check browser console for detailed error messages

### Issue: Database Connection Failed

**Solution**:
1. Verify Vercel Postgres connection string
2. Check if using non-pooling connection for migrations
3. Verify database has tables (check Vercel Postgres dashboard)

### Issue: 502 Bad Gateway on Backend

**Solution**:
1. Check Railway/Render logs for errors
2. Verify environment variables are set correctly
3. Check if database/Redis connections are working

### Issue: Build Failed on Vercel

**Solution**:
1. Check build logs in Vercel dashboard
2. Verify `vercel.json` configuration
3. Test build locally: `cd frontend && npm run build`

## Cost Breakdown

### Vercel
- **Hobby**: Free (100GB bandwidth)
- **Pro**: $20/month (1TB bandwidth, recommended for production)

### Vercel Postgres
- Free tier: 256MB (suitable for testing)
- Pro: $0.26/GB (starts at ~$5/month for small apps)

### Vercel KV (Redis)
- Free tier: 256MB
- Pro: $1/month (1GB)

### Railway
- $5-20/month based on usage
- Free trial: $5 credit

### Render
- Free tier: Available (spins down after inactivity)
- Starter: $7/month
- Standard: $25/month

**Total Estimated Monthly Cost**: $20-50 (production-ready setup)

## Rollback Plan

If something goes wrong:

1. **Keep Docker Setup**: Don't delete docker-compose.yml and Dockerfiles
2. **Database Backup**: Keep `nextgent_backup.dump` file safe
3. **DNS Revert**: Can point domain back to old server
4. **Vercel Rollback**: Instant rollback to previous deployment in Vercel dashboard
5. **Railway Rollback**: Can rollback to previous deployment

## Local Development vs Production

**Local Development** (continues to work):
```bash
docker-compose up
# Access at http://localhost
```

**Production**:
- Frontend: https://your-domain.vercel.app
- Backend: https://your-backend.railway.app
- Database: Vercel Postgres
- Redis: Vercel KV

## Security Checklist

- [ ] Changed `SECRET_KEY` to new random value
- [ ] Changed `ENCRYPTION_KEY` to new random value
- [ ] Updated `BACKEND_CORS_ORIGINS` with specific domains (no wildcards)
- [ ] Set `DEBUG=false` in production
- [ ] Verified HTTPS is enabled on all services
- [ ] Checked database connection limits in Vercel Postgres
- [ ] Enabled Redis password authentication
- [ ] Reviewed API rate limits
- [ ] Enabled Vercel Analytics
- [ ] Setup monitoring/alerts

## Next Steps

After successful deployment:

1. **Setup Monitoring**: Configure error tracking (Sentry, LogRocket)
2. **Performance Testing**: Load test your API endpoints
3. **Backup Strategy**: Setup automated database backups
4. **CI/CD**: Configure GitHub Actions for testing before deploy
5. **Documentation**: Update team documentation with new URLs
6. **DNS TTL**: Lower TTL before major changes, raise after stabilization

## Support & Resources

- **Vercel Docs**: https://vercel.com/docs
- **Railway Docs**: https://docs.railway.app
- **Render Docs**: https://render.com/docs
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/
- **Vue.js Production**: https://vuejs.org/guide/best-practices/production-deployment.html

---

**Deployment completed!** 🎉

Your NextGent CRM is now running on modern cloud infrastructure with:
- ✅ Global CDN for frontend (Vercel)
- ✅ Scalable backend (Railway/Render)
- ✅ Managed database (Vercel Postgres)
- ✅ Managed cache (Vercel KV)
- ✅ Automatic HTTPS
- ✅ Auto-deploy from GitHub
- ✅ Built-in monitoring and analytics
