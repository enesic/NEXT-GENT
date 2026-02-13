# ============================================================================
# NextGent Vercel Deployment - Automation Script
# ============================================================================
# This script automates the deployment process as much as possible
# ============================================================================

Write-Host ""
Write-Host "🚀 NextGent Vercel Deployment Automation" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Colors
$success = "Green"
$warning = "Yellow"
$error = "Red"
$info = "Cyan"

# Step 1: Check prerequisites
Write-Host "📋 Step 1: Checking prerequisites..." -ForegroundColor $info
Write-Host ""

# Check if Vercel CLI is installed
try {
    $vercelVersion = vercel --version 2>&1
    Write-Host "   ✅ Vercel CLI installed" -ForegroundColor $success
} catch {
    Write-Host "   ❌ Vercel CLI not found. Installing..." -ForegroundColor $error
    npm install -g vercel
    Write-Host "   ✅ Vercel CLI installed" -ForegroundColor $success
}

# Check if backup exists
$backupFile = "backups\nextgent_backup_20260212_110141.dump"
if (Test-Path $backupFile) {
    $backupSize = (Get-Item $backupFile).Length / 1MB
    Write-Host "   ✅ Database backup found: $([math]::Round($backupSize, 2)) MB" -ForegroundColor $success
} else {
    Write-Host "   ⚠️  Database backup not found at $backupFile" -ForegroundColor $warning
}

# Check Docker containers
$containers = docker ps --format "{{.Names}}" 2>&1 | Select-String "nextgent"
if ($containers) {
    Write-Host "   ✅ Docker containers running" -ForegroundColor $success
} else {
    Write-Host "   ⚠️  Docker containers not running" -ForegroundColor $warning
}

Write-Host ""
Start-Sleep -Seconds 2

# Step 2: Vercel Authentication
Write-Host "📋 Step 2: Vercel Authentication" -ForegroundColor $info
Write-Host ""
Write-Host "   Opening browser for Vercel login..." -ForegroundColor $warning
Write-Host "   Please complete authentication in your browser" -ForegroundColor $warning
Write-Host ""

# This will open the browser
vercel whoami 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "   Please login to Vercel:" -ForegroundColor $warning
    vercel login
}

Write-Host "   ✅ Vercel authentication complete" -ForegroundColor $success
Write-Host ""
Start-Sleep -Seconds 2

# Step 3: Prepare frontend environment
Write-Host "📋 Step 3: Preparing frontend configuration..." -ForegroundColor $info
Write-Host ""

# We'll need to update this after backend deployment
Write-Host "   ⚠️  Backend URL will be updated after Railway deployment" -ForegroundColor $warning
Write-Host "   Current placeholder: https://your-backend-url.railway.app/api/v1" -ForegroundColor $warning
Write-Host ""
Start-Sleep -Seconds 2

# Step 4: Build frontend locally to verify
Write-Host "📋 Step 4: Testing frontend build..." -ForegroundColor $info
Write-Host ""

Set-Location frontend
Write-Host "   Installing dependencies..." -ForegroundColor $info
npm install 2>&1 | Out-Null

Write-Host "   Building frontend..." -ForegroundColor $info
npm run build 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Frontend build successful" -ForegroundColor $success
} else {
    Write-Host "   ❌ Frontend build failed" -ForegroundColor $error
    Set-Location ..
    exit 1
}

Set-Location ..
Write-Host ""
Start-Sleep -Seconds 2

# Step 5: Deploy to Vercel
Write-Host "📋 Step 5: Deploying to Vercel..." -ForegroundColor $info
Write-Host ""
Write-Host "   🚀 Starting Vercel deployment..." -ForegroundColor $info
Write-Host ""

# Deploy to Vercel production
vercel --prod --yes

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "   ✅ Frontend deployed to Vercel!" -ForegroundColor $success
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "   ❌ Vercel deployment failed" -ForegroundColor $error
    exit 1
}

# Step 6: Summary and next steps
Write-Host ""
Write-Host "================================================" -ForegroundColor $success
Write-Host "✅ Automated Deployment Complete!" -ForegroundColor $success
Write-Host "================================================" -ForegroundColor $success
Write-Host ""

Write-Host "📊 Deployment Summary:" -ForegroundColor $info
Write-Host "   ✅ Vercel CLI configured" -ForegroundColor $success
Write-Host "   ✅ Frontend built successfully" -ForegroundColor $success
Write-Host "   ✅ Deployed to Vercel" -ForegroundColor $success
Write-Host ""

Write-Host "📝 Next Manual Steps:" -ForegroundColor $warning
Write-Host ""
Write-Host "1. Setup Vercel Storage:" -ForegroundColor $warning
Write-Host "   - Go to: https://vercel.com/dashboard" -ForegroundColor $info
Write-Host "   - Create Postgres database: nextgent-db" -ForegroundColor $info
Write-Host "   - Create KV Redis database: nextgent-redis" -ForegroundColor $info
Write-Host ""

Write-Host "2. Import Database:" -ForegroundColor $warning
Write-Host "   pg_restore -d `"<vercel-postgres-url>`" -v $backupFile" -ForegroundColor $info
Write-Host ""

Write-Host "3. Deploy Backend to Railway:" -ForegroundColor $warning
Write-Host "   - Go to: https://railway.app" -ForegroundColor $info
Write-Host "   - Deploy from GitHub: backend folder" -ForegroundColor $info
Write-Host "   - Add environment variables" -ForegroundColor $info
Write-Host ""

Write-Host "4. Update CORS:" -ForegroundColor $warning
Write-Host "   - Add your Vercel URL to BACKEND_CORS_ORIGINS" -ForegroundColor $info
Write-Host "   - Redeploy backend" -ForegroundColor $info
Write-Host ""

Write-Host "📚 Detailed Instructions:" -ForegroundColor $info
Write-Host "   DEPLOYMENT_STEPS_TR.md" -ForegroundColor $success
Write-Host ""

Write-Host "🎉 Great job! You're almost there!" -ForegroundColor $success
Write-Host ""
