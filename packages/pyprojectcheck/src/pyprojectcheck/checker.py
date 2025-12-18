"""
Validate pyproject.toml files.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore


@dataclass
class Issue:
    """Represents a validation issue."""
    level: str  # "error" or "warning"
    message: str
    path: str = ""
    
    def __str__(self) -> str:
        prefix = "❌" if self.level == "error" else "⚠️"
        if self.path:
            return f"{prefix} [{self.path}] {self.message}"
        return f"{prefix} {self.message}"


@dataclass
class ValidationResult:
    """Result of pyproject.toml validation."""
    valid: bool
    issues: List[Issue] = field(default_factory=list)
    
    @property
    def errors(self) -> List[Issue]:
        return [i for i in self.issues if i.level == "error"]
    
    @property
    def warnings(self) -> List[Issue]:
        return [i for i in self.issues if i.level == "warning"]
    
    def __str__(self) -> str:
        if self.valid and not self.issues:
            return "✅ pyproject.toml is valid"
        
        lines = []
        for issue in self.issues:
            lines.append(str(issue))
        
        if self.valid:
            lines.append(f"\n✅ Valid with {len(self.warnings)} warning(s)")
        else:
            lines.append(f"\n❌ Invalid: {len(self.errors)} error(s), {len(self.warnings)} warning(s)")
        
        return "\n".join(lines)


def _check_build_system(data: Dict, issues: List[Issue]) -> None:
    """Check [build-system] section."""
    if "build-system" not in data:
        issues.append(Issue("error", "Missing [build-system] section"))
        return
    
    build = data["build-system"]
    
    if "requires" not in build:
        issues.append(Issue("error", "Missing 'requires' field", "build-system"))
    elif not isinstance(build["requires"], list):
        issues.append(Issue("error", "'requires' must be a list", "build-system.requires"))
    
    if "build-backend" not in build:
        issues.append(Issue("error", "Missing 'build-backend' field", "build-system"))
    elif not isinstance(build["build-backend"], str):
        issues.append(Issue("error", "'build-backend' must be a string", "build-system.build-backend"))


def _check_project(data: Dict, issues: List[Issue]) -> None:
    """Check [project] section."""
    if "project" not in data:
        issues.append(Issue("error", "Missing [project] section"))
        return
    
    project = data["project"]
    
    # Required fields
    if "name" not in project:
        issues.append(Issue("error", "Missing 'name' field", "project"))
    elif not isinstance(project["name"], str):
        issues.append(Issue("error", "'name' must be a string", "project.name"))
    elif not project["name"].replace("-", "").replace("_", "").isalnum():
        issues.append(Issue("warning", "Package name should be lowercase with hyphens", "project.name"))
    
    if "version" not in project and "dynamic" not in project:
        issues.append(Issue("error", "Missing 'version' field (or add to 'dynamic')", "project"))
    elif "version" in project and not isinstance(project["version"], str):
        issues.append(Issue("error", "'version' must be a string", "project.version"))
    
    # Recommended fields
    if "description" not in project:
        issues.append(Issue("warning", "Missing 'description' field (recommended)", "project"))
    
    if "readme" not in project:
        issues.append(Issue("warning", "Missing 'readme' field (recommended)", "project"))
    
    if "license" not in project:
        issues.append(Issue("warning", "Missing 'license' field (recommended)", "project"))
    
    if "requires-python" not in project:
        issues.append(Issue("warning", "Missing 'requires-python' field (recommended)", "project"))
    
    if "authors" not in project:
        issues.append(Issue("warning", "Missing 'authors' field (recommended)", "project"))
    
    # Validate authors format
    if "authors" in project:
        if not isinstance(project["authors"], list):
            issues.append(Issue("error", "'authors' must be a list", "project.authors"))
        else:
            for i, author in enumerate(project["authors"]):
                if not isinstance(author, dict):
                    issues.append(Issue("error", f"Author must be a table", f"project.authors[{i}]"))
                elif "name" not in author and "email" not in author:
                    issues.append(Issue("error", "Author must have 'name' or 'email'", f"project.authors[{i}]"))
    
    # Validate classifiers
    if "classifiers" in project:
        if not isinstance(project["classifiers"], list):
            issues.append(Issue("error", "'classifiers' must be a list", "project.classifiers"))
    
    # Validate dependencies
    if "dependencies" in project:
        if not isinstance(project["dependencies"], list):
            issues.append(Issue("error", "'dependencies' must be a list", "project.dependencies"))
    
    # Validate optional-dependencies
    if "optional-dependencies" in project:
        if not isinstance(project["optional-dependencies"], dict):
            issues.append(Issue("error", "'optional-dependencies' must be a table", "project.optional-dependencies"))


def _check_urls(data: Dict, issues: List[Issue]) -> None:
    """Check [project.urls] section."""
    if "project" not in data:
        return
    
    project = data["project"]
    
    if "urls" not in project:
        issues.append(Issue("warning", "Missing 'urls' section (recommended)", "project"))
        return
    
    urls = project["urls"]
    
    if not isinstance(urls, dict):
        issues.append(Issue("error", "'urls' must be a table", "project.urls"))
        return
    
    for key, value in urls.items():
        if not isinstance(value, str):
            issues.append(Issue("error", f"URL must be a string", f"project.urls.{key}"))
        elif not value.startswith(("http://", "https://")):
            issues.append(Issue("warning", f"URL should start with http:// or https://", f"project.urls.{key}"))


def check(content: str) -> ValidationResult:
    """
    Validate pyproject.toml content.
    
    Args:
        content: The TOML content as a string
    
    Returns:
        ValidationResult with issues found
    """
    issues: List[Issue] = []
    
    try:
        data = tomllib.loads(content)
    except Exception as e:
        return ValidationResult(
            valid=False,
            issues=[Issue("error", f"Invalid TOML: {e}")]
        )
    
    _check_build_system(data, issues)
    _check_project(data, issues)
    _check_urls(data, issues)
    
    has_errors = any(i.level == "error" for i in issues)
    
    return ValidationResult(valid=not has_errors, issues=issues)


def check_file(path: str) -> ValidationResult:
    """
    Validate a pyproject.toml file.
    
    Args:
        path: Path to the pyproject.toml file
    
    Returns:
        ValidationResult with issues found
    """
    file_path = Path(path)
    
    if not file_path.exists():
        return ValidationResult(
            valid=False,
            issues=[Issue("error", f"File not found: {path}")]
        )
    
    if not file_path.name == "pyproject.toml":
        return ValidationResult(
            valid=False,
            issues=[Issue("warning", "File is not named 'pyproject.toml'")]
        )
    
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return ValidationResult(
            valid=False,
            issues=[Issue("error", f"Failed to read file: {e}")]
        )
    
    return check(content)


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) < 2:
        path = "pyproject.toml"
    else:
        path = sys.argv[1]
    
    result = check_file(path)
    print(result)
    
    return 0 if result.valid else 1


if __name__ == "__main__":
    sys.exit(main())
