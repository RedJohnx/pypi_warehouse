# PyPI Warehouse 

A collection of lightweight, focused Python utility packages that solve real-world development problems.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

##  Featured Package

###  Pragyan - AI-Powered DSA Solver

```bash
pip install pragyan
```

Pragyan is an AI-powered DSA (Data Structures & Algorithms) problem solver that generates solutions with animated video explanations using Manim.

**Features:**
-  Scrape problems from LeetCode, GeeksforGeeks, Codeforces, HackerRank
-  AI-powered solution generation (Gemini/Groq)
-  Animated video explanations with visual data structures
-  11+ programming languages supported
-  Algorithm visualizations (two-pointer, sliding window, binary search, etc.)

[![PyPI](https://img.shields.io/pypi/v/pragyan)](https://pypi.org/project/pragyan/)

---

##  All Packages

| Package | Description | Install | PyPI Link |
|---------|-------------|---------|-----------|
| [**pragyan**](./packages/pragyan) | AI-powered DSA solver with video explanations | `pip install pragyan` | [pypi.org/project/pragyan](https://pypi.org/project/pragyan/) |
| [**envmaster**](./packages/envmaster) | Type-safe environment variable management | `pip install envmaster` | [pypi.org/project/envmaster](https://pypi.org/project/envmaster/) |
| [**pylogfmt-rj**](./packages/pylogfmt-rj) | Beautiful, structured console logging | `pip install pylogfmt-rj` | [pypi.org/project/pylogfmt-rj](https://pypi.org/project/pylogfmt-rj/) |
| [**pycachely-rj**](./packages/pycachely-rj) | Simple in-memory caching with TTL support | `pip install pycachely-rj` | [pypi.org/project/pycachely-rj](https://pypi.org/project/pycachely-rj/) |
| [**pyretryit-rj**](./packages/pyretryit-rj) | Smart retry decorator with exponential backoff | `pip install pyretryit-rj` | [pypi.org/project/pyretryit-rj](https://pypi.org/project/pyretryit-rj/) |
| [**pyvaliddict-rj**](./packages/pyvaliddict-rj) | Dictionary schema validation | `pip install pyvaliddict-rj` | [pypi.org/project/pyvaliddict-rj](https://pypi.org/project/pyvaliddict-rj/) |
| [**pytimefunc-rj**](./packages/pytimefunc-rj) | Function execution timing utilities | `pip install pytimefunc-rj` | [pypi.org/project/pytimefunc-rj](https://pypi.org/project/pytimefunc-rj/) |
| [**pycliprog-rj**](./packages/pycliprog-rj) | Lightweight CLI progress bars | `pip install pycliprog-rj` | [pypi.org/project/pycliprog-rj](https://pypi.org/project/pycliprog-rj/) |
| [**pyprojectcheck-rj**](./packages/pyprojectcheck-rj) | Validate pyproject.toml files | `pip install pyprojectcheck-rj` | [pypi.org/project/pyprojectcheck-rj](https://pypi.org/project/pyprojectcheck-rj/) |

---

##  PyPI Links

**Direct Install All:**
```bash
pip install pragyan envmaster pylogfmt-rj pycachely-rj pyretryit-rj pyvaliddict-rj pytimefunc-rj pycliprog-rj pyprojectcheck-rj
```

**Individual Package Links:**
-  **pragyan**: https://pypi.org/project/pragyan/
-  **envmaster**: https://pypi.org/project/envmaster/
-  **pylogfmt-rj**: https://pypi.org/project/pylogfmt-rj/
-  **pycachely-rj**: https://pypi.org/project/pycachely-rj/
-  **pyretryit-rj**: https://pypi.org/project/pyretryit-rj/
-  **pyvaliddict-rj**: https://pypi.org/project/pyvaliddict-rj/
-  **pytimefunc-rj**: https://pypi.org/project/pytimefunc-rj/
-  **pycliprog-rj**: https://pypi.org/project/pycliprog-rj/
-  **pyprojectcheck-rj**: https://pypi.org/project/pyprojectcheck-rj/

---

##  Quick Start

### Pragyan - Solve DSA Problems with AI
```python
from pragyan import Pragyan

solver = Pragyan(api_key="your-gemini-api-key")
result = solver.solve("https://leetcode.com/problems/two-sum/", language="python")
print(result.solution.code)
```

Or from terminal:
```bash
pragyan interactive
```

### pyretryit-rj - Smart Retries
```python
from retryit import retry

@retry(max_attempts=3, delay=1, backoff=2)
def fetch_data():
    return requests.get("https://api.example.com/data")
```

### envmaster - Environment Variables Made Easy
```python
from envmaster import env

DATABASE_URL = env.str("DATABASE_URL", required=True)
DEBUG = env.bool("DEBUG", default=False)
MAX_CONNECTIONS = env.int("MAX_CONNECTIONS", default=10)
```

### pycachely-rj - Simple Caching
```python
from cachely import cache

@cache(ttl=300)  # Cache for 5 minutes
def expensive_computation(x):
    return x ** 100
```

### pylogfmt-rj - Pretty Logging
```python
from logfmt import Logger

log = Logger("myapp")
log.info("Server started", port=8080)
log.error("Connection failed", host="db.example.com")
```

---

##  Development

```bash
# Clone the repository
git clone https://github.com/Kamalllx/pypi_warehouse.git
cd pypi_warehouse

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

---

##  Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

##  License

MIT License - see [LICENSE](./LICENSE) for details.
