# Set Vercel Environment Variables for Backend
# This script adds all required environment variables to Vercel

$envVars = @{
    "PROJECT_NAME" = "NextGent"
    "API_V1_STR" = "/api/v1"
    "ENVIRONMENT" = "production"
    "DEBUG" = "false"
    "SECRET_KEY" = "Q8jlbbQUqykutPkRhg7HxTFgmn7BzLfXCbbwpLg_zY8"
    "ENCRYPTION_KEY" = "fXACJ43AmGdLJSumrunA2mUtLpD12RTqaAMsu5CEzsU="
    "POSTGRES_SERVER" = "db.eoblpdxlnsuwpaudcvzk.supabase.co"
    "POSTGRES_USER" = "postgres"
    "POSTGRES_PASSWORD" = "enesic3446!"
    "POSTGRES_DB" = "postgres"
    "POSTGRES_PORT" = "5432"
    "DATABASE_URL" = "postgresql+asyncpg://postgres:enesic3446!@db.eoblpdxlnsuwpaudcvzk.supabase.co:5432/postgres"
    "BACKEND_CORS_ORIGINS" = "https://nextgent.vercel.app,https://frontend-one-murex-64.vercel.app"
    "OPENAI_API_KEY" = "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"
    "AI_MODEL" = "gpt-4o-mini"
    "AI_ENABLED" = "true"
}

Write-Host "Setting Vercel Environment Variables for Backend..." -ForegroundColor Green
Write-Host ""

cd backend

foreach ($key in $envVars.Keys) {
    $value = $envVars[$key]
    Write-Host "Adding $key..." -NoNewline
    
    # Use echo to pipe value to vercel env add
    echo $value | vercel env add $key production 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " SKIPPED (may already exist)" -ForegroundColor Yellow
    }
}

cd ..

Write-Host ""
Write-Host "Environment variables set!" -ForegroundColor Green
Write-Host "Redeploying backend to apply variables..."

cd backend
vercel --prod --yes

Write-Host ""
Write-Host "Backend redeployed with environment variables!" -ForegroundColor Green
