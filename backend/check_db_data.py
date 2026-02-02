
import asyncio
import os
import sys
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

# Database URL for Docker
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/nextgent")

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
                    print(f"✅ Found: ID={c.customer_id}, Name={c.name}")
            
            # Check Tenants
            print("\n--- Checking Tenants ---")
            result = await conn.execute(text("SELECT id, name, slug FROM tenants"))
            tenants = result.fetchall()
            if not tenants:
                print("❌ No tenants found!")
            else:
                for t in tenants:
                    print(f"Tenant: {t.name} ({t.slug})")

    except Exception as e:
        print(f"❌ Error connecting to DB: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(check_db())
    except KeyboardInterrupt:
        pass
