# pyprojectcheck ✅

Validate pyproject.toml files for correctness and best practices.

## Installation

```bash
pip install pyprojectcheck
```

## Usage

### CLI

```bash
# Check current directory
pyprojectcheck

# Check specific file
pyprojectcheck path/to/pyproject.toml
```

### Python API

```python
from pyprojectcheck import check_file, check

# Check a file
result = check_file("pyproject.toml")
print(result)

# Check content directly
content = """
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mypackage"
version = "1.0.0"
"""

result = check(content)
if result.valid:
    print("✅ Valid!")
else:
    for error in result.errors:
        print(error)
```

## What It Checks

### Errors
- Missing `[build-system]` section
- Missing `requires` or `build-backend`
- Missing `[project]` section
- Missing `name` or `version`
- Invalid field types

### Warnings
- Missing recommended fields (description, readme, license)
- Missing `requires-python`
- Missing `authors`
- Missing `urls`

## Output Example

```
⚠️ [project] Missing 'description' field (recommended)
⚠️ [project] Missing 'readme' field (recommended)
❌ [project.authors[0]] Author must have 'name' or 'email'

❌ Invalid: 1 error(s), 2 warning(s)
```

## License

MIT
