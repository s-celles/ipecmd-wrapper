# IPECMD Wrapper Development

This directory contains the IPECMD Wrapper package development environment.

## Quick Start

```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run tests with coverage
pytest --cov=ipecmd_wrapper

# Format code
black .

# Type checking
mypy .

# Build package
python -m build
```

## Package Structure

```
ipecmd_wrapper/
├── pyproject.toml          # Modern Python package configuration
├── README.md              # Package documentation
├── LICENSE                # MIT license
├── .gitignore            # Git ignore rules
├── ipecmd_wrapper/       # Main package directory
│   ├── __init__.py       # Package initialization
│   ├── cli.py           # Command-line interface
│   └── core.py          # Core functionality
└── tests/               # Test suite
    ├── __init__.py
    ├── test_cli.py
    ├── test_core.py
    ├── test_integration.py
    ├── test_performance.py
    └── test_compatibility.py
```

## Usage

After installation, you can use the wrapper as:

```bash
# Command-line tool
ipecmd-wrapper --device PIC16F876A --programmer pickit3 --hex-file firmware.hex

# Python module
python -m ipecmd_wrapper.cli --device PIC16F876A --programmer pickit3 --hex-file firmware.hex

# Python API
from ipecmd_wrapper import get_ipecmd_path, upload_firmware
```

## Development Commands

### Setup Development Environment

```bash
# Automated setup (recommended)
python setup_dev.py

# Manual setup
python -m venv .venv
source .venv/bin/activate  # Unix/macOS
.venv\Scripts\activate     # Windows
pip install -e .[dev]
pre-commit install
```

### Testing

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=ipecmd_wrapper --cov-report=html

# Run specific test categories
pytest -m unit           # Unit tests only
pytest -m integration    # Integration tests only
pytest -m performance    # Performance tests only
pytest -m compatibility  # Compatibility tests only

# Run tests in parallel
pytest -n auto

# Run specific test file
pytest tests/test_core.py
```

### Code Quality

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type checking
mypy .

# Security scanning
bandit -r ipecmd_wrapper/

# Run all pre-commit hooks
pre-commit run --all-files
```

### Build and Release

```bash
# Build package
python -m build

# Upload to PyPI (maintainers only)
twine upload dist/*

# Create release
git tag v0.1.0
git push origin v0.1.0
```

## Testing Strategy

### Test Categories

- **Unit Tests**: Test individual functions and classes in isolation
- **Integration Tests**: Test component interactions and workflows
- **Performance Tests**: Benchmark critical operations
- **Compatibility Tests**: Test across different platforms and Python versions

### Test Organization

- `test_cli.py`: Command-line interface tests
- `test_core.py`: Core functionality tests
- `test_integration.py`: Integration and workflow tests
- `test_performance.py`: Performance and benchmarking tests
- `test_compatibility.py`: Cross-platform compatibility tests

### Running Tests

```bash
# Quick test run (exclude slow tests)
pytest -m "not slow"

# Full test suite
pytest

# Coverage report
pytest --cov=ipecmd_wrapper --cov-report=html
open htmlcov/index.html  # View coverage report
```

## Code Style

We follow PEP 8 with these conventions:

- Line length: 88 characters (Black default)
- Use double quotes for strings
- Use type hints for all public functions
- Document public APIs with docstrings
- Use Google-style docstrings

## Continuous Integration

The project uses GitHub Actions for CI/CD:

- **Tests**: Run on Windows, Linux, and macOS
- **Python versions**: 3.9, 3.10, 3.11, 3.12
- **Code quality**: Linting, formatting, type checking
- **Coverage**: Minimum 80% code coverage
- **Security**: Vulnerability scanning

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create and push git tag
4. GitHub Actions automatically builds and publishes to PyPI
5. Update documentation

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
