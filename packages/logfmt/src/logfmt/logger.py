"""
Beautiful, structured console logging.
"""

import sys
from datetime import datetime
from enum import IntEnum
from typing import Any, Optional, TextIO


class LogLevel(IntEnum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"


LEVEL_COLORS = {
    LogLevel.DEBUG: Colors.DIM + Colors.CYAN,
    LogLevel.INFO: Colors.BRIGHT_GREEN,
    LogLevel.WARNING: Colors.BRIGHT_YELLOW,
    LogLevel.ERROR: Colors.BRIGHT_RED,
    LogLevel.CRITICAL: Colors.BOLD + Colors.BRIGHT_RED,
}

LEVEL_NAMES = {
    LogLevel.DEBUG: "DEBUG",
    LogLevel.INFO: "INFO",
    LogLevel.WARNING: "WARN",
    LogLevel.ERROR: "ERROR",
    LogLevel.CRITICAL: "CRIT",
}


class Logger:
    """
    Beautiful, structured console logger.
    
    Example:
        from logfmt import Logger
        
        log = Logger("myapp")
        log.info("Server started", port=8080)
        log.error("Connection failed", host="db.example.com", retry=3)
    """
    
    def __init__(
        self,
        name: str,
        level: LogLevel = LogLevel.INFO,
        colorize: bool = True,
        output: TextIO = sys.stderr,
        timestamp: bool = True,
    ):
        """
        Initialize logger.
        
        Args:
            name: Logger name (shown in output)
            level: Minimum log level
            colorize: Enable colored output
            output: Output stream (default: stderr)
            timestamp: Show timestamps
        """
        self.name = name
        self.level = level
        self.colorize = colorize and self._supports_color(output)
        self.output = output
        self.timestamp = timestamp
    
    def _supports_color(self, stream: TextIO) -> bool:
        """Check if the stream supports colors."""
        if not hasattr(stream, "isatty"):
            return False
        if not stream.isatty():
            return False
        return True
    
    def _format_value(self, value: Any) -> str:
        """Format a value for output."""
        if isinstance(value, str):
            if " " in value or "=" in value:
                return f'"{value}"'
            return value
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif value is None:
            return "null"
        else:
            return str(value)
    
    def _format_message(
        self,
        level: LogLevel,
        message: str,
        **kwargs: Any,
    ) -> str:
        """Format a log message."""
        parts = []
        
        # Timestamp
        if self.timestamp:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if self.colorize:
                parts.append(f"{Colors.DIM}{ts}{Colors.RESET}")
            else:
                parts.append(ts)
        
        # Level
        level_name = LEVEL_NAMES[level]
        if self.colorize:
            level_color = LEVEL_COLORS[level]
            parts.append(f"{level_color}{level_name:5}{Colors.RESET}")
        else:
            parts.append(f"{level_name:5}")
        
        # Logger name
        if self.colorize:
            parts.append(f"{Colors.BOLD}[{self.name}]{Colors.RESET}")
        else:
            parts.append(f"[{self.name}]")
        
        # Message
        parts.append(message)
        
        # Key-value pairs
        for key, value in kwargs.items():
            formatted_value = self._format_value(value)
            if self.colorize:
                parts.append(f"{Colors.CYAN}{key}{Colors.RESET}={formatted_value}")
            else:
                parts.append(f"{key}={formatted_value}")
        
        return " ".join(parts)
    
    def _log(self, level: LogLevel, message: str, **kwargs: Any) -> None:
        """Internal logging method."""
        if level < self.level:
            return
        
        formatted = self._format_message(level, message, **kwargs)
        print(formatted, file=self.output)
    
    def debug(self, message: str, **kwargs: Any) -> None:
        """Log a debug message."""
        self._log(LogLevel.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs: Any) -> None:
        """Log an info message."""
        self._log(LogLevel.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs: Any) -> None:
        """Log a warning message."""
        self._log(LogLevel.WARNING, message, **kwargs)
    
    def warn(self, message: str, **kwargs: Any) -> None:
        """Alias for warning."""
        self.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs: Any) -> None:
        """Log an error message."""
        self._log(LogLevel.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs: Any) -> None:
        """Log a critical message."""
        self._log(LogLevel.CRITICAL, message, **kwargs)
    
    def exception(self, message: str, exc: Optional[Exception] = None, **kwargs: Any) -> None:
        """Log an error with exception info."""
        if exc:
            kwargs["exception"] = f"{type(exc).__name__}: {exc}"
        self.error(message, **kwargs)
