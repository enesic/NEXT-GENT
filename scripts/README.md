# Database Migration Scripts

This directory contains scripts to help migrate your database from Docker to Vercel Postgres.

## Scripts Overview

### 1. Export Database Scripts

Export your current PostgreSQL database from Docker container.

**Windows (PowerShell)**:
```powershell
.\scripts\export-database.ps1
```

**Linux/Mac (Bash)**:
```bash
chmod +x ./scripts/export-database.sh
./scripts/export-database.sh
```

**What it does**:
- Checks if Docker and database container are running
- Creates a backup directory if it doesn't exist
- Exports database in two formats:
  - Binary format (`.dump`) - Recommended for restore
  - SQL format (`.sql`) - For inspection and manual edits
- Saves backups with timestamp: `backups/nextgent_backup_YYYYMMDD_HHMMSS.dump`

**Output**:
```
🗄️  NextGent Database Export Script
====================================

📦 Exporting database...
   Container: nextgent_db
   Database: nextgent
   User: postgres

✅ Binary dump created successfully
✅ Dump file copied: .\backups\nextgent_backup_20260212_143000.dump
✅ SQL dump created: .\backups\nextgent_backup_20260212_143000.sql

================================================
✅ Database Export Completed Successfully!
================================================
```

### 2. Import Database Script

Import your database backup to Vercel Postgres.

**Windows (PowerShell)**:
```powershell
.\scripts\import-database.ps1 "<vercel-postgres-url>" "<backup-file-path>"
```

**Example**:
```powershell
.\scripts\import-database.ps1 "postgres://default:pass@host.vercel-storage.com:5432/verceldb" ".\backups\nextgent_backup_20260212_143000.dump"
```

**What it does**:
- Validates backup file exists
- Checks if `pg_restore` is installed
- Shows import details and asks for confirmation
- Restores database to Vercel Postgres
- Reports success or errors

**Prerequisites**:
- PostgreSQL client tools (`pg_restore`) must be installed
- Vercel Postgres connection string (get from Vercel dashboard)

## Installation of PostgreSQL Client Tools

### Windows

**Option 1: Official Installer**
1. Download from: https://www.postgresql.org/download/windows/
2. Run installer
3. Select only "Command Line Tools"
4. Add to PATH when prompted

**Option 2: Chocolatey**
```powershell
choco install postgresql
```

**Option 3: Scoop**
```powershell
scoop install postgresql
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install postgresql-client
```

### macOS

```bash
# Using Homebrew
brew install postgresql
```

## Verifying Installation

Test if PostgreSQL client tools are installed:

```bash
pg_restore --version
psql --version
```

Should output version information like:
```
pg_restore (PostgreSQL) 15.x
psql (PostgreSQL) 15.x
```

## Getting Vercel Postgres Connection String

1. Go to https://vercel.com/dashboard
2. Navigate to your project → **Storage** tab
3. Click on your Postgres database
4. Go to **Connection** section
5. Copy the connection string:
   - Use `POSTGRES_URL` for connection pooling (general use)
   - Use `POSTGRES_URL_NON_POOLING` for migrations/admin tasks

**Connection string format**:
```
postgres://username:password@host.vercel-storage.com:5432/database
```

## Usage Flow

### Full Migration Process

```powershell
# Step 1: Export database from Docker
.\scripts\export-database.ps1

# Output: .\backups\nextgent_backup_YYYYMMDD_HHMMSS.dump

# Step 2: Setup Vercel Postgres (in Vercel dashboard)
# - Create new Postgres database
# - Copy connection string

# Step 3: Import to Vercel Postgres
.\scripts\import-database.ps1 `
  "postgres://default:pass@host.vercel-storage.com:5432/verceldb" `
  ".\backups\nextgent_backup_20260212_143000.dump"

# Step 4: Verify import
# Test backend with new database connection
```

## Backup Directory Structure

After running export script:

```
NEXT-GENT/
├── backups/
│   ├── nextgent_backup_20260212_143000.dump  # Binary format
│   ├── nextgent_backup_20260212_143000.sql   # SQL format
│   ├── nextgent_backup_20260213_100000.dump
│   └── nextgent_backup_20260213_100000.sql
├── scripts/
│   ├── export-database.ps1
│   ├── export-database.sh
│   ├── import-database.ps1
│   └── README.md
```

## Troubleshooting

### Export Script Issues

**Problem**: "Docker is not running"
**Solution**: Start Docker Desktop and wait for it to fully start

**Problem**: "nextgent_db container not found"
**Solution**: Run `docker-compose up -d` to start containers

**Problem**: "Permission denied"
**Solution (Linux/Mac)**: Make script executable: `chmod +x scripts/*.sh`

### Import Script Issues

**Problem**: "pg_restore not found"
**Solution**: Install PostgreSQL client tools (see above)

**Problem**: "Connection refused"
**Solution**: 
- Check if Vercel Postgres is accessible
- Verify connection string is correct
- Check if IP is whitelisted (if required)

**Problem**: "role 'postgres' does not exist"
**Solution**: This is normal, use the `--no-owner --no-acl` flags (already included in script)

**Problem**: "Import completed with warnings"
**Solution**: 
- Some warnings are expected (permission issues, role doesn't exist, etc.)
- Check if data was imported: Connect to Vercel Postgres and verify tables exist
- Critical errors will show "ERROR:" in output

## Manual Import Methods

If scripts fail, try manual methods:

### Method 1: Using pg_restore directly

```bash
pg_restore --verbose --clean --no-acl --no-owner \
  -d "postgres://user:pass@host.vercel-storage.com:5432/verceldb" \
  ./backups/nextgent_backup.dump
```

### Method 2: Using SQL file

```bash
psql "postgres://user:pass@host.vercel-storage.com:5432/verceldb" \
  < ./backups/nextgent_backup.sql
```

### Method 3: Via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Connect to database
vercel env pull .env.vercel

# Use connection string from .env.vercel
pg_restore -d "<connection-string>" ./backups/nextgent_backup.dump
```

## Best Practices

1. **Always keep backups**: Don't delete backup files after import
2. **Test import**: Verify data after import before proceeding
3. **Export before changes**: Create backup before major changes
4. **Use timestamps**: Scripts automatically add timestamps to backups
5. **Version control**: Don't commit backup files to Git (already in .gitignore)

## Security Notes

- Backup files contain sensitive data - keep them secure
- Don't commit backups to version control
- Don't share connection strings publicly
- Use environment variables for credentials
- Rotate database passwords regularly

## Support

For issues or questions:
1. Check [VERCEL_DEPLOYMENT_GUIDE.md](../VERCEL_DEPLOYMENT_GUIDE.md)
2. Check [QUICK_START_VERCEL.md](../QUICK_START_VERCEL.md)
3. Vercel documentation: https://vercel.com/docs/storage/vercel-postgres
4. PostgreSQL documentation: https://www.postgresql.org/docs/

---

**Last Updated**: 2026-02-12
