"""
Database transaction management with retry and error handling.
"""
from typing import Callable, TypeVar, Optional
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import OperationalError, IntegrityError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from app.core.logger import get_logger

logger = get_logger(__name__)

T = TypeVar('T')


def with_transaction(
    retries: int = 3,
    retry_on: tuple = (OperationalError, IntegrityError)
):
    """
    Decorator for database operations with automatic retry and transaction management.
    
    Usage:
        @with_transaction(retries=3)
        async def create_customer(db: AsyncSession, ...):
            ...
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @retry(
            stop=stop_after_attempt(retries),
            wait=wait_exponential(multiplier=1, min=1, max=4),
            retry=retry_if_exception_type(retry_on),
            reraise=True
        )
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            # Find db session in args or kwargs
            db: Optional[AsyncSession] = None
            
            for arg in args:
                if isinstance(arg, AsyncSession):
                    db = arg
                    break
            
            if not db:
                db = kwargs.get('db')
            
            if not db:
                raise ValueError("Database session not found in function arguments")
            
            try:
                result = await func(*args, **kwargs)
                await db.commit()
                return result
            except Exception as e:
                await db.rollback()
                logger.error(
                    "transaction_error",
                    function=func.__name__,
                    error=str(e),
                    error_type=type(e).__name__
                )
                raise
        
        return wrapper
    return decorator



