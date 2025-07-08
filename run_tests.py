#!/usr/bin/env python3
"""
Test runner script for IPECMD Wrapper

This script provides a convenient way to run different types of tests
with various configurations.
"""

import argparse
import subprocess  # nosec B404
import sys
from typing import List


def run_command(
    cmd: List[str], description: str = "Running command", verbose: bool = False
) -> bool:
    """Run a command and return its result"""
    if verbose:
        print(f"🔧 {description}...")
        print(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd, capture_output=not verbose, text=True, check=True
        )  # nosec B603
        if verbose and result.stdout:
            print(result.stdout)
        if verbose and result.stderr:
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stdout:
            print("STDOUT:")
            print(e.stdout)
        if e.stderr:
            print("STDERR:")
            print(e.stderr)
        return False


def main() -> int:  # noqa: C901
    parser = argparse.ArgumentParser(description="Test runner for IPECMD Wrapper")
    parser.add_argument(
        "--type",
        choices=["unit", "integration", "performance", "compatibility", "all"],
        default="all",
        help="Type of tests to run",
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Run tests with coverage report"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--parallel",
        "-n",
        type=int,
        default=1,
        help="Number of parallel workers (default: 1)",
    )
    parser.add_argument(
        "--fast", action="store_true", help="Run fast tests only (exclude slow tests)"
    )
    parser.add_argument(
        "--html", action="store_true", help="Generate HTML coverage report"
    )
    parser.add_argument(
        "--xml", action="store_true", help="Generate XML coverage report"
    )
    parser.add_argument(
        "--fail-under",
        type=int,
        default=75,
        help="Minimum coverage percentage (default: 75)",
    )

    args = parser.parse_args()

    # Build pytest command
    cmd = ["python", "-m", "pytest"]

    # Add test selection based on type
    if args.type == "unit":
        cmd.extend(["-m", "unit"])
    elif args.type == "integration":
        cmd.extend(["-m", "integration"])
    elif args.type == "performance":
        cmd.extend(["-m", "performance"])
    elif args.type == "compatibility":
        cmd.extend(["-m", "compatibility"])
    elif args.type == "all":
        pass  # Run all tests

    # Add fast filter
    if args.fast:
        if args.type == "all":
            cmd.extend(["-m", "not slow"])
        else:
            cmd.extend(["-m", f"{args.type} and not slow"])

    # Add coverage options
    if args.coverage:
        cmd.extend(
            [
                "--cov=ipecmd_wrapper",
                "--cov-report=term-missing",
                f"--cov-fail-under={args.fail_under}",
            ]
        )

        if args.html:
            cmd.append("--cov-report=html")

        if args.xml:
            cmd.append("--cov-report=xml")

    # Add parallel execution
    if args.parallel > 1:
        cmd.extend(["-n", str(args.parallel)])

    # Add verbosity
    if args.verbose:
        cmd.append("-v")

    # Add test directory
    cmd.append("tests/")

    # Print test configuration
    print("🧪 IPECMD Wrapper Test Runner")
    print("=" * 40)
    print(f"Test type: {args.type}")
    print(f"Coverage: {args.coverage}")
    print(f"Parallel workers: {args.parallel}")
    print(f"Fast mode: {args.fast}")
    print(f"Verbose: {args.verbose}")
    if args.coverage:
        print(f"Coverage threshold: {args.fail_under}%")
    print("-" * 40)

    # Run tests
    success = run_command(cmd, "Running tests", args.verbose)

    if success:
        print("✅ All tests passed!")
        if args.coverage and args.html:
            print("📊 Coverage report generated in htmlcov/")
    else:
        print("❌ Some tests failed!")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
