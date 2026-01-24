"""
Advanced caching utilities with invalidation strategies.
"""
import json
import hashlib
from typing import Optional, Any, Callable, TypeVar
from functools import wraps
from uuid import UUID

import redis.asyncio as redis

from app.core.redis import redis_manager
from app.core.logger import get_logger

logger = get_logger(__name__)

T = TypeVar('T')


class CacheManager:
    """
    Centralized cache management with invalidation support.
    """
    
    @staticmethod
    def _generate_cache_key(prefix: str, *args, **kwargs) -> str:
        """Generate cache key from prefix and arguments."""
        key_parts = [prefix]
        key_parts.extend(str(arg) for arg in args)
        key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
        key_string = ":".join(key_parts)
        
        # Hash if too long (Redis key limit is 512MB but shorter is better)
        if len(key_string) > 250:
            key_hash = hashlib.md5(key_string.encode()).hexdigest()
            return f"{prefix}:hash:{key_hash}"
        
        return key_string
    
    @staticmethod
    async def get(key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            redis_client = await redis_manager.get_client()
            value = await redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error("cache_get_error", key=key, error=str(e))
            return None
    
    @staticmethod
    async def set(key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL."""
        try:
            redis_client = await redis_manager.get_client()
            await redis_client.setex(key, ttl, json.dumps(value, default=str))
            return True
        except Exception as e:
            logger.error("cache_set_error", key=key, error=str(e))
            return False
    
    @staticmethod
    async def delete(key: str) -> bool:
        """Delete key from cache."""
        try:
            redis_client = await redis_manager.get_client()
            await redis_client.delete(key)
            return True
        except Exception as e:
            logger.error("cache_delete_error", key=key, error=str(e))
            return False
    
    @staticmethod
    async def invalidate_pattern(pattern: str) -> int:
        """Invalidate all keys matching pattern."""
        try:
            redis_client = await redis_manager.get_client()
            keys = []
            async for key in redis_client.scan_iter(match=pattern):
                keys.append(key)
            
            if keys:
                await redis_client.delete(*keys)
                logger.info("cache_invalidated", pattern=pattern, count=len(keys))
                return len(keys)
            return 0
        except Exception as e:
            logger.error("cache_invalidate_error", pattern=pattern, error=str(e))
            return 0
    
    @staticmethod
    async def invalidate_tenant_cache(tenant_id: UUID):
        """Invalidate all cache entries for a tenant."""
        pattern = f"*:{tenant_id}:*"
        return await CacheManager.invalidate_pattern(pattern)


def cached(prefix: str, ttl: int = 3600):
    """
    Decorator for caching function results.
    
    Usage:
        @cached("customer", ttl=3600)
        async def get_customer(tenant_id: UUID, phone: str):
            ...
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            # Generate cache key
            cache_key = CacheManager._generate_cache_key(prefix, *args, **kwargs)
            
            # Try cache first
            cached_value = await CacheManager.get(cache_key)
            if cached_value is not None:
                logger.debug("cache_hit", key=cache_key, function=func.__name__)
                return cached_value
            
            # Cache miss - call function
            logger.debug("cache_miss", key=cache_key, function=func.__name__)
            result = await func(*args, **kwargs)
            
            # Cache result
            await CacheManager.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator


# Singleton instance
cache_manager = CacheManager()


