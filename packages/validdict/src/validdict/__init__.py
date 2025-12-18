"""
validdict - Dictionary schema validation
"""

from .validator import validate, Schema, ValidationError

__version__ = "1.0.0"
__all__ = ["validate", "Schema", "ValidationError"]
