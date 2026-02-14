#!/bin/bash
set -e

echo "🚀 Starting NextGent Backend..."

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL..."
while ! pg_isready -h $POSTGRES_SERVER -p $POSTGRES_PORT -U $POSTGRES_USER > /dev/null 2>&1; do
    echo "   PostgreSQL is unavailable - sleeping"
    sleep 2
done
echo "✅ PostgreSQL is ready!"

# Wait a bit more to ensure database is fully initialized
sleep 3

# Check if tables exist
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

if [ "$TABLE_EXISTS" = "false" ]; then
    echo "📊 Database tables not found. Initializing..."
    
    # Initialize database tables
    echo "🔨 Creating database tables..."
    python init_db.py
    
    # Seed database with demo data
    echo "🌱 Seeding database with demo data..."
    python comprehensive_seed.py
    
    echo "✅ Database initialization complete!"
else
    echo "✅ Database tables already exist. Skipping initialization."
fi

# Always ensure admin user exists (even if tables already existed)
echo "👤 Checking admin user..."
python create_default_admin.py

# Start the FastAPI application
echo "🎯 Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

