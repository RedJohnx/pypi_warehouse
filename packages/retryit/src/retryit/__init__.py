"""
retryit - Smart retry decorator with exponential backoff
"""

from .retry import retry, RetryError

__version__ = "1.0.0"
__all__ = ["retry", "RetryError"]
