"""
Smart retry decorator with exponential backoff support.
"""

import time
import functools
from typing import Callable, Tuple, Type, Optional, Any


class RetryError(Exception):
    """Raised when all retry attempts have been exhausted."""
    
    def __init__(self, message: str, last_exception: Optional[Exception] = None):
        super().__init__(message)
        self.last_exception = last_exception


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[Exception, int], None]] = None,
) -> Callable:
    """
    Decorator that retries a function on failure with exponential backoff.
    
    Args:
        max_attempts: Maximum number of attempts (default: 3)
        delay: Initial delay between retries in seconds (default: 1.0)
        backoff: Multiplier for delay after each retry (default: 2.0)
        exceptions: Tuple of exceptions to catch and retry (default: all)
        on_retry: Optional callback function called on each retry with (exception, attempt_number)
    
    Returns:
        Decorated function with retry logic
    
    Example:
        @retry(max_attempts=3, delay=1, backoff=2)
        def fetch_data():
            return requests.get("https://api.example.com/data")
        
        @retry(max_attempts=5, exceptions=(ConnectionError, TimeoutError))
        def connect_to_db():
            return database.connect()
    """
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts:
                        raise RetryError(
                            f"Failed after {max_attempts} attempts: {str(e)}",
                            last_exception=e
                        ) from e
                    
                    if on_retry:
                        on_retry(e, attempt)
                    
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            # This should never be reached, but just in case
            raise RetryError(
                f"Failed after {max_attempts} attempts",
                last_exception=last_exception
            )
        
        return wrapper
    
    return decorator


def retry_async(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[Exception, int], None]] = None,
) -> Callable:
    """
    Async version of retry decorator.
    
    Example:
        @retry_async(max_attempts=3, delay=1)
        async def fetch_data():
            async with aiohttp.ClientSession() as session:
                return await session.get("https://api.example.com/data")
    """
    import asyncio
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts:
                        raise RetryError(
                            f"Failed after {max_attempts} attempts: {str(e)}",
                            last_exception=e
                        ) from e
                    
                    if on_retry:
                        on_retry(e, attempt)
                    
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
            
            raise RetryError(
                f"Failed after {max_attempts} attempts",
                last_exception=last_exception
            )
        
        return wrapper
    
    return decorator
