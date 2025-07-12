# Contributing to IPECMD Wrapper

Thank you for your interest in contributing to the IPECMD Wrapper project! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/s-celles/ipecmd-wrapper.git
   cd ipecmd-wrapper
   ```
3. **Set up the development environment**:
   ```bash
   python setup_dev.py
   ```
4. **Activate the virtual environment**:
   - Windows: `.venv\Scripts\activate`
   - Unix/macOS: `source .venv/bin/activate`
5. **Run tests** to ensure everything works:
   ```bash
   python -m pytest tests/ -v
   ```

## 🛠️ Development Workflow

### Setting Up Your Development Environment

We provide several ways to set up your development environment:

1. **Automated setup** (recommended):
   ```bash
   python setup_dev.py
   ```

2. **Manual setup**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Unix/macOS
   # or
   .venv\Scripts\activate     # Windows

   pip install -e .[dev]
   pre-commit install
   ```

3. **Using Makefile** (Unix/macOS):
   ```bash
   make setup-dev
   ```

### Running Tests

We use pytest for testing with several test categories:

```bash
# Run all tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=ipecmd_wrapper

# Run only unit tests
python -m pytest -m unit

# Run only integration tests
python -m pytest -m integration

# Run specific test file
python -m pytest tests/test_core.py

# Run tests in parallel
python -m pytest -n auto
```

### Code Quality

We maintain high code quality standards:

```bash
# Format and lint code (replaces black, isort, flake8)
ruff check --fix .
ruff format .

# Type checking
mypy .

# Security analysis
bandit -r ipecmd_wrapper/

# Run all pre-commit hooks
pre-commit run --all-files
```

## 📋 Testing Guidelines

### Test Categories

We organize tests into several categories using pytest markers:

- `@pytest.mark.unit`: Unit tests for individual functions/classes
- `@pytest.mark.integration`: Integration tests for component interaction
- `@pytest.mark.performance`: Performance and benchmarking tests
- `@pytest.mark.compatibility`: Cross-platform compatibility tests
- `@pytest.mark.slow`: Tests that take longer to run

### Writing Tests

1. **Test file naming**: Use `test_*.py` format
2. **Test function naming**: Use `test_*` format
3. **Test class naming**: Use `Test*` format
4. **Use descriptive test names**: `test_upload_with_valid_hex_file_succeeds`
5. **Include docstrings**: Explain what the test verifies
6. **Use fixtures**: For common setup/teardown
7. **Mock external dependencies**: Use `unittest.mock` or `pytest-mock`

### Test Structure

```python
def test_feature_with_valid_input_succeeds():
    """Test that feature works correctly with valid input."""
    # Arrange
    input_data = "valid_input"
    expected_result = "expected_output"

    # Act
    result = feature_function(input_data)

    # Assert
    assert result == expected_result
```

## 🔧 Code Style

We follow PEP 8 with some modifications:

- Line length: 88 characters (Ruff default)
- Use double quotes for strings
- Use type hints where appropriate
- Document public functions and classes

### Pre-commit Hooks

We use pre-commit to ensure code quality:

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## 📝 Documentation

### Code Documentation

- Use docstrings for all public functions, classes, and modules
- Follow Google docstring format
- Include type hints in function signatures
- Document parameters, return values, and exceptions

### Example:

```python
def upload_firmware(hex_file: str, device: str, programmer: str = "pickit3") -> bool:
    """Upload firmware to PIC microcontroller.

    Args:
        hex_file: Path to the hex file to upload
        device: Target device name (e.g., "PIC16F876A")
        programmer: Programmer type (default: "pickit3")

    Returns:
        True if upload successful, False otherwise

    Raises:
        FileNotFoundError: If hex file doesn't exist
        RuntimeError: If upload fails
    """
```

## 🚀 Submitting Changes

### Pull Request Process

1. **Create a feature branch**: `git checkout -b feature/your-feature-name`
2. **Make your changes**: Follow the code style and testing guidelines
3. **Write tests**: Add tests for new functionality
4. **Run tests**: Ensure all tests pass
5. **Update documentation**: Update README, docstrings, etc.
6. **Commit changes**: Use clear, descriptive commit messages
7. **Push to your fork**: `git push origin feature/your-feature-name`
8. **Create pull request**: Submit a PR against the main branch

### Commit Messages

Use conventional commit format:

```
type(scope): description

feat(core): add support for PIC18F series
fix(cli): handle missing hex file gracefully
docs(readme): update installation instructions
test(core): add unit tests for device detection
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `style`: Code style changes
- `ci`: CI/CD changes

### Code Review

All changes must be reviewed before merging:

1. **Automated checks**: CI must pass
2. **Manual review**: At least one maintainer approval
3. **Testing**: New features must include tests
4. **Documentation**: User-facing changes need documentation updates

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Steps to reproduce**: Minimal steps to reproduce the bug
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Environment**: OS, Python version, package versions
6. **Code samples**: Minimal code that reproduces the issue

## 💡 Feature Requests

When requesting features:

1. **Use case**: Describe why this feature would be useful
2. **Proposed solution**: How you think it should work
3. **Alternatives**: Other solutions you've considered
4. **Impact**: Who would benefit from this feature

## 📜 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## 🤝 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Please be respectful and inclusive in all interactions.

## 🆘 Getting Help

If you need help:

1. Check the [documentation](https://s-celles.github.io/ipecmd-wrapper/)
2. Search existing [issues](https://github.com/s-celles/ipecmd-wrapper/issues)
3. Create a new issue with the "question" label
4. Join our discussions in the GitHub repository

## 🙏 Recognition

Contributors are recognized in:

- Git commit history
- Release notes
- Contributors section in README
- GitHub contributors graph

Thank you for contributing to IPECMD Wrapper! 🎉
