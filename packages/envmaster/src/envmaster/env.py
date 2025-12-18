"""
Type-safe environment variable management.
"""

import os
from typing import Optional, List, TypeVar, Type, Any

T = TypeVar('T')


class EnvError(Exception):
    """Raised when a required environment variable is missing or invalid."""
    pass


class EnvManager:
    """
    Type-safe environment variable manager.
    
    Example:
        from envmaster import env
        
        DATABASE_URL = env.str("DATABASE_URL", required=True)
        DEBUG = env.bool("DEBUG", default=False)
        MAX_CONNECTIONS = env.int("MAX_CONNECTIONS", default=10)
    """
    
    def str(
        self,
        key: str,
        default: Optional[str] = None,
        required: bool = False,
    ) -> Optional[str]:
        """
        Get a string environment variable.
        
        Args:
            key: Environment variable name
            default: Default value if not set
            required: If True, raises EnvError when missing
        
        Returns:
            The environment variable value as string
        """
        value = os.environ.get(key)
        
        if value is None:
            if required:
                raise EnvError(f"Required environment variable '{key}' is not set")
            return default
        
        return value
    
    def int(
        self,
        key: str,
        default: Optional[int] = None,
        required: bool = False,
    ) -> Optional[int]:
        """
        Get an integer environment variable.
        
        Args:
            key: Environment variable name
            default: Default value if not set
            required: If True, raises EnvError when missing
        
        Returns:
            The environment variable value as integer
        """
        value = os.environ.get(key)
        
        if value is None:
            if required:
                raise EnvError(f"Required environment variable '{key}' is not set")
            return default
        
        try:
            return int(value)
        except ValueError:
            raise EnvError(f"Environment variable '{key}' must be an integer, got '{value}'")
    
    def float(
        self,
        key: str,
        default: Optional[float] = None,
        required: bool = False,
    ) -> Optional[float]:
        """
        Get a float environment variable.
        
        Args:
            key: Environment variable name
            default: Default value if not set
            required: If True, raises EnvError when missing
        
        Returns:
            The environment variable value as float
        """
        value = os.environ.get(key)
        
        if value is None:
            if required:
                raise EnvError(f"Required environment variable '{key}' is not set")
            return default
        
        try:
            return float(value)
        except ValueError:
            raise EnvError(f"Environment variable '{key}' must be a float, got '{value}'")
    
    def bool(
        self,
        key: str,
        default: Optional[bool] = None,
        required: bool = False,
    ) -> Optional[bool]:
        """
        Get a boolean environment variable.
        
        Truthy values: 'true', '1', 'yes', 'on' (case-insensitive)
        Falsy values: 'false', '0', 'no', 'off' (case-insensitive)
        
        Args:
            key: Environment variable name
            default: Default value if not set
            required: If True, raises EnvError when missing
        
        Returns:
            The environment variable value as boolean
        """
        value = os.environ.get(key)
        
        if value is None:
            if required:
                raise EnvError(f"Required environment variable '{key}' is not set")
            return default
        
        lower_value = value.lower()
        
        if lower_value in ('true', '1', 'yes', 'on'):
            return True
        elif lower_value in ('false', '0', 'no', 'off'):
            return False
        else:
            raise EnvError(
                f"Environment variable '{key}' must be a boolean, got '{value}'. "
                "Use 'true', 'false', '1', '0', 'yes', 'no', 'on', or 'off'"
            )
    
    def list(
        self,
        key: str,
        default: Optional[List[str]] = None,
        separator: str = ",",
        required: bool = False,
    ) -> Optional[List[str]]:
        """
        Get a list environment variable (comma-separated by default).
        
        Args:
            key: Environment variable name
            default: Default value if not set
            separator: String separator (default: comma)
            required: If True, raises EnvError when missing
        
        Returns:
            The environment variable value as list of strings
        """
        value = os.environ.get(key)
        
        if value is None:
            if required:
                raise EnvError(f"Required environment variable '{key}' is not set")
            return default
        
        if not value.strip():
            return []
        
        return [item.strip() for item in value.split(separator)]
    
    def json(
        self,
        key: str,
        default: Optional[Any] = None,
        required: bool = False,
    ) -> Optional[Any]:
        """
        Get a JSON environment variable.
        
        Args:
            key: Environment variable name
            default: Default value if not set
            required: If True, raises EnvError when missing
        
        Returns:
            The parsed JSON value
        """
        import json as json_lib
        
        value = os.environ.get(key)
        
        if value is None:
            if required:
                raise EnvError(f"Required environment variable '{key}' is not set")
            return default
        
        try:
            return json_lib.loads(value)
        except json_lib.JSONDecodeError as e:
            raise EnvError(f"Environment variable '{key}' must be valid JSON: {e}")


# Global instance for convenient access
env = EnvManager()
