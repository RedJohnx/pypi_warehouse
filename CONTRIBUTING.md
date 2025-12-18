# Contributing to PyPI Warehouse

Thank you for your interest in contributing! 🎉

## 📋 How to Contribute

### Reporting Bugs
- Open an issue with a clear description
- Include Python version and OS
- Provide minimal reproducible example

### Suggesting Features
- Open an issue with `[Feature]` prefix
- Explain the use case and benefits

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Run tests: `pytest`
6. Commit: `git commit -m "Add amazing feature"`
7. Push: `git push origin feature/amazing-feature`
8. Open a Pull Request

## 🧪 Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/pypi_warehouse.git
cd pypi_warehouse

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dev dependencies
pip install -e ".[dev]"
```

## 📁 Project Structure

```
pypi_warehouse/
├── packages/
│   ├── retryit/
│   ├── envmaster/
│   ├── cachely/
│   └── ...
├── tests/
├── README.md
└── CONTRIBUTING.md
```

## ✅ Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public functions
- Keep functions focused and small

## 📝 Commit Messages

Use clear, descriptive commit messages:
- `feat: Add retry decorator with backoff`
- `fix: Handle None values in env parser`
- `docs: Update README examples`

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.
