"""
Function execution timing utilities.
"""

import time
import functools
import statistics
from typing import Callable, Any, Optional, List, Dict
from contextlib import contextmanager


class TimingResult:
    """Result of a timing operation."""
    
    def __init__(self, name: str, duration: float):
        self.name = name
        self.duration = duration
    
    def __repr__(self) -> str:
        return f"TimingResult(name='{self.name}', duration={self.duration:.4f}s)"
    
    def __str__(self) -> str:
        return f"{self.name}: {self._format_duration(self.duration)}"
    
    @staticmethod
    def _format_duration(seconds: float) -> str:
        """Format duration as human-readable string."""
        if seconds < 0.001:
            return f"{seconds * 1_000_000:.2f}μs"
        elif seconds < 1:
            return f"{seconds * 1000:.2f}ms"
        else:
            return f"{seconds:.4f}s"


class BenchmarkResult:
    """Result of a benchmark operation."""
    
    def __init__(self, name: str, times: List[float]):
        self.name = name
        self.times = times
        self.runs = len(times)
        self.total = sum(times)
        self.mean = statistics.mean(times)
        self.median = statistics.median(times)
        self.min = min(times)
        self.max = max(times)
        self.stdev = statistics.stdev(times) if len(times) > 1 else 0
    
    def __repr__(self) -> str:
        return f"BenchmarkResult(name='{self.name}', runs={self.runs}, mean={self.mean:.4f}s)"
    
    def __str__(self) -> str:
        return (
            f"{self.name}:\n"
            f"  Runs: {self.runs}\n"
            f"  Mean: {self._format(self.mean)}\n"
            f"  Median: {self._format(self.median)}\n"
            f"  Min: {self._format(self.min)}\n"
            f"  Max: {self._format(self.max)}\n"
            f"  Std Dev: {self._format(self.stdev)}"
        )
    
    @staticmethod
    def _format(seconds: float) -> str:
        if seconds < 0.001:
            return f"{seconds * 1_000_000:.2f}μs"
        elif seconds < 1:
            return f"{seconds * 1000:.2f}ms"
        else:
            return f"{seconds:.4f}s"


class Timer:
    """
    Context manager for timing code blocks.
    
    Example:
        with Timer("database query") as t:
            results = db.query()
        print(t.result)
    """
    
    def __init__(self, name: str = "block", print_result: bool = False):
        self.name = name
        self.print_result = print_result
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.result: Optional[TimingResult] = None
    
    def __enter__(self) -> "Timer":
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, *args) -> None:
        self.end_time = time.perf_counter()
        duration = self.end_time - self.start_time
        self.result = TimingResult(self.name, duration)
        
        if self.print_result:
            print(self.result)
    
    @property
    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        elif self.start_time:
            return time.perf_counter() - self.start_time
        return 0.0


def timeit(
    func: Optional[Callable] = None,
    name: Optional[str] = None,
    print_result: bool = True,
) -> Callable:
    """
    Decorator to time function execution.
    
    Example:
        @timeit
        def slow_function():
            time.sleep(1)
        
        @timeit(name="custom name", print_result=False)
        def another_function():
            pass
    """
    
    def decorator(fn: Callable) -> Callable:
        fn_name = name or fn.__name__
        
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            try:
                return fn(*args, **kwargs)
            finally:
                duration = time.perf_counter() - start
                result = TimingResult(fn_name, duration)
                
                # Attach result to function for later access
                wrapper.last_result = result
                
                if print_result:
                    print(result)
        
        wrapper.last_result = None
        return wrapper
    
    if func is not None:
        return decorator(func)
    
    return decorator


def benchmark(
    func: Optional[Callable] = None,
    runs: int = 10,
    warmup: int = 1,
    name: Optional[str] = None,
) -> Callable:
    """
    Decorator to benchmark function execution over multiple runs.
    
    Example:
        @benchmark(runs=100, warmup=5)
        def function_to_benchmark():
            pass
    """
    
    def decorator(fn: Callable) -> Callable:
        fn_name = name or fn.__name__
        
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> BenchmarkResult:
            # Warmup runs
            for _ in range(warmup):
                fn(*args, **kwargs)
            
            # Timed runs
            times = []
            for _ in range(runs):
                start = time.perf_counter()
                fn(*args, **kwargs)
                times.append(time.perf_counter() - start)
            
            result = BenchmarkResult(fn_name, times)
            print(result)
            return result
        
        return wrapper
    
    if func is not None:
        return decorator(func)
    
    return decorator


@contextmanager
def timed(name: str = "block"):
    """
    Context manager for timing code blocks (functional style).
    
    Example:
        with timed("heavy computation"):
            result = compute()
    """
    timer = Timer(name, print_result=True)
    with timer:
        yield timer
