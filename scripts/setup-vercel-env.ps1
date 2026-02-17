# Quick Vercel Backend Environment Setup
# Using existing keys and minimal configuration for immediate testing

$PROJECT = "backend"

Write-Host "🚀 Quick Vercel Environment Setup for Testing..." -ForegroundColor Cyan
Write-Host ""

cd C:\Users\icene\Desktop\NEXT-GENT\backend

# Application
Write-Host "📝 Application Settings..." -ForegroundColor Yellow
vercel env add PROJECT_NAME production --value "NextGent" --yes
vercel env add API_V1_STR production --value "/api/v1" --yes
vercel env add ENVIRONMENT production --value "production" --yes
vercel env add DEBUG production --value "false" --yes

# Security (from DEPLOYMENT_KEYS.txt)
Write-Host "🔐 Security Keys..." -ForegroundColor Yellow
vercel env add SECRET_KEY production --value "Q8jlbbQUqykutPkRhg7HxTFgmn7BzLfXCbbwpLg_zY8" --yes
vercel env add ENCRYPTION_KEY production --value "fXACJ43AmGdLJSumrunA2mUtLpD12RTqaAMsu5CEzsU=" --yes

# Supabase Database (from SUPABASE_HIZLI_BASLANGIC.md)
Write-Host "🗄️  Supabase Database..." -ForegroundColor Yellow
Write-Host "⚠️  Using Supabase - ensure database password is correct!" -ForegroundColor Red

$SUPABASE_HOST = "db.kmuwxpyaqpkwfewnsijy.supabase.co"
$SUPABASE_DB = "postgres"
$SUPABASE_USER = "postgres"
$SUPABASE_PORT = "5432"

# Note: Password needs to be provided - using placeholder
$SUPABASE_PASSWORD = Read-Host "Enter Supabase database password"

vercel env add POSTGRES_SERVER production --value $SUPABASE_HOST --yes
vercel env add POSTGRES_USER production --value $SUPABASE_USER --yes
vercel env add POSTGRES_PASSWORD production --value $SUPABASE_PASSWORD --yes
vercel env add POSTGRES_DB production --value $SUPABASE_DB --yes
vercel env add POSTGRES_PORT production --value $SUPABASE_PORT --yes

$DATABASE_URL = "postgresql+asyncpg://${SUPABASE_USER}:${SUPABASE_PASSWORD}@${SUPABASE_HOST}:${SUPABASE_PORT}/${SUPABASE_DB}"
vercel env add DATABASE_URL production --value $DATABASE_URL --yes

# Redis - For testing, make it optional (backend can work without Redis, just slower)
Write-Host "📮 Redis (Optional - will configure if available)..." -ForegroundColor Yellow
$REDIS_URL = Read-Host "Enter Redis URL (press Enter to skip)"

if ($REDIS_URL) {
    vercel env add REDIS_URL production --value $REDIS_URL --yes
    # Parse Redis URL for individual components if needed
    vercel env add REDIS_HOST production --value "redis-host" --yes
    vercel env add REDIS_PORT production --value "6379" --yes
}

# CORS
Write-Host "🌐 CORS..." -ForegroundColor Yellow
vercel env add BACKEND_CORS_ORIGINS production --value "http://localhost:5173,https://nextgent.co,https://next-gent-bbxs21jcs-enesics-projects.vercel.app" --yes

# AI (from config.py - already has default)
Write-Host "🤖 AI Configuration..." -ForegroundColor Yellow
vercel env add OPENAI_API_KEY production --value "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" --yes
vercel env add AI_MODEL production --value "gpt-4o-mini" --yes
vercel env add AI_ENABLED production --value "true" --yes

Write-Host ""
Write-Host "✅ Environment variables configured!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Now redeploying..." -ForegroundColor Yellow
vercel --prod --yes

Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host ""
