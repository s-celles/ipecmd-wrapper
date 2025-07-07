"""
IPECMD Wrapper Package

A Python wrapper for Microchip's IPECMD tool for PIC microcontroller programming.
"""

__version__ = "0.1.0"
__author__ = "Sébastien Celles"
__email__ = "s.celles@gmail.com"

from .core import (
    get_ipecmd_path,
    validate_ipecmd,
    validate_hex_file,
    build_ipecmd_command,
    test_programmer_detection,
    execute_programming,
    program_pic,
    TOOL_CHOICES,
    VERSION_CHOICES,
    TOOL_MAP,
)

__all__ = [
    "get_ipecmd_path",
    "validate_ipecmd",
    "validate_hex_file",
    "build_ipecmd_command",
    "test_programmer_detection",
    "execute_programming",
    "program_pic",
    "TOOL_CHOICES",
    "VERSION_CHOICES",
    "TOOL_MAP",
]
