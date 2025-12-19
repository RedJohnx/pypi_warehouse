"""
envmaster - Type-safe environment variable management
"""

from .env import env, EnvError

__version__ = "1.0.0"
__all__ = ["env", "EnvError"]
