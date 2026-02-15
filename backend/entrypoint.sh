#!/bin/bash
set -e

echo "🚀 Starting NextGent Backend..."
echo "🌍 ENVIRONMENT=${ENVIRONMENT:-local}"

start_api() {
    echo "🎯 Starting FastAPI application..."
    exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
}

# Production path: never block startup with long init/seed loops.
# Railway edge returns 502 if app does not become healthy quickly.
if [ "${ENVIRONMENT}" = "production" ]; then
    echo "✅ Production mode detected: skipping init/seed bootstrap."
    start_api
fi

# Non-production bootstrap path (local/dev/demo)
if [ -n "${POSTGRES_SERVER}" ] && [ -n "${POSTGRES_PORT}" ] && [ -n "${POSTGRES_USER}" ]; then
    echo "⏳ Waiting for PostgreSQL (max 60s)..."
    ATTEMPTS=0
    MAX_ATTEMPTS=30
    until pg_isready -h "${POSTGRES_SERVER}" -p "${POSTGRES_PORT}" -U "${POSTGRES_USER}" > /dev/null 2>&1; do
        ATTEMPTS=$((ATTEMPTS+1))
        if [ "${ATTEMPTS}" -ge "${MAX_ATTEMPTS}" ]; then
            echo "⚠️ PostgreSQL readiness check timed out; continuing startup."
            break
        fi
        echo "   PostgreSQL is unavailable - sleeping"
        sleep 2
    done
fi

echo "🔍 Checking if database is initialized..."
TABLE_EXISTS=$(python -c "
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.core.config import settings

async def check_tables():
    engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    async with engine.connect() as conn:
        result = await conn.execute(text(\"\"\"
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'customers'
            );
        \"\"\"))
        exists = result.scalar()
        await engine.dispose()
        return exists

if __name__ == '__main__':
    result = asyncio.run(check_tables())
    print('true' if result else 'false')
" 2>/dev/null || echo "false")

if [ "${TABLE_EXISTS}" = "false" ]; then
    echo "📊 Database tables not found. Initializing..."
    python init_db.py || true
    python comprehensive_seed.py || true
else
    echo "✅ Database tables already exist. Skipping initialization."
fi

echo "👤 Checking admin user..."
python create_default_admin.py || true

start_api

