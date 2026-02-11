#!/bin/sh
# Database Initialization Script for Docker
# This script waits for database, creates tables, and seeds data

set -e

echo "🔄 Waiting for database to be ready..."
python -c "
import asyncio
import asyncpg
import time

async def wait_for_db():
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            conn = await asyncpg.connect(
                host='db',
                port=5432,
                user='postgres',
                password='postgres',
                database='nextgent',
                timeout=5
            )
            await conn.close()
            print('✅ Database is ready!')
            return True
        except Exception as e:
            retry_count += 1
            print(f'⏳ Waiting for database... ({retry_count}/{max_retries})')
            time.sleep(2)
    
    print('❌ Database connection failed after maximum retries')
    return False

asyncio.run(wait_for_db())
"

echo "🗄️  Initializing database tables..."
python init_db.py

echo "🌱 Seeding database with sample data..."
python comprehensive_seed.py

echo "✅ Database initialization complete!"
echo ""
echo "📊 Sample Login Credentials:"
echo "================================"
echo "Beauty Center:"
echo "  ID: BEA-000001"
echo "  PIN: 1234"
echo ""
echo "Hotel/Hospitality:"
echo "  ID: HOS-000001"
echo "  PIN: 1234"
echo ""
echo "Medical:"
echo "  ID: MED-000001"
echo "  PIN: 1234"
echo "================================"
