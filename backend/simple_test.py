#!/usr/bin/env python3
"""
Simple database connection test
"""
import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv('.env.production')

async def test_direct():
    try:
        conn_str = os.getenv('DATABASE_URL')
        print(f"Testing connection: {conn_str[:50]}...")
        
        conn = await asyncpg.connect(conn_str)
        version = await conn.fetchval('SELECT version()')
        print(f"SUCCESS: {version}")
        await conn.close()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_direct())