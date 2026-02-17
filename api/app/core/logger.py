import logging
import sys
from typing import Any, Dict
import json
from datetime import datetime

from app.core.pii_masker import pii_masker


class PIISafeFormatter(logging.Formatter):
    """
    Custom log formatter that automatically masks PII data.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        # Mask PII in message
        if hasattr(record, 'pii_data'):
            record.msg = pii_masker.safe_log(record.msg, **record.pii_data)
        
        return super().format(record)


class StructuredLogger:
    """
    Structured logger with automatic PII masking for KVKK/GDPR compliance.
    """
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Console handler with PII-safe formatter
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)
            
            formatter = PIISafeFormatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def info(self, message: str, **kwargs):
        """Log info with automatic PII masking."""
        masked_kwargs = self._mask_kwargs(kwargs)
        extra = {'pii_data': masked_kwargs}
        self.logger.info(message, extra=extra)
    
    def warning(self, message: str, **kwargs):
        """Log warning with automatic PII masking."""
        masked_kwargs = self._mask_kwargs(kwargs)
        extra = {'pii_data': masked_kwargs}
        self.logger.warning(message, extra=extra)
    
    def error(self, message: str, **kwargs):
        """Log error with automatic PII masking."""
        masked_kwargs = self._mask_kwargs(kwargs)
        extra = {'pii_data': masked_kwargs}
        self.logger.error(message, extra=extra)
    
    def debug(self, message: str, **kwargs):
        """Log debug with automatic PII masking."""
        masked_kwargs = self._mask_kwargs(kwargs)
        extra = {'pii_data': masked_kwargs}
        self.logger.debug(message, extra=extra)
    
    def _mask_kwargs(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Mask PII in kwargs."""
        masked = {}
        for key, value in kwargs.items():
            if 'phone' in key.lower():
                masked[key] = pii_masker.mask_phone(str(value))
            elif 'email' in key.lower():
                masked[key] = pii_masker.mask_email(str(value))
            elif 'name' in key.lower():
                masked[key] = pii_masker.mask_name(str(value))
            elif isinstance(value, dict):
                masked[key] = pii_masker.mask_dict(value)
            else:
                masked[key] = value
        return masked
    
    def log_request(self, endpoint: str, tenant_id: str, **kwargs):
        """Log API request with masked PII."""
        self.info(
            f"API Request: {endpoint}",
            tenant_id=tenant_id,
            **kwargs
        )
    
    def log_performance(self, operation: str, duration_ms: float, **kwargs):
        """Log performance metrics with masked PII."""
        status = "⚡ FAST" if duration_ms < 200 else "⚠️ SLOW"
        self.info(
            f"Performance: {operation}",
            duration_ms=duration_ms,
            status=status,
            **kwargs
        )
    
    def log_cache_hit(self, cache_type: str, key_hash: str):
        """Log cache hit (use hash instead of actual key)."""
        self.info(
            f"Cache HIT: {cache_type}",
            key_hash=key_hash
        )
    
    def log_cache_miss(self, cache_type: str, key_hash: str):
        """Log cache miss (use hash instead of actual key)."""
        self.info(
            f"Cache MISS: {cache_type}",
            key_hash=key_hash
        )


def get_logger(name: str) -> StructuredLogger:
    """Get or create structured logger."""
    return StructuredLogger(name)
