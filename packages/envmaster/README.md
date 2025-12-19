# envmaster 🔐

Type-safe environment variable management for Python with `.env` file support.

## Installation

```bash
pip install envmaster
```

## Usage

### Load from .env file

```python
from envmaster import env

# Load .env file automatically
env.load_dotenv()  # Loads .env from current directory

# Or specify a path
env.load_dotenv(".env.production")

# Override existing environment variables
env.load_dotenv(override=True)
```

### Access environment variables

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

## .env File Format

```bash
# Database configuration
DATABASE_URL=postgresql://localhost/mydb
DB_PORT=5432

# App settings
DEBUG=true
MAX_CONNECTIONS=10
ALLOWED_HOSTS=localhost,example.com

# Quotes are optional
API_KEY="sk-1234567890"
APP_NAME='My Application'
```

## Methods

| Method | Return Type | Description |
|--------|-------------|-------------|
| `env.load_dotenv()` | bool | Load .env file |
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
