from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# Serverless-optimized engine configuration
# Vercel functions are stateless, so we use minimal pooling
engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
    # Serverless optimization: minimal pool to avoid connection exhaustion
    pool_size=1,
    max_overflow=0,
    pool_recycle=300,  # Recycle connections after 5 minutes
    pool_timeout=30,   # Connection timeout
    connect_args={
        "command_timeout": 60,
        "server_settings": {
            "application_name": "nextgent_api"
        }
    }
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
