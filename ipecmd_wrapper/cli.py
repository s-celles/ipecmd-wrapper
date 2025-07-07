#!/usr/bin/env python3
"""
Command-line interface for IPECMD Wrapper

This module provides the main entry point for the IPECMD wrapper.
"""

import argparse
import sys
from typing import List, Optional
from colorama import init, Fore, Style

# Initialize colorama for cross-platform support
init(autoreset=True)

from .core import program_pic, TOOL_CHOICES, VERSION_CHOICES

# Version information
__version__ = "0.1.0"


def print_colored(text: str, color: str) -> None:
    """Print text with specified color using colorama"""
    print(f"{color}{text}{Style.RESET_ALL}")


# Color constants
class Colors:
    CYAN = Fore.CYAN


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(
        description="IPECMD wrapper for PIC programming",
        prog="ipecmd-wrapper"
    )
    
    # Version argument
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    # Required arguments
    parser.add_argument(
        "-P", "--part", 
        required=True, 
        help="Part Selection (required)"
    )
    parser.add_argument(
        "-T", "--tool",
        required=True,
        choices=TOOL_CHOICES,
        help="Tool Selection (required)",
    )
    parser.add_argument(
        "-F", "--file", 
        required=True, 
        help="Hex File Selection (required)"
    )
    parser.add_argument(
        "-W", "--power",
        required=True,
        help="Power target from tool (VDD voltage, required)",
    )
    
    # Optional programming arguments
    parser.add_argument(
        "-M", "--memory",
        default="",
        help="Program Device memory regions (P=Program, E=EEPROM, I=ID, C=Configuration, B=Boot, A=Auxiliary)",
    )
    parser.add_argument(
        "-Y", "--verify",
        default="",
        help="Verify Device memory regions (P=Program, E=EEPROM, I=ID, C=Configuration, B=Boot, A=Auxiliary)",
    )
    parser.add_argument(
        "-E", "--erase",
        action="store_true",
        help="Erase Flash Device before programming",
    )
    parser.add_argument(
        "-OL", "--logout", 
        action="store_true", 
        help="Release from Reset"
    )
    parser.add_argument(
        "-OD", "--vdd-first", 
        action="store_true", 
        help="VDD First (default: VPP First)"
    )
    
    # Testing and debugging
    parser.add_argument(
        "--test-programmer",
        action="store_true",
        help="Test programmer detection before programming",
    )
    
    # IPECMD path/version arguments
    parser.add_argument(
        "--ipecmd-version",
        choices=VERSION_CHOICES,
        help="MPLAB IPE version to use (ignored if --ipecmd-path is provided)",
    )
    parser.add_argument(
        "--ipecmd-path", 
        help="Full path to ipecmd.exe (overrides --ipecmd-version)"
    )
    
    return parser


def main(argv: Optional[List[str]] = None) -> None:
    """
    Main entry point for the IPECMD wrapper CLI
    
    Args:
        argv: Command line arguments (defaults to sys.argv)
    """
    print_colored("=== IPECMD WRAPPER ===", Colors.CYAN)
    
    parser = create_argument_parser()
    args = parser.parse_args(argv)
    
    # Validate that either ipecmd-version or ipecmd-path is provided
    if not args.ipecmd_version and not args.ipecmd_path:
        parser.error("Either --ipecmd-version or --ipecmd-path must be provided")
    
    # Call the main programming function
    program_pic(args)


if __name__ == "__main__":
    main()
