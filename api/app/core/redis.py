import redis.asyncio as redis
from typing import Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class RedisConnectionManager:
    """
    Singleton Redis connection pool manager with optional Redis support.
    If Redis is not configured or unavailable, operations gracefully degrade.
    """
    _pool: Optional[redis.ConnectionPool] = None
    _client: Optional[redis.Redis] = None
    _redis_available: bool = True
    _connection_attempted: bool = False
    
    @classmethod
    async def get_pool(cls) -> Optional[redis.ConnectionPool]:
        """Get or create Redis connection pool. Returns None if Redis unavailable."""
        if not cls._connection_attempted:
            cls._connection_attempted = True
            
            # Check if Redis is configured
            if not hasattr(settings, 'REDIS_HOST') or not settings.REDIS_HOST:
                logger.warning("⚠️ Redis not configured - running without cache")
                cls._redis_available = False
                return None
            
            try:
                cls._pool = redis.ConnectionPool(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    max_connections=10,  # Reduced for serverless
                    decode_responses=True,
                    socket_keepalive=True,
                    socket_connect_timeout=5,
                    retry_on_timeout=False
                )
                logger.info("✅ Redis connection pool initialized")
            except Exception as e:
                logger.warning(f"⚠️ Redis connection failed: {e} - running without cache")
                cls._redis_available = False
                return None
                
        return cls._pool
    
    @classmethod
    async def get_client(cls) -> Optional[redis.Redis]:
        """Get Redis client from pool. Returns None if Redis unavailable."""
        if not cls._redis_available:
            return None
            
        if cls._client is None:
            pool = await cls.get_pool()
            if pool is None:
                return None
                
            try:
                cls._client = redis.Redis(connection_pool=pool)
                # Test connection
                await cls._client.ping()
            except Exception as e:
                logger.warning(f"⚠️ Redis ping failed: {e} - running without cache")
                cls._redis_available = False
                cls._client = None
                return None
                
        return cls._client
    
    @classmethod
    async def close(cls):
        """Close all Redis connections (call on shutdown)."""
        if cls._client:
            try:
                await cls._client.close()
            except Exception as e:
                logger.warning(f"Error closing Redis client: {e}")
            cls._client = None
        
        if cls._pool:
            try:
                await cls._pool.disconnect()
            except Exception as e:
                logger.warning(f"Error disconnecting Redis pool: {e}")
            cls._pool = None


# Singleton instance
redis_manager = RedisConnectionManager()
