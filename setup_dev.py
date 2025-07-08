#!/usr/bin/env python3
"""
Development setup script for IPECMD Wrapper

This script sets up the development environment for the IPECMD wrapper project.
"""

import os
import subprocess  # nosec B404
import sys
from pathlib import Path


# Color codes for output
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    END = "\033[0m"


def print_colored(text: str, color: str) -> None:
    """Print colored text"""
    print(f"{color}{text}{Colors.END}")


def run_command(cmd: str, description: str, check: bool = True) -> bool:
    """Run a command and print status"""
    print_colored(f"\n🔧 {description}...", Colors.CYAN)
    try:
        result = subprocess.run(
            cmd, shell=True, check=check, capture_output=True, text=True
        )  # nosec B602
        if result.stdout:
            print(result.stdout)
        if result.stderr and check:
            print_colored(f"Warning: {result.stderr}", Colors.YELLOW)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print_colored(f"Error: {e}", Colors.RED)
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False


def check_python_version() -> bool:
    """Check if Python version is compatible"""
    print_colored("\n🐍 Checking Python version...", Colors.BLUE)
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print_colored("❌ Python 3.9+ is required", Colors.RED)
        return False

    print_colored("✅ Python version is compatible", Colors.GREEN)
    return True


def check_git() -> bool:
    """Check if git is available"""
    print_colored("\n📦 Checking git...", Colors.BLUE)
    try:
        result = subprocess.run(
            ["git", "--version"], capture_output=True, text=True, check=True
        )
        print(result.stdout.strip())
        print_colored("✅ Git is available", Colors.GREEN)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_colored("❌ Git is not available", Colors.RED)
        return False


def create_virtual_environment() -> bool:
    """Create virtual environment"""
    venv_path = Path(".venv")

    if venv_path.exists():
        print_colored("\n🔄 Virtual environment already exists", Colors.YELLOW)
        return True

    print_colored("\n🏗️  Creating virtual environment...", Colors.BLUE)
    success = run_command(
        f"{sys.executable} -m venv .venv", "Creating virtual environment"
    )

    if success:
        print_colored("✅ Virtual environment created", Colors.GREEN)
        return True
    else:
        print_colored("❌ Failed to create virtual environment", Colors.RED)
        return False


def get_pip_command() -> str:
    """Get the pip command for the current platform"""
    if os.name == "nt":  # Windows
        return r".venv\Scripts\pip.exe"
    else:  # Unix/Linux/macOS
        return ".venv/bin/pip"


def get_python_command() -> str:
    """Get the python command for the current platform"""
    if os.name == "nt":  # Windows
        return r".venv\Scripts\python.exe"
    else:  # Unix/Linux/macOS
        return ".venv/bin/python"


def upgrade_pip() -> bool:
    """Upgrade pip in virtual environment"""
    pip_cmd = get_pip_command()
    return run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip")


def install_package_dev() -> bool:
    """Install package in development mode with dev dependencies"""
    pip_cmd = get_pip_command()
    return run_command(
        f"{pip_cmd} install -e .[dev]", "Installing package in development mode"
    )


def install_pre_commit() -> bool:
    """Install pre-commit hooks"""
    python_cmd = get_python_command()
    return run_command(
        f"{python_cmd} -m pre_commit install", "Installing pre-commit hooks"
    )


def run_initial_tests() -> bool:
    """Run initial tests to verify setup"""
    python_cmd = get_python_command()
    print_colored("\n🧪 Running initial tests...", Colors.BLUE)
    success = run_command(
        f"{python_cmd} -m pytest tests/ -v --tb=short", "Running tests", check=False
    )

    if success:
        print_colored("✅ All tests passed", Colors.GREEN)
    else:
        print_colored(
            "⚠️  Some tests failed (this might be expected for initial setup)",
            Colors.YELLOW,
        )

    return success


def verify_installation() -> bool:
    """Verify the installation by importing the package"""
    python_cmd = get_python_command()
    print_colored("\n🔍 Verifying installation...", Colors.BLUE)

    # Test importing the package
    success = run_command(
        f'{python_cmd} -c "import ipecmd_wrapper; '
        f"print('✅ Package imported successfully')\"",
        "Testing package import",
        check=False,
    )

    if success:
        print_colored("✅ Package installation verified", Colors.GREEN)
    else:
        print_colored("❌ Package installation verification failed", Colors.RED)

    return success


def show_next_steps() -> None:
    """Show next steps for development"""
    print_colored("\n🎉 Development environment setup complete!", Colors.GREEN)
    print_colored("\n📋 Next steps:", Colors.BOLD)

    if os.name == "nt":  # Windows
        activate_cmd = r".venv\Scripts\activate"
    else:  # Unix/Linux/macOS
        activate_cmd = "source .venv/bin/activate"

    print(
        f"""
1. Activate the virtual environment:
   {activate_cmd}

2. Run tests:
   python -m pytest tests/ -v

3. Run tests with coverage:
   python -m pytest tests/ --cov=ipecmd_wrapper --cov-report=html

4. Format code:
   black .
   isort .

5. Run linting:
   flake8 .

6. Run type checking:
   mypy .

7. Run all pre-commit hooks:
   pre-commit run --all-files

8. Build package:
   python -m build

9. Start developing:
   - Edit code in ipecmd_wrapper/
   - Add tests in tests/
   - Update documentation as needed
"""
    )

    print_colored("📚 Documentation:", Colors.BOLD)
    print("- README.md: Project overview and usage")
    print("- CONTRIBUTING.md: Contribution guidelines")
    print("- DEVELOPMENT.md: Development guide")

    print_colored("\n🛠️  Development commands:", Colors.BOLD)
    print("- make help: Show all available make commands")
    print("- make test: Run all tests")
    print("- make dev-check: Run quick development checks")
    print("- make dev-test: Run full development test cycle")


def main() -> int:
    """Main setup function"""
    print_colored("🚀 Setting up IPECMD Wrapper development environment", Colors.BOLD)

    # Check prerequisites
    if not check_python_version():
        sys.exit(1)

    if not check_git():
        print_colored(
            "⚠️  Git is not available, but continuing setup...", Colors.YELLOW
        )

    # Setup steps
    steps = [
        ("Create virtual environment", create_virtual_environment),
        ("Upgrade pip", upgrade_pip),
        ("Install package in development mode", install_package_dev),
        ("Install pre-commit hooks", install_pre_commit),
        ("Verify installation", verify_installation),
        ("Run initial tests", run_initial_tests),
    ]

    failed_steps = []

    for step_name, step_func in steps:
        try:
            if not step_func():
                failed_steps.append(step_name)
        except Exception as e:
            print_colored(f"❌ Error in {step_name}: {e}", Colors.RED)
            failed_steps.append(step_name)

    if failed_steps:
        print_colored(
            f"\n⚠️  Some steps failed: {', '.join(failed_steps)}",
            Colors.YELLOW,
        )
        print_colored("You may need to run these steps manually.", Colors.YELLOW)

    show_next_steps()

    if not failed_steps:
        print_colored("\n✅ Setup completed successfully!", Colors.GREEN)
        return 0
    else:
        print_colored(
            "\n⚠️  Setup completed with some issues. Check the output above.",
            Colors.YELLOW,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
