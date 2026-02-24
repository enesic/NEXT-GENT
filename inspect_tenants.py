import asyncio
import asyncpg
import json

DATABASE_URL = "postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

async def inspect():
    conn = await asyncpg.connect(DATABASE_URL)
    
    print("--- TENANTS ---")
    tenants = await conn.fetch("SELECT id, name, slug FROM tenants")
    for t in tenants:
        print(f"ID: {t['id']}, Name: {t['name']}, Slug: {t['slug']}")
    
    print("\n--- CUSTOMERS (First 5) ---")
    customers = await conn.fetch("SELECT first_name, last_name, tenant_id FROM customers LIMIT 5")
    for c in customers:
        print(f"Name: {c['first_name']} {c['last_name']}, Tenant ID: {c['tenant_id']}")

    await conn.close()

if __name__ == "__main__":
    asyncio.run(inspect())
