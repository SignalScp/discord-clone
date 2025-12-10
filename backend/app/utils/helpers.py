"""Helper utility functions."""

from typing import Optional
from datetime import datetime


def format_datetime(dt: Optional[datetime], format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[str]:
    """Format datetime object to string.
    
    Args:
        dt: Datetime object
        format_str: Format string (default: YYYY-MM-DD HH:MM:SS)
        
    Returns:
        Formatted datetime string or None
    """
    if dt is None:
        return None
    return dt.strftime(format_str)


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate string to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length (default: 100)
        suffix: Suffix to add if truncated (default: ...)
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def sanitize_username(username: str) -> str:
    """Sanitize username by removing special characters.
    
    Args:
        username: Raw username
        
    Returns:
        Sanitized username
    """
    # Allow alphanumeric, underscores, and hyphens
    return ''.join(c for c in username if c.isalnum() or c in ('_', '-'))
