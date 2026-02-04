"""
Database initialization script for testing.
Creates all tables in the test database.
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.core.config import settings
from app.models.base import Base

# Import all models to register them
from app.models.tenant import Tenant
from app.models.interaction import Interaction
from app.models.customer import Customer
from app.models.failed_webhook import FailedWebhook
from app.models.satisfaction import Satisfaction


async def init_db():
    """Initialize database tables."""
    print("Initializing database...")
    print(f"Database URL: {settings.SQLALCHEMY_DATABASE_URI}")
    
    engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)
    
    async with engine.begin() as conn:
        # Check if tables already exist
        result = await conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'customers'
            );
        """))
        tables_exist = result.scalar()
        
        if tables_exist:
            print("⚠️  Tables already exist. Skipping drop/create to preserve data.")
        else:
            # Drop all tables (clean slate)
            print("Dropping existing tables...")
            await conn.run_sync(Base.metadata.drop_all)
            
            # Create all tables
            print("Creating tables...")
            await conn.run_sync(Base.metadata.create_all)
    
    await engine.dispose()
    
    print("Database initialized successfully!")
    print("\nCreated tables:")
    for table in Base.metadata.sorted_tables:
        print(f"   - {table.name}")


if __name__ == "__main__":
    asyncio.run(init_db())
