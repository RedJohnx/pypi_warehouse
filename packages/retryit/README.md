# retryit 🔄

Smart retry decorator with exponential backoff for Python.

## Installation

```bash
pip install retryit
```

## Usage

```python
from retryit import retry

@retry(max_attempts=3, delay=1, backoff=2)
def fetch_data():
    return requests.get("https://api.example.com/data")

# With specific exceptions
@retry(max_attempts=5, exceptions=(ConnectionError, TimeoutError))
def connect_to_db():
    return database.connect()

# With callback on retry
def log_retry(exception, attempt):
    print(f"Attempt {attempt} failed: {exception}")

@retry(max_attempts=3, on_retry=log_retry)
def unreliable_function():
    # ...
```

### Async Support

```python
from retryit import retry_async

@retry_async(max_attempts=3, delay=1)
async def fetch_data():
    async with aiohttp.ClientSession() as session:
        return await session.get("https://api.example.com/data")
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_attempts` | int | 3 | Maximum retry attempts |
| `delay` | float | 1.0 | Initial delay (seconds) |
| `backoff` | float | 2.0 | Delay multiplier |
| `exceptions` | tuple | (Exception,) | Exceptions to catch |
| `on_retry` | callable | None | Callback on each retry |

## License

MIT
