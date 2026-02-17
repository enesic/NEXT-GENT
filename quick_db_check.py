import asyncio
import asyncpg

async def check():
    conn = await asyncpg.connect("postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require")
    
    # Check tenants
    tenants = await conn.fetch("SELECT slug, name FROM tenants WHERE slug != 'nextgent-main' ORDER BY slug")
    print(f"Tenants created: {len(tenants)}")
    for tenant in tenants:
        print(f"  - {tenant['slug']}: {tenant['name']}")
    
    # Check customers per sector
    total_customers = 0
    for tenant in tenants:
        customers = await conn.fetch("SELECT customer_id FROM customers WHERE tenant_id = (SELECT id FROM tenants WHERE slug = $1)", tenant['slug'])
        print(f"  {tenant['slug']}: {len(customers)} customers")
        if len(customers) > 0:
            print(f"    Sample: {customers[0]['customer_id']}")
        total_customers += len(customers)
    
    print(f"\nTotal customers: {total_customers}")
    
    # Check analytics data
    analytics_count = await conn.fetchval("SELECT COUNT(*) FROM analytics_metrics")
    print(f"Analytics records: {analytics_count}")
    
    calls_count = await conn.fetchval("SELECT COUNT(*) FROM call_interactions")  
    print(f"Call interactions: {calls_count}")
    
    await conn.close()

asyncio.run(check())