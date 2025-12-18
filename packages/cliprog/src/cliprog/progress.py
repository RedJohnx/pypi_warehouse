"""
Lightweight CLI progress bars.
"""

import sys
import time
from typing import Iterator, TypeVar, Optional, Iterable

T = TypeVar('T')


class ProgressBar:
    """
    A simple, customizable progress bar for CLI applications.
    
    Example:
        bar = ProgressBar(total=100, desc="Processing")
        for i in range(100):
            # do work
            bar.update(1)
        bar.close()
    """
    
    def __init__(
        self,
        total: int,
        desc: str = "",
        width: int = 40,
        fill: str = "█",
        empty: str = "░",
        show_percent: bool = True,
        show_count: bool = True,
        show_eta: bool = True,
    ):
        """
        Initialize progress bar.
        
        Args:
            total: Total number of items
            desc: Description text
            width: Width of the bar in characters
            fill: Character for filled portion
            empty: Character for empty portion
            show_percent: Show percentage
            show_count: Show count (current/total)
            show_eta: Show estimated time remaining
        """
        self.total = total
        self.desc = desc
        self.width = width
        self.fill = fill
        self.empty = empty
        self.show_percent = show_percent
        self.show_count = show_count
        self.show_eta = show_eta
        
        self.current = 0
        self.start_time = time.time()
        self._last_render = 0
    
    def update(self, n: int = 1) -> None:
        """Update progress by n steps."""
        self.current = min(self.current + n, self.total)
        self._render()
    
    def set(self, n: int) -> None:
        """Set progress to specific value."""
        self.current = min(n, self.total)
        self._render()
    
    def _format_time(self, seconds: float) -> str:
        """Format seconds as human-readable time."""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"
    
    def _render(self) -> None:
        """Render the progress bar."""
        # Throttle rendering to avoid flicker
        now = time.time()
        if now - self._last_render < 0.05 and self.current < self.total:
            return
        self._last_render = now
        
        # Calculate progress
        progress = self.current / self.total if self.total > 0 else 0
        filled_width = int(self.width * progress)
        
        # Build bar
        bar = self.fill * filled_width + self.empty * (self.width - filled_width)
        
        # Build info parts
        parts = []
        
        if self.desc:
            parts.append(self.desc)
        
        parts.append(f"[{bar}]")
        
        if self.show_percent:
            parts.append(f"{progress * 100:5.1f}%")
        
        if self.show_count:
            parts.append(f"{self.current}/{self.total}")
        
        if self.show_eta and self.current > 0:
            elapsed = now - self.start_time
            rate = self.current / elapsed
            remaining = (self.total - self.current) / rate if rate > 0 else 0
            parts.append(f"ETA: {self._format_time(remaining)}")
        
        # Print with carriage return
        line = " ".join(parts)
        sys.stdout.write(f"\r{line}")
        sys.stdout.flush()
    
    def close(self) -> None:
        """Complete the progress bar."""
        self.current = self.total
        self._render()
        print()  # New line


def progress(
    iterable: Iterable[T],
    total: Optional[int] = None,
    desc: str = "",
    **kwargs
) -> Iterator[T]:
    """
    Wrap an iterable with a progress bar.
    
    Example:
        from cliprog import progress
        
        for item in progress(items, desc="Processing"):
            process(item)
        
        # With list/range
        for i in progress(range(100)):
            do_work(i)
    """
    if total is None:
        try:
            total = len(iterable)  # type: ignore
        except TypeError:
            total = 0
    
    bar = ProgressBar(total=total, desc=desc, **kwargs)
    
    for item in iterable:
        yield item
        bar.update(1)
    
    bar.close()


class Spinner:
    """Simple CLI spinner for indeterminate progress."""
    
    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    def __init__(self, message: str = "Loading"):
        self.message = message
        self.frame = 0
        self.running = False
    
    def _render(self) -> None:
        """Render current frame."""
        frame_char = self.FRAMES[self.frame % len(self.FRAMES)]
        sys.stdout.write(f"\r{frame_char} {self.message}")
        sys.stdout.flush()
        self.frame += 1
    
    def update(self, message: Optional[str] = None) -> None:
        """Update spinner with optional new message."""
        if message:
            self.message = message
        self._render()
    
    def done(self, message: str = "Done") -> None:
        """Complete the spinner."""
        sys.stdout.write(f"\r✓ {message}\n")
        sys.stdout.flush()
    
    def fail(self, message: str = "Failed") -> None:
        """Mark spinner as failed."""
        sys.stdout.write(f"\r✗ {message}\n")
        sys.stdout.flush()


def spinner(message: str = "Loading") -> Spinner:
    """Create a new spinner instance."""
    return Spinner(message)
