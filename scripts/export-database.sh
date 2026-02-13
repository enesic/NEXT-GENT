#!/bin/bash

# ============================================================================
# Database Export Script for Vercel Migration
# ============================================================================
# This script exports the current Docker PostgreSQL database for migration
# to Vercel Postgres.
#
# Usage: ./scripts/export-database.sh
# ============================================================================

echo "🗄️  NextGent Database Export Script"
echo "===================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running!"
    echo "Please start Docker and try again."
    exit 1
fi

# Check if nextgent_db container exists
if ! docker ps -a --format '{{.Names}}' | grep -q "^nextgent_db$"; then
    echo "❌ Error: nextgent_db container not found!"
    echo "Make sure Docker Compose is running: docker-compose up -d"
    exit 1
fi

# Check if container is running
if ! docker ps --format '{{.Names}}' | grep -q "^nextgent_db$"; then
    echo "⚠️  Warning: nextgent_db container is not running!"
    echo "Starting container..."
    docker-compose up -d db
    sleep 5
fi

# Create backup directory
BACKUP_DIR="./backups"
mkdir -p "$BACKUP_DIR"

# Generate timestamp for backup filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/nextgent_backup_${TIMESTAMP}.dump"
SQL_BACKUP_FILE="$BACKUP_DIR/nextgent_backup_${TIMESTAMP}.sql"

echo "📦 Exporting database..."
echo "   Container: nextgent_db"
echo "   Database: nextgent"
echo "   User: postgres"
echo ""

# Export as custom format (recommended for large databases)
echo "Creating binary dump (custom format)..."
docker exec nextgent_db pg_dump -U postgres -d nextgent -F c -b -v -f /tmp/nextgent.dump 2>&1 | grep -v "^pg_dump:"

if [ $? -eq 0 ]; then
    echo "✅ Binary dump created successfully"
else
    echo "❌ Failed to create binary dump"
    exit 1
fi

# Copy to local machine
echo "📋 Copying dump file to local machine..."
docker cp nextgent_db:/tmp/nextgent.dump "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Dump file copied: $BACKUP_FILE"
else
    echo "❌ Failed to copy dump file"
    exit 1
fi

# Also create SQL version (easier to inspect/edit if needed)
echo ""
echo "Creating SQL dump (text format)..."
docker exec nextgent_db pg_dump -U postgres -d nextgent > "$SQL_BACKUP_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "✅ SQL dump created: $SQL_BACKUP_FILE"
else
    echo "⚠️  Warning: Failed to create SQL dump (not critical)"
fi

# Get file sizes
DUMP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
SQL_SIZE=$(du -h "$SQL_BACKUP_FILE" 2>/dev/null | cut -f1)

echo ""
echo "================================================"
echo "✅ Database Export Completed Successfully!"
echo "================================================"
echo ""
echo "📊 Backup Files:"
echo "   Binary dump: $BACKUP_FILE ($DUMP_SIZE)"
if [ -f "$SQL_BACKUP_FILE" ]; then
    echo "   SQL dump:    $SQL_BACKUP_FILE ($SQL_SIZE)"
fi
echo ""
echo "📝 Next Steps:"
echo "   1. Setup Vercel Postgres database"
echo "   2. Get connection string from Vercel dashboard"
echo "   3. Run import script:"
echo "      ./scripts/import-database.sh \"<vercel-postgres-url>\" \"$BACKUP_FILE\""
echo ""
echo "   Or manually restore:"
echo "      pg_restore -d \"<vercel-postgres-url>\" -v \"$BACKUP_FILE\""
echo ""
echo "⚠️  Important: Keep backup files safe!"
echo "   These backups are your safety net for rollback."
echo ""
