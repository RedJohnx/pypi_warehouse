"""
cachely - Simple in-memory caching with TTL support
"""

from .cache import cache, Cache, clear_all

__version__ = "1.0.0"
__all__ = ["cache", "Cache", "clear_all"]
