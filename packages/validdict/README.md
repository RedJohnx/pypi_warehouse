# validdict ✅

Dictionary schema validation for Python.

## Installation

```bash
pip install validdict
```

## Usage

```python
from validdict import validate, String, Integer, Email, Boolean

data = {
    "name": "John Doe",
    "age": 30,
    "email": "john@example.com",
    "active": True
}

schema = {
    "name": String(min_length=1, max_length=100),
    "age": Integer(min_value=0, max_value=150),
    "email": Email(required=False),
    "active": Boolean(default=True),
}

result = validate(data, schema)
```

## Field Types

| Field | Description |
|-------|-------------|
| `String` | String with length/pattern validation |
| `Integer` | Integer with min/max validation |
| `Float` | Float with min/max validation |
| `Boolean` | Boolean value |
| `List_` | List with item type validation |
| `Dict_` | Nested dictionary |
| `Email` | Email format validation |
| `Enum_` | Value from allowed list |

## Field Options

```python
# Required (default)
String()

# Optional with default
String(required=False, default="unknown")

# String constraints
String(min_length=1, max_length=100, pattern=r"^[a-z]+$")

# Number constraints
Integer(min_value=0, max_value=100)

# List with item validation
List_(item_type=String(), min_length=1)

# Nested schema
Dict_({
    "street": String(),
    "city": String(),
})
```

## Error Handling

```python
from validdict import validate, ValidationError

try:
    result = validate(data, schema)
except ValidationError as e:
    print(f"Validation failed: {e.message}")
    print(f"At path: {e.path}")
```

## License

MIT
