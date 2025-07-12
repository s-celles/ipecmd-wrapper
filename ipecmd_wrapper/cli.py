#!/usr/bin/env python3
"""
Command-line interface for IPECMD Wrapper

This module provides the main entry point for the IPECMD wrapper.
"""

from enum import Enum
from pathlib import Path
from typing import Annotated, Optional, Union

import typer

from .core import program_pic
from .logger import log

# Version information
__version__ = "0.1.0"


# Create enums for better validation
class ToolChoice(str, Enum):
    """Available programmer tools"""

    PK3 = "PK3"
    PK4 = "PK4"
    PK5 = "PK5"
    ICD3 = "ICD3"
    ICD4 = "ICD4"
    ICD5 = "ICD5"
    ICE4 = "ICE4"
    RICE = "RICE"
    SNAP = "SNAP"
    PM3 = "PM3"
    PKOB = "PKOB"
    PKOB4 = "PKOB4"
    J32 = "J32"


class VersionChoice(str, Enum):
    """Available MPLAB IPE versions"""

    V5_50 = "5.50"
    V6_00 = "6.00"
    V6_05 = "6.05"
    V6_10 = "6.10"
    V6_15 = "6.15"
    V6_20 = "6.20"
    V6_25 = "6.25"


# Create the main Typer app
app = typer.Typer(
    name="ipecmd-wrapper",
    help="IPECMD wrapper for PIC programming",
    add_completion=False,
)


def version_callback(value: bool) -> None:
    """Print version and exit"""
    if value:
        typer.echo(f"ipecmd-wrapper {__version__}")
        raise typer.Exit()


# Simple namespace class to mimic argparse.Namespace for compatibility
class Args:
    def __init__(self, **kwargs: Union[str, bool, None]) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)


@app.command()
def main(
    # Required arguments
    part: Annotated[
        str, typer.Option("--part", "-P", help="Part Selection (required)")
    ] = ...,
    tool: Annotated[
        ToolChoice, typer.Option("--tool", "-T", help="Tool Selection (required)")
    ] = ...,
    file: Annotated[
        Path,
        typer.Option("--file", "-F", help="Hex File Selection (required)", exists=True),
    ] = ...,
    power: Annotated[
        str,
        typer.Option(
            "--power", "-W", help="Power target from tool (VDD voltage, required)"
        ),
    ] = ...,
    # Optional programming arguments
    memory: Annotated[
        str,
        typer.Option(
            "--memory",
            "-M",
            help="Program Device memory regions (P=Program, E=EEPROM, I=ID, "
            "C=Configuration, B=Boot, A=Auxiliary)",
        ),
    ] = "",
    verify: Annotated[
        str,
        typer.Option(
            "--verify",
            "-Y",
            help="Verify Device memory regions (P=Program, E=EEPROM, I=ID, "
            "C=Configuration, B=Boot, A=Auxiliary)",
        ),
    ] = "",
    erase: Annotated[
        bool,
        typer.Option("--erase", "-E", help="Erase Flash Device before programming"),
    ] = False,
    logout: Annotated[
        bool, typer.Option("--logout", "-OL", help="Release from Reset")
    ] = False,
    vdd_first: Annotated[
        bool, typer.Option("--vdd-first", "-OD", help="VDD First (default: VPP First)")
    ] = False,
    # Testing and debugging
    test_programmer: Annotated[
        bool,
        typer.Option(
            "--test-programmer", help="Test programmer detection before programming"
        ),
    ] = False,
    # IPECMD path/version arguments
    ipecmd_version: Annotated[
        Optional[VersionChoice],
        typer.Option(
            "--ipecmd-version",
            help="MPLAB IPE version to use (ignored if --ipecmd-path is provided)",
        ),
    ] = None,
    ipecmd_path: Annotated[
        Optional[str],
        typer.Option(
            "--ipecmd-path", help="Full path to ipecmd.exe (overrides --ipecmd-version)"
        ),
    ] = None,
    # Version flag
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version", callback=version_callback, help="Show version and exit"
        ),
    ] = None,
) -> None:
    """
    IPECMD wrapper for PIC programming

    A Python wrapper for Microchip's IPECMD tool for PIC microcontroller programming.
    """
    log.info("=== IPECMD WRAPPER ===")

    # Validate that either ipecmd-version or ipecmd-path is provided
    if not ipecmd_version and not ipecmd_path:
        typer.echo(
            "Error: Either --ipecmd-version or --ipecmd-path must be provided",
            err=True,
        )
        raise typer.Exit(1)

    # Create args object compatible with existing core.program_pic function
    args = Args(
        part=part,
        tool=tool.value,  # Get string value from enum
        file=str(file),  # Convert Path to string for compatibility
        power=power,
        memory=memory,
        verify=verify,
        erase=erase,
        logout=logout,
        vdd_first=vdd_first,
        test_programmer=test_programmer,
        ipecmd_version=ipecmd_version.value
        if ipecmd_version
        else None,  # Get string value from enum
        ipecmd_path=ipecmd_path,
    )

    # Call the main programming function with error handling
    try:
        program_pic(args)
    except (ValueError, FileNotFoundError) as e:
        log.error(f"Error: {e}")
        raise typer.Exit(1) from e
    except Exception as e:
        log.error(f"Unexpected error: {e}")
        raise typer.Exit(1) from None


def cli_main() -> None:
    """Entry point for the CLI"""
    app()


if __name__ == "__main__":
    cli_main()
