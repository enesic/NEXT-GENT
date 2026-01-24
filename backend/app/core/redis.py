import redis.asyncio as redis
from typing import Optional
from app.core.config import settings


class RedisConnectionManager:
    """
    Singleton Redis connection pool manager.
    Prevents memory leaks and manages connections properly.
    """
    _pool: Optional[redis.ConnectionPool] = None
    _client: Optional[redis.Redis] = None
    
    @classmethod
    async def get_pool(cls) -> redis.ConnectionPool:
        """Get or create Redis connection pool."""
        if cls._pool is None:
            cls._pool = redis.ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                max_connections=50,  # Limit connections
                decode_responses=True,
                socket_keepalive=True,
                socket_connect_timeout=5,
                retry_on_timeout=True
            )
        return cls._pool
    
    @classmethod
    async def get_client(cls) -> redis.Redis:
        """Get Redis client from pool."""
        if cls._client is None:
            pool = await cls.get_pool()
            cls._client = redis.Redis(connection_pool=pool)
        return cls._client
    
    @classmethod
    async def close(cls):
        """Close all Redis connections (call on shutdown)."""
        if cls._client:
            await cls._client.close()
            cls._client = None
        
        if cls._pool:
            await cls._pool.disconnect()
            cls._pool = None


# Singleton instance
redis_manager = RedisConnectionManager()
