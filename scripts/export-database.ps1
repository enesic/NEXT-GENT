# ============================================================================
# Database Export Script for Vercel Migration (PowerShell version for Windows)
# ============================================================================
# This script exports the current Docker PostgreSQL database for migration
# to Vercel Postgres.
#
# Usage: .\scripts\export-database.ps1
# ============================================================================

Write-Host "🗄️  NextGent Database Export Script" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
try {
    docker info 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not running"
    }
} catch {
    Write-Host "❌ Error: Docker is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
    exit 1
}

# Check if nextgent_db container exists
$containerExists = docker ps -a --format "{{.Names}}" | Select-String -Pattern "^nextgent_db$"
if (-not $containerExists) {
    Write-Host "❌ Error: nextgent_db container not found!" -ForegroundColor Red
    Write-Host "Make sure Docker Compose is running: docker-compose up -d" -ForegroundColor Yellow
    exit 1
}

# Check if container is running
$containerRunning = docker ps --format "{{.Names}}" | Select-String -Pattern "^nextgent_db$"
if (-not $containerRunning) {
    Write-Host "⚠️  Warning: nextgent_db container is not running!" -ForegroundColor Yellow
    Write-Host "Starting container..." -ForegroundColor Yellow
    docker-compose up -d db
    Start-Sleep -Seconds 5
}

# Create backup directory
$BACKUP_DIR = ".\backups"
if (-not (Test-Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR | Out-Null
}

# Generate timestamp for backup filename
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$BACKUP_FILE = "$BACKUP_DIR\nextgent_backup_${TIMESTAMP}.dump"
$SQL_BACKUP_FILE = "$BACKUP_DIR\nextgent_backup_${TIMESTAMP}.sql"

Write-Host "📦 Exporting database..." -ForegroundColor Cyan
Write-Host "   Container: nextgent_db"
Write-Host "   Database: nextgent"
Write-Host "   User: postgres"
Write-Host ""

# Export as custom format (recommended for large databases)
Write-Host "Creating binary dump (custom format)..." -ForegroundColor Yellow
docker exec nextgent_db pg_dump -U postgres -d nextgent -F c -b -v -f /tmp/nextgent.dump 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Binary dump created successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to create binary dump" -ForegroundColor Red
    exit 1
}

# Copy to local machine
Write-Host "📋 Copying dump file to local machine..." -ForegroundColor Yellow
docker cp nextgent_db:/tmp/nextgent.dump "$BACKUP_FILE"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dump file copied: $BACKUP_FILE" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to copy dump file" -ForegroundColor Red
    exit 1
}

# Also create SQL version (easier to inspect/edit if needed)
Write-Host ""
Write-Host "Creating SQL dump (text format)..." -ForegroundColor Yellow
docker exec nextgent_db pg_dump -U postgres -d nextgent | Out-File -FilePath "$SQL_BACKUP_FILE" -Encoding UTF8

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ SQL dump created: $SQL_BACKUP_FILE" -ForegroundColor Green
} else {
    Write-Host "⚠️  Warning: Failed to create SQL dump (not critical)" -ForegroundColor Yellow
}

# Get file sizes
$DUMP_SIZE = (Get-Item "$BACKUP_FILE").Length / 1MB
$DUMP_SIZE_STR = "{0:N2} MB" -f $DUMP_SIZE

$SQL_SIZE_STR = "N/A"
if (Test-Path "$SQL_BACKUP_FILE") {
    $SQL_SIZE = (Get-Item "$SQL_BACKUP_FILE").Length / 1MB
    $SQL_SIZE_STR = "{0:N2} MB" -f $SQL_SIZE
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "✅ Database Export Completed Successfully!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Backup Files:" -ForegroundColor Cyan
Write-Host "   Binary dump: $BACKUP_FILE ($DUMP_SIZE_STR)"
if (Test-Path "$SQL_BACKUP_FILE") {
    Write-Host "   SQL dump:    $SQL_BACKUP_FILE ($SQL_SIZE_STR)"
}
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Setup Vercel Postgres database"
Write-Host "   2. Get connection string from Vercel dashboard"
Write-Host "   3. Run import script:"
Write-Host "      .\scripts\import-database.ps1 `"<vercel-postgres-url>`" `"$BACKUP_FILE`""
Write-Host ""
Write-Host "   Or manually restore using pg_restore:"
Write-Host "      pg_restore -d `"<vercel-postgres-url>`" -v `"$BACKUP_FILE`""
Write-Host ""
Write-Host "⚠️  Important: Keep backup files safe!" -ForegroundColor Yellow
Write-Host "   These backups are your safety net for rollback." -ForegroundColor Yellow
Write-Host ""
