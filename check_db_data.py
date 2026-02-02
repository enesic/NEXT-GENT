
import asyncio
import os
import sys
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

# Setup path to import app modules if needed, but we'll use direct SQL for independence
sys.path.append(os.path.join(os.getcwd(), 'backend'))

# Database URL (Try to use localhost since we are running this script on host)
# The docker-compose maps 5432:5432, so localhost:5432 should work for the host script
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/nextgent"

async def check_db():
    print(f"Connecting to {DATABASE_URL}...")
    try:
        engine = create_async_engine(DATABASE_URL, echo=False)
        async with engine.connect() as conn:
            # Check Customers
            print("\n--- Checking Customers ---")
            result = await conn.execute(text("SELECT id, name, customer_id, pin_hash, tenant_id FROM customers"))
            customers = result.fetchall()
            if not customers:
                print("❌ No customers found!")
            else:
                for c in customers:
                    print(f"✅ Found Customer: ID={c.customer_id}, Name={c.name}, Tenant={c.tenant_id}")
            
            # Check Tenants
            print("\n--- Checking Tenants ---")
            result = await conn.execute(text("SELECT id, name, slug FROM tenants"))
            tenants = result.fetchall()
            for t in tenants:
                print(f"Tenant: {t.name} ({t.slug})")

    except Exception as e:
        print(f"❌ Error connecting to DB: {e}")
        print("Ensure the database container is running and port 5432 is exposed.")

if __name__ == "__main__":
    try:
        asyncio.run(check_db())
    except KeyboardInterrupt:
        pass
