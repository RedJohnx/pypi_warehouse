"""
Dictionary schema validation.
"""

from typing import Any, Dict, List, Optional, Type, Union, Callable


class ValidationError(Exception):
    """Raised when validation fails."""
    
    def __init__(self, message: str, path: str = ""):
        self.message = message
        self.path = path
        full_message = f"{path}: {message}" if path else message
        super().__init__(full_message)


class Field:
    """Base field for schema validation."""
    
    def __init__(
        self,
        required: bool = True,
        default: Any = None,
        validators: Optional[List[Callable]] = None,
    ):
        self.required = required
        self.default = default
        self.validators = validators or []
    
    def validate(self, value: Any, path: str = "") -> Any:
        raise NotImplementedError


class String(Field):
    """String field."""
    
    def __init__(
        self,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        pattern: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = pattern
    
    def validate(self, value: Any, path: str = "") -> str:
        if not isinstance(value, str):
            raise ValidationError(f"expected string, got {type(value).__name__}", path)
        
        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(f"string length must be >= {self.min_length}", path)
        
        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(f"string length must be <= {self.max_length}", path)
        
        if self.pattern is not None:
            import re
            if not re.match(self.pattern, value):
                raise ValidationError(f"string must match pattern '{self.pattern}'", path)
        
        return value


class Integer(Field):
    """Integer field."""
    
    def __init__(
        self,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, value: Any, path: str = "") -> int:
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValidationError(f"expected integer, got {type(value).__name__}", path)
        
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"value must be >= {self.min_value}", path)
        
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(f"value must be <= {self.max_value}", path)
        
        return value


class Float(Field):
    """Float field."""
    
    def __init__(
        self,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, value: Any, path: str = "") -> float:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValidationError(f"expected number, got {type(value).__name__}", path)
        
        value = float(value)
        
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"value must be >= {self.min_value}", path)
        
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(f"value must be <= {self.max_value}", path)
        
        return value


class Boolean(Field):
    """Boolean field."""
    
    def validate(self, value: Any, path: str = "") -> bool:
        if not isinstance(value, bool):
            raise ValidationError(f"expected boolean, got {type(value).__name__}", path)
        return value


class List_(Field):
    """List field."""
    
    def __init__(
        self,
        item_type: Optional[Field] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.item_type = item_type
        self.min_length = min_length
        self.max_length = max_length
    
    def validate(self, value: Any, path: str = "") -> list:
        if not isinstance(value, list):
            raise ValidationError(f"expected list, got {type(value).__name__}", path)
        
        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(f"list length must be >= {self.min_length}", path)
        
        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(f"list length must be <= {self.max_length}", path)
        
        if self.item_type:
            validated = []
            for i, item in enumerate(value):
                item_path = f"{path}[{i}]" if path else f"[{i}]"
                validated.append(self.item_type.validate(item, item_path))
            return validated
        
        return value


class Dict_(Field):
    """Nested dictionary field."""
    
    def __init__(self, schema: Dict[str, Field], **kwargs):
        super().__init__(**kwargs)
        self.schema = schema
    
    def validate(self, value: Any, path: str = "") -> dict:
        if not isinstance(value, dict):
            raise ValidationError(f"expected dict, got {type(value).__name__}", path)
        
        return _validate_dict(value, self.schema, path)


class Email(String):
    """Email field with basic validation."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def validate(self, value: Any, path: str = "") -> str:
        value = super().validate(value, path)
        
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValidationError("invalid email format", path)
        
        return value


class Enum_(Field):
    """Enum field - value must be one of allowed values."""
    
    def __init__(self, values: List[Any], **kwargs):
        super().__init__(**kwargs)
        self.values = values
    
    def validate(self, value: Any, path: str = "") -> Any:
        if value not in self.values:
            raise ValidationError(f"must be one of {self.values}", path)
        return value


def _validate_dict(data: Dict, schema: Dict[str, Field], base_path: str = "") -> Dict:
    """Validate a dictionary against a schema."""
    result = {}
    
    for key, field in schema.items():
        path = f"{base_path}.{key}" if base_path else key
        
        if key not in data:
            if field.required:
                raise ValidationError(f"missing required field", path)
            elif field.default is not None:
                result[key] = field.default
            continue
        
        result[key] = field.validate(data[key], path)
    
    return result


class Schema:
    """
    Schema definition for dictionary validation.
    
    Example:
        schema = Schema({
            "name": String(min_length=1),
            "age": Integer(min_value=0),
            "email": Email(required=False),
        })
        
        result = schema.validate(data)
    """
    
    def __init__(self, fields: Dict[str, Field]):
        self.fields = fields
    
    def validate(self, data: Dict) -> Dict:
        """Validate data against schema."""
        if not isinstance(data, dict):
            raise ValidationError(f"expected dict, got {type(data).__name__}")
        return _validate_dict(data, self.fields)


def validate(data: Dict, schema: Dict[str, Field]) -> Dict:
    """
    Validate a dictionary against a schema.
    
    Example:
        from validdict import validate, String, Integer
        
        data = {"name": "John", "age": 30}
        schema = {
            "name": String(min_length=1),
            "age": Integer(min_value=0),
        }
        
        result = validate(data, schema)
    """
    return _validate_dict(data, schema)
