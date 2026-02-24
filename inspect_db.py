import asyncio
import asyncpg
import json

DATABASE_URL = "postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

async def inspect():
    conn = await asyncpg.connect(DATABASE_URL)
    
    # Get tables
    tables = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    print(f"Tables: {[t['table_name'] for t in tables]}")
    
    # Check satisfactions columns
    if any(t['table_name'] == 'satisfactions' for t in tables):
        cols = await conn.fetch("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'satisfactions'")
        print("\nColumns in 'satisfactions':")
        for c in cols:
            print(f"- {c['column_name']} ({c['data_type']}), Nullable: {c['is_nullable']}")
    
    # Check vapi_calls columns
    cols = await conn.fetch("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'vapi_calls'")
    print("\nColumns in 'vapi_calls':")
    for c in cols:
        print(f"- {c['column_name']} ({c['data_type']}), Nullable: {c['is_nullable']}")

    await conn.close()

if __name__ == "__main__":
    asyncio.run(inspect())
