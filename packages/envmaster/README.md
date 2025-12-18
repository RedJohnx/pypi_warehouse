# envmaster 🔐

Type-safe environment variable management for Python.

## Installation

```bash
pip install envmaster
```

## Usage

```python
from envmaster import env

# String (required)
DATABASE_URL = env.str("DATABASE_URL", required=True)

# Boolean with default
DEBUG = env.bool("DEBUG", default=False)

# Integer with default
MAX_CONNECTIONS = env.int("MAX_CONNECTIONS", default=10)

# Float
TIMEOUT = env.float("TIMEOUT", default=30.0)

# List (comma-separated)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])

# JSON
CONFIG = env.json("CONFIG", default={})
```

## Methods

| Method | Return Type | Description |
|--------|-------------|-------------|
| `env.str()` | str | String value |
| `env.int()` | int | Integer value |
| `env.float()` | float | Float value |
| `env.bool()` | bool | Boolean value |
| `env.list()` | list | List of strings |
| `env.json()` | any | Parsed JSON |

## Boolean Values

Truthy: `true`, `1`, `yes`, `on`  
Falsy: `false`, `0`, `no`, `off`

## Error Handling

```python
from envmaster import env, EnvError

try:
    secret = env.str("SECRET_KEY", required=True)
except EnvError as e:
    print(f"Configuration error: {e}")
```

## License

MIT
