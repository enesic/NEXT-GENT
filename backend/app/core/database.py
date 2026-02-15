from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from fastapi import HTTPException, status
from app.core.config import settings

engine = None
AsyncSessionLocal = None

if settings.SQLALCHEMY_DATABASE_URI:
    database_uri = str(settings.SQLALCHEMY_DATABASE_URI)
    connect_args = {
        "command_timeout": 60,
        # Required for PgBouncer transaction/statement mode (e.g. Supabase pooler).
        # Prevents "prepared statement ... already exists" errors.
        "statement_cache_size": 0,
        "server_settings": {
            "application_name": "nextgent_api"
        }
    }

    # Supabase PostgreSQL requires SSL.
    if "supabase.co" in database_uri:
        connect_args["ssl"] = "require"

    uses_pgbouncer_pooler = ("pooler.supabase.com" in database_uri) or (":6543/" in database_uri)

    if uses_pgbouncer_pooler:
        # With external PgBouncer poolers, disable SQLAlchemy connection pooling
        # to avoid queue starvation and stale pooled connections.
        engine = create_async_engine(
            database_uri,
            echo=settings.DEBUG,
            future=True,
            pool_pre_ping=True,
            poolclass=NullPool,
            connect_args=connect_args,
        )
    else:
        # Default pooled configuration for direct DB connections.
        engine = create_async_engine(
            database_uri,
            echo=settings.DEBUG,
            future=True,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            pool_recycle=300,
            pool_timeout=30,
            connect_args=connect_args,
        )

    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    if AsyncSessionLocal is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is not configured"
        )

    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
