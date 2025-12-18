# logfmt 📝

Beautiful, structured console logging for Python.

## Installation

```bash
pip install logfmt
```

## Usage

```python
from logfmt import Logger

log = Logger("myapp")

log.debug("Debugging info", variable=42)
log.info("Server started", port=8080, host="0.0.0.0")
log.warning("High memory usage", percent=85)
log.error("Connection failed", host="db.example.com", retry=3)
log.critical("System shutdown imminent")
```

### Output

```
2025-12-18 10:30:45 INFO  [myapp] Server started port=8080 host=0.0.0.0
2025-12-18 10:30:46 WARN  [myapp] High memory usage percent=85
2025-12-18 10:30:47 ERROR [myapp] Connection failed host=db.example.com retry=3
```

## Features

- 🎨 Colored output (auto-detected)
- 📊 Structured key-value logging
- ⏰ Timestamps
- 🎚️ Log levels
- 📤 Configurable output stream

## Configuration

```python
from logfmt import Logger, LogLevel

log = Logger(
    name="myapp",
    level=LogLevel.DEBUG,  # Minimum log level
    colorize=True,         # Enable colors
    timestamp=True,        # Show timestamps
)
```

## Log Levels

| Level | Value | Use Case |
|-------|-------|----------|
| DEBUG | 10 | Detailed debugging |
| INFO | 20 | General information |
| WARNING | 30 | Warning messages |
| ERROR | 40 | Error conditions |
| CRITICAL | 50 | Critical failures |

## License

MIT
