"""
Core functionality for IPECMD wrapper

This module contains the main functions for interacting with MPLAB IPE's IPECMD tool.
"""

import shlex
import re
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


def detect_latest_ipecmd_version() -> Optional[str]:
    """
    Auto-detect the latest installed MPLAB X IDE version
    
    Returns:
        str: Latest detected version (e.g., '6.20') or None if not found
    """
    import os
    
    log.info("Auto-detecting MPLAB X IDE version...")
    
    # Define base paths for different platforms
    if sys.platform == "win32":
        base_paths = [
            Path("C:/Program Files/Microchip/MPLABX"),
            Path("C:/Program Files (x86)/Microchip/MPLABX")
        ]
    elif sys.platform == "darwin":  # macOS
        base_paths = [Path("/Applications/microchip/mplabx")]
    else:  # Linux and other Unix systems
        base_paths = [Path("/opt/microchip/mplabx")]
    
    detected_versions = []
    
    for base_path in base_paths:
        if not base_path.exists():
            continue
            
        try:
            # Look for version directories (e.g., v6.20, v6.15, etc.)
            for item in base_path.iterdir():
                if item.is_dir() and item.name.startswith('v'):
                    version_str = item.name[1:]  # Remove 'v' prefix
                    
                    # Check if ipecmd exists in this version
                    if sys.platform == "win32":
                        ipecmd_path = item / "mplab_platform" / "mplab_ipe" / "ipecmd.exe"
                    else:
                        ipecmd_path = item / "mplab_platform" / "mplab_ipe" / "ipecmd"
                    
                    if ipecmd_path.exists():
                        detected_versions.append(version_str)
                        log.info(f"Found MPLAB X v{version_str}")
                        
        except (PermissionError, OSError) as e:
            log.debug(f"Could not scan {base_path}: {e}")
            continue
    
    if not detected_versions:
        log.warning("No MPLAB X IDE installations found")
        return None
    
    # Sort versions and return the latest
    # Convert to float for proper numeric sorting
    try:
        sorted_versions = sorted(detected_versions, key=float, reverse=True)
        latest_version = sorted_versions[0]
        log.info(f"Auto-detected latest MPLAB X version: v{latest_version}")
        return latest_version
    except ValueError:
        # Fallback: return the last one alphabetically
        latest_version = sorted(detected_versions)[-1]
        log.info(f"Auto-detected MPLAB X version: v{latest_version}")
        return latest_version


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
        ValueError: If no IPECMD installation can be found
    """
    if custom_path:
        return custom_path
    elif version:
        # Use specified version
        target_version = version
    else:
        # Auto-detect latest version
        target_version = detect_latest_ipecmd_version()
        if not target_version:
            raise ValueError(
                "No MPLAB X IDE installation found. "
                "Please install MPLAB X IDE or specify custom path with --ipecmd-path"
            )
    
    # Cross-platform path handling using pathlib
    if sys.platform == "win32":
        path = (
            Path("C:/Program Files/Microchip/MPLABX")
            / f"v{target_version}"
            / "mplab_platform"
            / "mplab_ipe"
            / "ipecmd.exe"
        )
    elif sys.platform == "darwin":  # macOS
        path = (
            Path("/Applications/microchip/mplabx")
            / f"v{target_version}"
            / "mplab_platform"
            / "mplab_ipe"
            / "ipecmd"
        )
    else:  # Linux and other Unix systems
        path = (
            Path("/opt/microchip/mplabx")
            / f"v{target_version}"
            / "mplab_platform"
            / "mplab_ipe"
            / "ipecmd"
        )

    return path.as_posix()


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


def is_safe_passthrough(passthrough: str) -> bool:
    # Reject dangerous shell metacharacters
    if re.search(r"[;&|`$><]", passthrough):
        return False
    # Optionally, add more checks or a whitelist
    return True


def run_cmd_with_passthrough_option(args: Any) -> None:
    """
    Main function to run a passthrough command
    """
    log.info("Running command...")

    cmd_args = [args.ipecmd_path]

    if not is_safe_passthrough(args.passthrough):
        log.error("Unsafe passthrough argument detected!")
        raise ValueError("Unsafe passthrough argument")

    # Split passthrough string into arguments, respecting quotes
    passthrough_args = shlex.split(args.passthrough)

    cmd_args.extend(passthrough_args)

    log.info(f"Command: {cmd_args}")
    try:
        result = subprocess.run(cmd_args, capture_output=True, text=True)  # nosec B603
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except Exception as e:
        log.error(f"Error running programmer detection: {e}")


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
    detected_version = None
    
    if args.ipecmd_path:
        ipecmd_path = args.ipecmd_path
        version_info = "custom path"
    else:
        # Get the path and potentially detect version
        if args.ipecmd_version:
            ipecmd_path = get_ipecmd_path(version=args.ipecmd_version)
            version_info = f"v{args.ipecmd_version}"
        else:
            # Auto-detect latest version
            detected_version = detect_latest_ipecmd_version()
            if detected_version:
                ipecmd_path = get_ipecmd_path(version=detected_version)
                version_info = f"v{detected_version} (auto-detected)"
                log.info(f"Auto-detected MPLAB X v{detected_version}")
            else:
                log.error("Could not auto-detect MPLAB X installation")
                sys.exit(1)

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
    version_for_errors = detected_version or args.ipecmd_version
    if not execute_programming(cmd_args, args.part, args.tool, version_for_errors):
        sys.exit(1)
