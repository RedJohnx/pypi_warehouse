"""
Simple in-memory caching with TTL support.
"""

import time
import functools
import hashlib
import json
from typing import Callable, Any, Optional, Dict
from threading import Lock


class CacheEntry:
    """Represents a cached value with expiration."""
    
    def __init__(self, value: Any, expires_at: Optional[float] = None):
        self.value = value
        self.expires_at = expires_at
    
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at


class Cache:
    """
    Thread-safe in-memory cache with TTL support.
    
    Example:
        cache = Cache()
        cache.set("key", "value", ttl=300)
        value = cache.get("key")
    """
    
    def __init__(self):
        self._store: Dict[str, CacheEntry] = {}
        self._lock = Lock()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from cache."""
        with self._lock:
            entry = self._store.get(key)
            
            if entry is None:
                return default
            
            if entry.is_expired():
                del self._store[key]
                return default
            
            return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set a value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (None = never expires)
        """
        expires_at = None
        if ttl is not None:
            expires_at = time.time() + ttl
        
        with self._lock:
            self._store[key] = CacheEntry(value, expires_at)
    
    def delete(self, key: str) -> bool:
        """Delete a key from cache. Returns True if key existed."""
        with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False
    
    def clear(self) -> None:
        """Clear all cached values."""
        with self._lock:
            self._store.clear()
    
    def cleanup(self) -> int:
        """Remove expired entries. Returns number of entries removed."""
        removed = 0
        with self._lock:
            expired_keys = [
                key for key, entry in self._store.items()
                if entry.is_expired()
            ]
            for key in expired_keys:
                del self._store[key]
                removed += 1
        return removed
    
    def size(self) -> int:
        """Return number of items in cache."""
        with self._lock:
            return len(self._store)


# Global cache instance
_global_cache = Cache()


def _make_key(func: Callable, args: tuple, kwargs: dict) -> str:
    """Generate a cache key from function and arguments."""
    key_parts = [func.__module__, func.__qualname__]
    
    # Serialize arguments
    try:
        args_str = json.dumps(args, sort_keys=True, default=str)
        kwargs_str = json.dumps(kwargs, sort_keys=True, default=str)
    except (TypeError, ValueError):
        args_str = str(args)
        kwargs_str = str(kwargs)
    
    key_parts.extend([args_str, kwargs_str])
    key_string = ":".join(key_parts)
    
    return hashlib.md5(key_string.encode()).hexdigest()


def cache(
    ttl: Optional[int] = None,
    key_prefix: Optional[str] = None,
) -> Callable:
    """
    Decorator that caches function results.
    
    Args:
        ttl: Time-to-live in seconds (None = never expires)
        key_prefix: Optional prefix for cache keys
    
    Example:
        @cache(ttl=300)  # Cache for 5 minutes
        def expensive_computation(x):
            return x ** 100
        
        @cache(ttl=60, key_prefix="user")
        def get_user(user_id):
            return database.fetch_user(user_id)
    """
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Generate cache key
            key = _make_key(func, args, kwargs)
            if key_prefix:
                key = f"{key_prefix}:{key}"
            
            # Try to get from cache
            cached_value = _global_cache.get(key)
            if cached_value is not None:
                return cached_value
            
            # Compute and cache result
            result = func(*args, **kwargs)
            _global_cache.set(key, result, ttl)
            
            return result
        
        # Attach cache control methods
        wrapper.cache_clear = lambda: _global_cache.clear()
        wrapper.cache_info = lambda: {"size": _global_cache.size()}
        
        return wrapper
    
    return decorator


def clear_all() -> None:
    """Clear the global cache."""
    _global_cache.clear()
