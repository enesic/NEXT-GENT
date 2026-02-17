"""
Metrics collection for observability and monitoring.
"""
import time
from typing import Dict, Any, Optional
from datetime import datetime
from uuid import UUID

import redis.asyncio as redis

from app.core.redis import redis_manager
from app.core.logger import get_logger

logger = get_logger(__name__)


class MetricsCollector:
    """
    Collects and stores application metrics in Redis.
    """
    
    @staticmethod
    async def increment_counter(
        name: str,
        value: int = 1,
        tags: Optional[Dict[str, str]] = None
    ):
        """Increment a counter metric."""
        try:
            redis_client = await redis_manager.get_client()
            key = MetricsCollector._build_key("counter", name, tags)
            await redis_client.incrby(key, value)
            await redis_client.expire(key, 86400)  # 24 hours
        except Exception as e:
            logger.error("metrics_error", operation="increment_counter", error=str(e))
    
    @staticmethod
    async def record_timing(
        name: str,
        duration_ms: float,
        tags: Optional[Dict[str, str]] = None
    ):
        """Record a timing metric."""
        try:
            redis_client = await redis_manager.get_client()
            key = MetricsCollector._build_key("timing", name, tags)
            
            # Store timing with timestamp
            data = {
                "value": duration_ms,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Use sorted set for timing metrics (allows percentile calculations)
            await redis_client.zadd(key, {str(data["timestamp"]): duration_ms})
            await redis_client.expire(key, 86400)  # 24 hours
            
            # Also track average
            avg_key = f"{key}:avg"
            await redis_client.incrbyfloat(avg_key, duration_ms)
            await redis_client.expire(avg_key, 86400)
            
        except Exception as e:
            logger.error("metrics_error", operation="record_timing", error=str(e))
    
    @staticmethod
    async def set_gauge(
        name: str,
        value: float,
        tags: Optional[Dict[str, str]] = None
    ):
        """Set a gauge metric."""
        try:
            redis_client = await redis_manager.get_client()
            key = MetricsCollector._build_key("gauge", name, tags)
            await redis_client.setex(key, 86400, str(value))
        except Exception as e:
            logger.error("metrics_error", operation="set_gauge", error=str(e))
    
    @staticmethod
    def _build_key(metric_type: str, name: str, tags: Optional[Dict[str, str]]) -> str:
        """Build Redis key for metric."""
        key_parts = ["metrics", metric_type, name]
        if tags:
            tag_str = ":".join(f"{k}={v}" for k, v in sorted(tags.items()))
            key_parts.append(tag_str)
        return ":".join(key_parts)
    
    @staticmethod
    async def get_metrics_summary(tenant_id: Optional[UUID] = None) -> Dict[str, Any]:
        """Get summary of metrics."""
        try:
            redis_client = await redis_manager.get_client()
            pattern = "metrics:*"
            if tenant_id:
                pattern = f"metrics:*:tenant_id={tenant_id}:*"
            
            metrics = {}
            async for key in redis_client.scan_iter(match=pattern):
                key_parts = key.split(":")
                if len(key_parts) >= 3:
                    metric_type = key_parts[1]
                    metric_name = key_parts[2]
                    
                    if metric_type == "counter":
                        value = await redis_client.get(key)
                        metrics[f"{metric_name}_count"] = int(value) if value else 0
                    elif metric_type == "gauge":
                        value = await redis_client.get(key)
                        metrics[f"{metric_name}_gauge"] = float(value) if value else 0
            
            return metrics
        except Exception as e:
            logger.error("metrics_error", operation="get_summary", error=str(e))
            return {}


# Singleton instance
metrics = MetricsCollector()




