# ============================================================================
# Database Import Script for Vercel Migration (PowerShell version for Windows)
# ============================================================================
# This script imports a database backup to Vercel Postgres.
#
# Prerequisites:
#   - PostgreSQL client tools (pg_restore) installed
#   - Vercel Postgres connection string
#
# Usage: .\scripts\import-database.ps1 "<vercel-postgres-url>" "<backup-file>"
#
# Example:
#   .\scripts\import-database.ps1 "postgres://user:pass@host.vercel-storage.com:5432/verceldb" ".\backups\nextgent_backup.dump"
# ============================================================================

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$ConnectionString,
    
    [Parameter(Mandatory=$true, Position=1)]
    [string]$BackupFile
)

Write-Host "📥 NextGent Database Import Script" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Validate backup file exists
if (-not (Test-Path $BackupFile)) {
    Write-Host "❌ Error: Backup file not found: $BackupFile" -ForegroundColor Red
    Write-Host ""
    Write-Host "Available backup files:" -ForegroundColor Yellow
    Get-ChildItem -Path ".\backups" -Filter "*.dump" | ForEach-Object {
        Write-Host "   - $($_.FullName)" -ForegroundColor Gray
    }
    exit 1
}

# Check if pg_restore is available
try {
    $null = Get-Command pg_restore -ErrorAction Stop
} catch {
    Write-Host "❌ Error: pg_restore not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install PostgreSQL client tools:" -ForegroundColor Yellow
    Write-Host "   1. Download from: https://www.postgresql.org/download/windows/"
    Write-Host "   2. Or use: choco install postgresql" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

# Display import details
Write-Host "📋 Import Details:" -ForegroundColor Cyan
Write-Host "   Backup file: $BackupFile"
Write-Host "   Target: Vercel Postgres"
Write-Host "   Connection: $($ConnectionString.Substring(0, [Math]::Min(50, $ConnectionString.Length)))..."
Write-Host ""

# Warn user
Write-Host "⚠️  WARNING: This will restore data to Vercel Postgres!" -ForegroundColor Yellow
Write-Host "   - Existing data may be overwritten" -ForegroundColor Yellow
Write-Host "   - Make sure you have the correct connection string" -ForegroundColor Yellow
Write-Host ""

$confirmation = Read-Host "Do you want to continue? (yes/no)"
if ($confirmation -ne "yes") {
    Write-Host "❌ Import cancelled by user" -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "🚀 Starting import..." -ForegroundColor Cyan
Write-Host ""

# Run pg_restore
try {
    pg_restore --verbose --clean --no-acl --no-owner -d "$ConnectionString" "$BackupFile"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "================================================" -ForegroundColor Green
        Write-Host "✅ Database Import Completed Successfully!" -ForegroundColor Green
        Write-Host "================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "📝 Next Steps:" -ForegroundColor Yellow
        Write-Host "   1. Update backend environment variables with Vercel Postgres credentials"
        Write-Host "   2. Deploy backend to Railway/Render"
        Write-Host "   3. Test database connection"
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "⚠️  Import completed with warnings" -ForegroundColor Yellow
        Write-Host "   Some errors are normal (e.g., permission warnings)" -ForegroundColor Gray
        Write-Host "   Check the output above for any critical errors" -ForegroundColor Gray
        Write-Host ""
    }
} catch {
    Write-Host ""
    Write-Host "❌ Import failed!" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "   1. Verify connection string is correct"
    Write-Host "   2. Check if Vercel Postgres is accessible"
    Write-Host "   3. Try using SQL format instead:"
    Write-Host "      psql `"$ConnectionString`" < backup.sql"
    Write-Host ""
    exit 1
}
