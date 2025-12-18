# PyPI Warehouse 🏭

A collection of lightweight, focused Python utility packages that solve real-world development problems.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## 📦 Packages

| Package | Description | Install |
|---------|-------------|---------|
| [**retryit**](./packages/retryit) | Smart retry decorator with exponential backoff | `pip install retryit` |
| [**envmaster**](./packages/envmaster) | Type-safe environment variable management | `pip install envmaster` |
| [**cachely**](./packages/cachely) | Simple in-memory caching with TTL support | `pip install cachely` |
| [**logfmt**](./packages/logfmt) | Beautiful, structured console logging | `pip install logfmt` |
| [**cliprog**](./packages/cliprog) | Lightweight CLI progress bars | `pip install cliprog` |
| [**validdict**](./packages/validdict) | Dictionary schema validation | `pip install validdict` |
| [**timefunc**](./packages/timefunc) | Function execution timing utilities | `pip install timefunc` |
| [**pyprojectcheck**](./packages/pyprojectcheck) | Validate pyproject.toml files | `pip install pyprojectcheck` |

## 🚀 Quick Start

```bash
# Install any package
pip install retryit envmaster cachely

# Or install all packages
pip install retryit envmaster cachely logfmt cliprog validdict timefunc pyprojectcheck
```

## 📖 Package Highlights

### retryit - Smart Retries
```python
from retryit import retry

@retry(max_attempts=3, delay=1, backoff=2)
def fetch_data():
    # Automatically retries on failure
    return requests.get("https://api.example.com/data")
```

### envmaster - Environment Variables Made Easy
```python
from envmaster import env

DATABASE_URL = env.str("DATABASE_URL", required=True)
DEBUG = env.bool("DEBUG", default=False)
MAX_CONNECTIONS = env.int("MAX_CONNECTIONS", default=10)
```

### cachely - Simple Caching
```python
from cachely import cache

@cache(ttl=300)  # Cache for 5 minutes
def expensive_computation(x):
    return x ** 100
```

### logfmt - Pretty Logging
```python
from logfmt import Logger

log = Logger("myapp")
log.info("Server started", port=8080)
log.error("Connection failed", host="db.example.com")
```

## 🛠️ Development

```bash
# Clone the repository
git clone https://github.com/RedJohnx/pypi_warehouse.git
cd pypi_warehouse

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## 🤝 Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](./LICENSE) for details.