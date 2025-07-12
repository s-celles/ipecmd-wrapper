# Makefile for IPECMD Wrapper development and testing

# Python interpreter
PYTHON := python

# Package name
PACKAGE := ipecmd_wrapper

# Test directories
TEST_DIR := tests
SRC_DIR := $(PACKAGE)

# Coverage settings
COVERAGE_MIN := 80
COVERAGE_HTML_DIR := htmlcov

# Virtual environment
VENV_DIR := .venv
VENV_ACTIVATE := $(VENV_DIR)/Scripts/activate

.PHONY: help install install-dev test test-fast test-slow test-coverage test-unit test-integration test-performance test-compatibility lint format type-check security clean build upload docs pre-commit setup-dev

help:
	@echo "IPECMD Wrapper Development Commands"
	@echo "=================================="
	@echo ""
	@echo "Setup:"
	@echo "  setup-dev         Set up development environment"
	@echo "  install           Install package"
	@echo "  install-dev       Install package with development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  test              Run all tests"
	@echo "  test-fast         Run fast tests (exclude slow tests)"
	@echo "  test-slow         Run slow tests only"
	@echo "  test-coverage     Run tests with coverage report"
	@echo "  test-unit         Run unit tests only"
	@echo "  test-integration  Run integration tests only"
	@echo "  test-performance  Run performance tests only"
	@echo "  test-compatibility Run compatibility tests only"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint              Run linting (ruff)"
	@echo "  format            Format code (ruff)"
	@echo "  type-check        Run type checking (mypy)"
	@echo "  security          Run security scanning (bandit)"
	@echo "  pre-commit        Run pre-commit hooks"
	@echo ""
	@echo "Build:"
	@echo "  clean             Clean build artifacts"
	@echo "  build             Build package"
	@echo "  upload            Upload to PyPI"
	@echo ""
	@echo "Documentation:"
	@echo "  docs              Build documentation"

# Setup commands
setup-dev:
	@echo "Setting up development environment..."
	$(PYTHON) setup_dev.py

install:
	@echo "Installing package..."
	pip install -e .

install-dev:
	@echo "Installing package with development dependencies..."
	pip install -e .[dev]

# Test commands
test:
	@echo "Running all tests..."
	pytest $(TEST_DIR) -v

test-fast:
	@echo "Running fast tests..."
	pytest $(TEST_DIR) -v -m "not slow"

test-slow:
	@echo "Running slow tests..."
	pytest $(TEST_DIR) -v -m "slow"

test-coverage:
	@echo "Running tests with coverage..."
	pytest $(TEST_DIR) --cov=$(PACKAGE) --cov-report=html --cov-report=term-missing --cov-fail-under=$(COVERAGE_MIN)

test-unit:
	@echo "Running unit tests..."
	pytest $(TEST_DIR) -v -m "unit"

test-integration:
	@echo "Running integration tests..."
	pytest $(TEST_DIR) -v -m "integration"

test-performance:
	@echo "Running performance tests..."
	pytest $(TEST_DIR) -v -m "performance"

test-compatibility:
	@echo "Running compatibility tests..."
	pytest $(TEST_DIR) -v -m "compatibility"

# Code quality commands
lint:
	@echo "Running linting..."
	ruff check $(SRC_DIR) $(TEST_DIR)

format:
	@echo "Formatting code..."
	ruff format $(SRC_DIR) $(TEST_DIR)

type-check:
	@echo "Running type checking..."
	mypy $(SRC_DIR)

security:
	@echo "Running security scanning..."
	bandit -r $(SRC_DIR)

pre-commit:
	@echo "Running pre-commit hooks..."
	pre-commit run --all-files

# Build commands
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf $(COVERAGE_HTML_DIR)/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	@echo "Building package..."
	$(PYTHON) -m build

upload: build
	@echo "Uploading to PyPI..."
	twine upload dist/*

# Documentation commands
docs:
	@echo "Building documentation..."
	mkdocs build

# Development workflow commands
dev-setup: setup-dev install-dev
	@echo "Development environment ready!"

dev-test: format lint type-check test-coverage
	@echo "Full development test cycle complete!"

dev-check: format lint type-check test-fast
	@echo "Quick development check complete!"

# CI/CD simulation
ci-test:
	@echo "Running CI test simulation..."
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) type-check
	$(MAKE) security
	$(MAKE) test-coverage
	@echo "CI test simulation complete!"

# Release commands
release-check: ci-test
	@echo "Release check complete!"

release: release-check build upload
	@echo "Release complete!"

# Platform-specific commands
ifeq ($(OS),Windows_NT)
    VENV_ACTIVATE := $(VENV_DIR)/Scripts/activate
else
    VENV_ACTIVATE := $(VENV_DIR)/bin/activate
endif

# Help for platform-specific setup
platform-help:
ifeq ($(OS),Windows_NT)
	@echo "Windows detected - use PowerShell or Command Prompt"
	@echo "Virtual environment activation: $(VENV_ACTIVATE)"
else
	@echo "Unix/Linux/macOS detected"
	@echo "Virtual environment activation: source $(VENV_ACTIVATE)"
endif
