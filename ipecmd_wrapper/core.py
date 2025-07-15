"""
Core functionality for IPECMD wrapper

This module contains the main functions for interacting with MPLAB IPE's IPECMD tool.
"""

import subprocess  # nosec B404
import sys
from pathlib import Path
from typing import Any, Optional

from .logger import log

# Available tool choices
TOOL_CHOICES = [
    "PK3",
    "PK4",
    "PK5",
    "ICD3",
    "ICD4",
    "ICD5",
    "ICE4",
    "RICE",
    "SNAP",
    "PM3",
    "PKOB",
    "PKOB4",
    "J32",
]

# Available version choices
VERSION_CHOICES = ["5.50", "6.00", "6.05", "6.10", "6.15", "6.20", "6.25"]

# Map of tool names to IPECMD options
TOOL_MAP = {
    "PK3": "TPPK3",
    "PK4": "TPPK4",
    "PK5": "TPPK5",
    "ICD3": "TPICD3",
    "ICD4": "TPICD4",
    "ICD5": "TPICD5",
    "ICE4": "TPICE4",
    "RICE": "TPRICE",
    "SNAP": "TPSNAP",
    "PM3": "TPPM3",
    "PKOB": "TPPKOB",
    "PKOB4": "TPPKOB4",
    "J32": "TPJ32",
}


def get_ipecmd_path(
    version: Optional[str] = None, custom_path: Optional[str] = None
) -> str:
    """
    Get the path to IPECMD executable

    Args:
        version: MPLAB X IDE version string (e.g., '6.20')
        custom_path: Custom path to ipecmd.exe

    Returns:
        str: Path to ipecmd.exe

    Raises:
        ValueError: If neither version nor custom_path is provided
    """
    if custom_path:
        return custom_path
    elif version:
        # Cross-platform path handling using pathlib
        if sys.platform == "win32":
            path = (
                Path("C:/Program Files/Microchip/MPLABX")
                / f"v{version}"
                / "mplab_platform"
                / "mplab_ipe"
                / "ipecmd.exe"
            )
        elif sys.platform == "darwin":  # macOS
            path = (
                Path("/Applications/microchip/mplabx")
                / f"v{version}"
                / "mplab_platform"
                / "mplab_ipe"
                / "ipecmd"
            )
        else:  # Linux and other Unix systems
            path = (
                Path("/opt/microchip/mplabx")
                / f"v{version}"
                / "mplab_platform"
                / "mplab_ipe"
                / "ipecmd"
            )

        return path.as_posix()
    else:
        raise ValueError("Either version or custom_path must be provided")


def validate_ipecmd(ipecmd_path: str, version_info: str) -> bool:
    """
    Validate that IPECMD exists and is accessible

    Args:
        ipecmd_path: Path to ipecmd.exe
        version_info: Version information string for error messages

    Returns:
        bool: True if IPECMD is valid, False otherwise
    """
    path = Path(ipecmd_path)
    if not path.exists():
        log.error(f"IPECMD not found: {ipecmd_path}")
        if "custom path" in version_info:
            log.warning("Check the provided --ipecmd-path")
        else:
            log.warning(
                f"Install MPLAB X IDE {version_info} or use --ipecmd-path "
                f"to specify custom location"
            )
        return False

    log.info("IPECMD found")
    return True


def validate_hex_file(hex_file_path: str) -> bool:
    """
    Validate that HEX file exists

    Args:
        hex_file_path: Path to HEX file

    Returns:
        bool: True if HEX file exists, False otherwise
    """
    path = Path(hex_file_path)
    if not path.exists():
        log.error(f"HEX file not found: {hex_file_path}")
        log.warning("Compile first with: python compile.py")
        return False

    log.info(f"HEX file found: {hex_file_path}")
    return True


def build_ipecmd_command(args: Any, ipecmd_path: str) -> list[str]:
    """
    Build IPECMD command arguments

    Args:
        args: Parsed command line arguments
        ipecmd_path: Path to ipecmd.exe

    Returns:
        List[str]: Command arguments for IPECMD
    """
    # Get tool mapping
    tool_option = TOOL_MAP[args.tool]

    # Build command arguments
    cmd_args = [ipecmd_path]

    # Add tool selection
    cmd_args.append(f"-{tool_option}")

    # Add part selection
    if args.part[:3] == "PIC":
        cmd_args.append(f"-P{args.part[3:]}")
    else:
        cmd_args.append(f"-P{args.part}")

    # Add hex file (if provided)
    if args.file:
        cmd_args.append(f"-F{args.file}")

    # Add programming option
    if args.memory:
        cmd_args.append(f"-M{args.memory}")
    else:
        cmd_args.append("-M")  # Program entire device

    # Add verification option
    if args.verify:
        cmd_args.append(f"-Y{args.verify}")

    # Add power option (if provided)
    if args.power:
        cmd_args.append(f"-W{args.power}")

    # Add erase option
    if args.erase:
        cmd_args.append("-E")

    # Add VDD first option
    if args.vdd_first:
        cmd_args.append("-OD")

    # Add logout option
    if args.logout:
        cmd_args.append("-OL")

    # Add passthrough options
    if args.passthrough:
        # Split passthrough string into arguments, respecting quotes
        import shlex

        passthrough_args = shlex.split(args.passthrough)
        cmd_args.extend(passthrough_args)

    return cmd_args


