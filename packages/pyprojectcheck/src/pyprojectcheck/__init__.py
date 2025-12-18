"""
pyprojectcheck - Validate pyproject.toml files
"""

from .checker import check, check_file, ValidationResult

__version__ = "1.0.0"
__all__ = ["check", "check_file", "ValidationResult"]
