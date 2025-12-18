# cachely ⚡

Simple in-memory caching with TTL support for Python.

## Installation

```bash
pip install cachely
```

## Usage

### Decorator

```python
from cachely import cache

@cache(ttl=300)  # Cache for 5 minutes
def expensive_computation(x):
    return x ** 100

@cache(ttl=60, key_prefix="user")
def get_user(user_id):
    return database.fetch_user(user_id)
```

### Manual Cache

```python
from cachely import Cache

cache = Cache()

# Set with TTL
cache.set("key", "value", ttl=300)

# Get value
value = cache.get("key", default=None)

# Delete
cache.delete("key")

# Clear all
cache.clear()
```

## Features

- 🕐 TTL (time-to-live) support
- 🔒 Thread-safe operations
- 🎯 Function decorator
- 🧹 Automatic cleanup of expired entries
- 📊 Cache info and stats

## API

### Decorator Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ttl` | int | None | Seconds until expiration |
| `key_prefix` | str | None | Prefix for cache keys |

### Cache Methods

| Method | Description |
|--------|-------------|
| `get(key, default)` | Get cached value |
| `set(key, value, ttl)` | Set cached value |
| `delete(key)` | Delete cached value |
| `clear()` | Clear all cache |
| `cleanup()` | Remove expired entries |
| `size()` | Number of cached items |

## License

MIT
