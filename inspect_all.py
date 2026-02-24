import asyncio
import asyncpg

DATABASE_URL = "postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

async def inspect():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        # 1. List all tables
        tables = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        print(f"Tables found: {[t['table_name'] for t in tables]}")
        
        # 2. For each relevant table, check count and column names
        target_tables = ['customers', 'appointments', 'interactions', 'tenants', 'vapi_calls']
        for table in target_tables:
            if any(t['table_name'] == table for t in tables):
                count = await conn.fetchval(f"SELECT COUNT(*) FROM {table}")
                cols = await conn.fetch(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
                print(f"\nTABLE: {table} (Count: {count})")
                print(f"Columns: {[c['column_name'] for c in cols]}")
            else:
                print(f"\nTABLE: {table} NOT FOUND")
        
        await conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(inspect())