def detect_programmer(ipecmd_path: str, part: str, tool: str) -> bool:
    """
    Test programmer detection

    Args:
        ipecmd_path: Path to ipecmd.exe
        part: Target microcontroller part number
        tool: Programmer tool name

    Returns:
        bool: True if programmer detection successful, False otherwise
    """
    log.warning("Testing programmer detection...")
    tool_option = TOOL_MAP[tool]
    test_cmd = [ipecmd_path, f"-{tool_option}", f"-P{part}", "-OK"]
    log.info(f'Command: "{ipecmd_path}" -{tool_option} -P{part} -OK')

    try:
        result = subprocess.run(test_cmd, capture_output=True, text=True)  # nosec B603
        if result.returncode != 0:
            log.error("Programmer detection failed!")
            log.warning("Check programmer connection and try again")
            log.error(f"STDERR: {result.stderr}")
            return False
        log.info("Programmer detection successful")
        return True
    except Exception as e:
        log.error(f"Error running programmer detection: {e}")
        return False


def _get_version_suggestions(current_version: str) -> list[str]:
    """
    Get alternative version suggestions for troubleshooting

    Args:
        current_version: Current MPLAB X IDE version being used

    Returns:
        List of suggested alternative versions (max 2)
    """
    if current_version not in VERSION_CHOICES:
        return []

    current_index = VERSION_CHOICES.index(current_version)
    suggestions = []

    # Suggest the latest version if not already using it
    if current_version != VERSION_CHOICES[-1]:
        suggestions.append(VERSION_CHOICES[-1])

    # Suggest previous version if available and not already suggested
    if current_index > 0 and VERSION_CHOICES[current_index - 1] not in suggestions:
        suggestions.append(VERSION_CHOICES[current_index - 1])

    # Suggest next version if available and not already suggested
    if (
        current_index < len(VERSION_CHOICES) - 1
        and VERSION_CHOICES[current_index + 1] not in suggestions
    ):
        suggestions.append(VERSION_CHOICES[current_index + 1])

    return suggestions[:2]  # Limit to 2 suggestions


def execute_programming(
    cmd_args: list[str], part: str, tool: str, ipecmd_version: Optional[str]
) -> bool:
    """
    Execute the programming command

    Args:
        cmd_args: Command arguments for IPECMD
        part: Target microcontroller part number
        tool: Programmer tool name
        ipecmd_version: IPECMD version for error suggestions

    Returns:
        bool: True if programming successful, False otherwise
    """
    log.warning("Attempting to program...")
    cmd_str = f'"{cmd_args[0]}" ' + " ".join(cmd_args[1:])
    log.info(f"Command: {cmd_str}")

    try:
        result = subprocess.run(cmd_args, capture_output=True, text=True)  # nosec B603

        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

        if result.returncode == 0:
            log.info(f"SUCCESS! PIC {part} programmed!")
            log.info("Your program should now be running on this PIC")
            return True
        else:
            log.error("Programming error")
            log.warning("Check connections and power supply")

            # Suggest alternative versions based on current version
            if ipecmd_version:
                suggestions = _get_version_suggestions(ipecmd_version)
                for suggestion in suggestions:
                    log.info(f"You can also try with --ipecmd-version {suggestion}")
            return False

    except Exception as e:
        log.error(f"Error running programming command: {e}")
        return False


def program_pic(args: Any) -> None:
    """
    Main function to program PIC microcontroller

    Args:
        args: Parsed command line arguments

    Raises:
        SystemExit: If programming fails or requirements are not met
    """
    # Determine IPECMD path
    version_info = ""
    if args.ipecmd_path:
        ipecmd_path = args.ipecmd_path
        version_info = "custom path"
    else:
        ipecmd_path = get_ipecmd_path(version=args.ipecmd_version)
        version_info = f"v{args.ipecmd_version}"

    # Validate HEX file (if provided)
    if args.file and not validate_hex_file(args.file):
        sys.exit(1)

    # Validate IPECMD
    if not validate_ipecmd(ipecmd_path, version_info):
        sys.exit(1)

    # Display configuration
    log.warning("Programming in progress...")
    log.info("Make sure that:")
    log.info(f"  - {args.tool} is connected via USB")
    log.info(f"  - PIC {args.part} is in the socket")
    log.info(f"  - Circuit will be powered by {args.tool} (voltage: {args.power}V)")

    # Test programmer detection if requested
    if args.test_programmer:
        if not detect_programmer(ipecmd_path, args.part, args.tool):
            sys.exit(1)

    # Build command
    cmd_args = build_ipecmd_command(args, ipecmd_path)

    # Execute programming
    if not execute_programming(cmd_args, args.part, args.tool, args.ipecmd_version):
        sys.exit(1)
