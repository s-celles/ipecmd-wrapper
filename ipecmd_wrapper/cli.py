#!/usr/bin/env python3
"""
Command-line interface for IPECMD Wrapper

This module provides the main entry point for the IPECMD wrapper.
"""

import os
import sys
from enum import Enum
from pathlib import Path
from typing import Annotated, Optional, Union

import typer

from .core import program_pic, run_cmd_with_passthrough_option
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


def autodetect_ipecmd():
    """Detect installed MPLABX versions and return latest ipecmd_version and path."""
    candidates = []
    if os.name == "nt":
        base = Path("C:/Program Files/Microchip/MPLABX")
    elif sys.platform == "darwin":
        base = Path("/Applications/microchip/mplabx")
    else:
        base = Path("/opt/microchip/mplabx")
    if base.exists():
        for d in base.iterdir():
            if d.is_dir() and d.name.startswith("v"):
                version = d.name[1:]
                ipecmd = (
                    d
                    / "mplab_platform"
                    / "mplab_ipe"
                    / ("ipecmd.exe" if os.name == "nt" else "ipecmd")
                )
                if ipecmd.exists():
                    candidates.append((version, str(ipecmd)))
    if candidates:
        # Sort by version (as float), pick highest
        candidates.sort(key=lambda x: float(x[0]), reverse=True)
        return candidates[0]
    return None, None


@app.command()
def main(
    part: Annotated[
        Optional[str],
        typer.Argument(help="Part Selection"),
    ] = None,
    tool: Annotated[
        Optional[ToolChoice],
        typer.Argument(help="Tool Selection"),
    ] = None,
    # Optional file and power arguments
    file: Annotated[
        Optional[Path],
        typer.Option("--file", "-F", help="Hex File Selection", exists=True),
    ] = None,
    power: Annotated[
        Optional[float],
        typer.Option("--power", "-P", help="Power target from tool (VDD voltage)"),
    ] = None,
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
    ipecmd_help: Annotated[
        Optional[bool],
        typer.Option(
            "--ipecmd-help",
            help="Show IPECMD help output and exit",
        ),
    ] = None,
    # Passthrough for raw IPECMD options
    passthrough: Annotated[
        Optional[str],
        typer.Option(
            "--passthrough",
            "-p",
            help="Pass extra raw options directly to IPECMD (e.g. '--passthrough=\"-K -I\"')",
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

    Arguments:
        part: Part Selection (e.g., PIC16F877A)
        tool: Tool Selection (PK3, PK4, PK5, etc.)

    Options:
        --file: Path to hex file for programming
        --power: Power target from tool (VDD voltage, e.g., 5.0)
    """
    log.info("=== IPECMD WRAPPER ===")

    # Autodetect if neither version nor path is given
    autodetected_version = None
    autodetected_path = None
    if not ipecmd_version and not ipecmd_path:
        autodetected_version, autodetected_path = autodetect_ipecmd()
        if not autodetected_version:
            typer.echo(
                "Error: Could not autodetect any installed MPLABX/IPECMD. Please specify --ipecmd-version or --ipecmd-path.",
                err=True,
            )
            raise typer.Exit(1)
        log.info(f"Autodetected MPLABX version: {autodetected_version}")
        log.info(f"Autodetected IPECMD path: {autodetected_path}")

    # Handle --ipecmd-help
    if ipecmd_help:
        autodetected_version = None
        autodetected_path = None
        if not ipecmd_version and not ipecmd_path:
            autodetected_version, autodetected_path = autodetect_ipecmd()
        ipecmd_path_final = ipecmd_path if ipecmd_path else autodetected_path
        if not ipecmd_path_final:
            typer.echo("Error: Could not determine IPECMD path.", err=True)
            raise typer.Exit(1)
        import subprocess

        try:
            result = subprocess.run(
                [ipecmd_path_final, "-?"], capture_output=True, text=True
            )
            typer.echo(result.stdout)
            if result.stderr:
                typer.echo(result.stderr, err=True)
        except Exception as e:
            typer.echo(f"Error running IPECMD help: {e}", err=True)
            raise typer.Exit(1)
        raise typer.Exit()

    # Create args object compatible with existing core.program_pic function
    args = Args(
        part=part,
        tool=tool.value if tool else None,
        file=str(file) if file else None,
        power=str(power) if power is not None else None,
        memory=memory,
        verify=verify,
        erase=erase,
        logout=logout,
        vdd_first=vdd_first,
        test_programmer=test_programmer,
        ipecmd_version=ipecmd_version.value if ipecmd_version else autodetected_version,
        ipecmd_path=ipecmd_path if ipecmd_path else autodetected_path,
        passthrough=passthrough,
    )

    if passthrough:
        # Call the main programming function with error handling
        try:
            run_cmd_with_passthrough_option(args)
        except (ValueError, FileNotFoundError) as e:
            log.error(f"Error: {e}")
            raise typer.Exit(1) from e
        except Exception as e:
            log.error(f"Unexpected error: {e}")
            raise typer.Exit(1) from None
        raise typer.Exit()

    # Validate required positional arguments for normal operation
    if part is None or tool is None:
        typer.echo("Error: Missing required arguments: part and tool", err=True)
        raise typer.Exit(1)

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
