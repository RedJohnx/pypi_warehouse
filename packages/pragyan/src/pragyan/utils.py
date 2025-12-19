"""
Utility functions for Pragyan
"""

import os
import re
from pathlib import Path
from typing import Optional


def get_downloads_dir() -> Path:
    """Get the user's Downloads directory"""
    # Try common locations
    downloads = Path.home() / "Downloads"
    if downloads.exists():
        return downloads
    
    # Windows specific
    if os.name == 'nt':
        import winreg
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
            ) as key:
                downloads = Path(winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0])
                if downloads.exists():
                    return downloads
        except:
            pass
    
    # Fallback to home directory
    return Path.home()


def sanitize_filename(name: str, max_length: int = 100) -> str:
    """
    Sanitize a string to be used as a filename
    
    Args:
        name: The string to sanitize
        max_length: Maximum length of the result
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Replace spaces with underscores
    name = re.sub(r'\s+', '_', name)
    # Remove leading/trailing underscores
    name = name.strip('_')
    # Truncate if necessary
    if len(name) > max_length:
        name = name[:max_length]
    return name or "untitled"


def is_valid_url(url: str) -> bool:
    """Check if a string is a valid URL"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    return bool(url_pattern.match(url))


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def wrap_text(text: str, width: int) -> str:
    """
    Wrap text to a specified width
    
    Args:
        text: Text to wrap
        width: Maximum line width
        
    Returns:
        Wrapped text
    """
    import textwrap
    return "\n".join(textwrap.wrap(text, width))


def extract_code_from_response(response: str, language: Optional[str] = None) -> str:
    """
    Extract code from an LLM response that may contain markdown code blocks
    
    Args:
        response: The LLM response
        language: Expected programming language
        
    Returns:
        Extracted code
    """
    # Try to find code block
    patterns = [
        rf'```{language}\n(.*?)```' if language else None,
        r'```\w+\n(.*?)```',
        r'```\n(.*?)```',
        r'```(.*?)```',
    ]
    
    for pattern in patterns:
        if pattern:
            match = re.search(pattern, response, re.DOTALL)
            if match:
                return match.group(1).strip()
    
    # No code block found, return as-is
    return response.strip()


def format_complexity(complexity: str) -> str:
    """
    Format complexity notation consistently
    
    Args:
        complexity: Complexity string (e.g., "O(n)", "O(n^2)", etc.)
        
    Returns:
        Formatted complexity string
    """
    # Ensure O() notation
    complexity = complexity.strip()
    if not complexity.startswith("O("):
        if complexity.startswith("("):
            complexity = "O" + complexity
        else:
            complexity = f"O({complexity})"
    
    # Clean up common variations
    complexity = complexity.replace("**", "^")
    complexity = complexity.replace("×", "*")
    complexity = complexity.replace("·", "*")
    
    return complexity


class ProgressTracker:
    """Simple progress tracker for CLI"""
    
    def __init__(self, total_steps: int = 0):
        self.total_steps = total_steps
        self.current_step = 0
        self.messages = []
    
    def update(self, message: str):
        """Update progress with a message"""
        self.current_step += 1
        self.messages.append(message)
        print(f"[{self.current_step}/{self.total_steps}] {message}")
    
    def complete(self):
        """Mark as complete"""
        print("✓ Complete!")


def ensure_dependencies():
    """Check and report on optional dependencies"""
    dependencies = {
        "manim": "Video generation with Manim animations",
        "moviepy": "Simple video generation",
        "selenium": "Web scraping for dynamic pages",
        "langchain_community": "LangChain web scraping",
    }
    
    available = {}
    missing = {}
    
    for dep, desc in dependencies.items():
        try:
            __import__(dep)
            available[dep] = desc
        except ImportError:
            missing[dep] = desc
    
    return available, missing
