#!/usr/bin/env python3
"""
Test Neon.tech database connection and migrate schema
"""
import asyncio
import os
from sqlalchemy import text
from dotenv import load_dotenv

# Load production environment
load_dotenv('.env.production')

from app.core.database import engine, AsyncSessionLocal
from app.models.base import Base
import app.models  # Import all models

async def test_connection():
    """Test database connection"""
    if not engine:
        print("ERROR: Database engine not configured")
        return False
    
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"SUCCESS: Connected to: {version}")
            return True
    except Exception as e:
        print(f"ERROR: Connection failed: {e}")
        return False

async def migrate_schema():
    """Create all tables"""
    if not engine:
        print("ERROR: No database engine")
        return False
        
    try:
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            print("SUCCESS: Schema migrated successfully")
            return True
    except Exception as e:
        print(f"ERROR: Migration failed: {e}")
        return False

async def main():
    print("Testing Neon.tech connection...")
    
    # Test connection
    if not await test_connection():
        return
    
    # Migrate schema
    if not await migrate_schema():
        return
        
    print("Database setup completed!")

if __name__ == "__main__":
    asyncio.run(main())