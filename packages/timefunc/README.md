# timefunc ⏱️

Function execution timing utilities for Python.

## Installation

```bash
pip install timefunc
```

## Usage

### Decorator

```python
from timefunc import timeit

@timeit
def slow_function():
    time.sleep(1)

slow_function()
# Output: slow_function: 1.0012s
```

### Context Manager

```python
from timefunc import Timer

with Timer("database query") as t:
    results = db.query()

print(f"Query took {t.elapsed:.2f}s")
```

### Benchmark

```python
from timefunc import benchmark

@benchmark(runs=100, warmup=5)
def function_to_test():
    # code to benchmark
    pass

function_to_test()
# Output:
# function_to_test:
#   Runs: 100
#   Mean: 1.23ms
#   Median: 1.20ms
#   Min: 1.01ms
#   Max: 2.45ms
#   Std Dev: 0.15ms
```

## Features

- ⏱️ Function timing decorator
- 📊 Benchmarking with statistics
- 🔄 Context manager support
- 📈 Warmup runs for accurate benchmarks
- 📝 Human-readable output

## API

### `@timeit`
```python
@timeit(name="custom", print_result=True)
def func(): pass
```

### `@benchmark`
```python
@benchmark(runs=10, warmup=1, name="custom")
def func(): pass
```

### `Timer`
```python
with Timer("name", print_result=False) as t:
    pass
print(t.elapsed)  # seconds as float
print(t.result)   # TimingResult object
```

## License

MIT
