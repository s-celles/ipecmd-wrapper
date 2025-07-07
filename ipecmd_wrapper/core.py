"""
Core functionality for IPECMD wrapper

This module contains the main functions for interacting with MPLAB IPE's IPECMD tool.
"""

import os
import sys
import subprocess
from typing import Dict, List, Optional
from colorama import init, Fore, Style

# Initialize colorama for cross-platform support
init(autoreset=True)


def print_colored(text: str, color: str) -> None:
    """Print text with specified color using colorama"""
    print(f"{color}{text}{Style.RESET_ALL}")


# Color constants
class Colors:
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    GRAY = Fore.LIGHTBLACK_EX


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
VERSION_CHOICES = ["5.50", "6.20"]

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


def get_ipecmd_path(version: Optional[str] = None, custom_path: Optional[str] = None) -> str:
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
        return f"C:\\Program Files\\Microchip\\MPLABX\\v{version}\\mplab_platform\\mplab_ipe\\ipecmd.exe"
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
    if not os.path.exists(ipecmd_path):
        print_colored(f"✗ IPECMD not found: {ipecmd_path}", Colors.RED)
        if "custom path" in version_info:
            print_colored("Check the provided --ipecmd-path", Colors.YELLOW)
        else:
            print_colored(
                f"Install MPLAB X IDE {version_info} or use --ipecmd-path to specify custom location",
                Colors.YELLOW,
            )
        return False
    
    print_colored("✓ IPECMD found", Colors.GREEN)
    return True


def validate_hex_file(hex_file_path: str) -> bool:
    """
    Validate that HEX file exists
    
    Args:
        hex_file_path: Path to HEX file
        
    Returns:
        bool: True if HEX file exists, False otherwise
    """
    if not os.path.exists(hex_file_path):
        print_colored(f"✗ HEX file not found: {hex_file_path}", Colors.RED)
        print_colored("Compile first with: python compile.py", Colors.YELLOW)
        return False
    
    print_colored(f"✓ HEX file found: {hex_file_path}", Colors.GREEN)
    return True


def build_ipecmd_command(args, ipecmd_path: str) -> List[str]:
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
    cmd_args.append(f"-P{args.part}")
    
    # Add hex file
    cmd_args.append(f"-F{args.file}")
    
    # Add programming option
    if args.memory:
        cmd_args.append(f"-M{args.memory}")
    else:
        cmd_args.append("-M")  # Program entire device
    
    # Add verification option
    if args.verify:
        cmd_args.append(f"-Y{args.verify}")
    
    # Add power option
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


def test_programmer_detection(ipecmd_path: str, part: str, tool: str) -> bool:
    """
    Test programmer detection
    
    Args:
        ipecmd_path: Path to ipecmd.exe
        part: Target microcontroller part number
        tool: Programmer tool name
        
    Returns:
        bool: True if programmer detection successful, False otherwise
    """
    print_colored("\nTesting programmer detection...", Colors.YELLOW)
    tool_option = TOOL_MAP[tool]
    test_cmd = [ipecmd_path, f"-{tool_option}", f"-P{part}", "-OK"]
    print_colored(f'Command: "{ipecmd_path}" -{tool_option} -P{part} -OK', Colors.CYAN)
    
    try:
        result = subprocess.run(test_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print_colored("\n✗ Programmer detection failed!", Colors.RED)
            print_colored("Check programmer connection and try again", Colors.YELLOW)
            print_colored("STDERR:", Colors.RED)
            print(result.stderr)
            return False
        print_colored("✓ Programmer detection successful", Colors.GREEN)
        return True
    except Exception as e:
        print_colored(f"\n✗ Error running programmer detection: {e}", Colors.RED)
        return False


def execute_programming(cmd_args: List[str], part: str, tool: str, ipecmd_version: Optional[str]) -> bool:
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
    print_colored("\nAttempting to program...", Colors.YELLOW)
    cmd_str = f'"{cmd_args[0]}" ' + " ".join(cmd_args[1:])
    print_colored(f"Command: {cmd_str}", Colors.CYAN)
    
    try:
        result = subprocess.run(cmd_args, capture_output=True, text=True)
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        if result.returncode == 0:
            print_colored(f"\n🎉 SUCCESS! PIC {part} programmed!", Colors.GREEN)
            print_colored(
                "Your program should now be running on this PIC", Colors.WHITE
            )
            return True
        else:
            print_colored("\n✗ Programming error", Colors.RED)
            print_colored("Check connections and power supply", Colors.YELLOW)
            if ipecmd_version == "5.50":
                print_colored(
                    "You can also try with --ipecmd-version 6.20", Colors.CYAN
                )
            elif ipecmd_version == "6.20":
                print_colored(
                    "You can also try with --ipecmd-version 5.50", Colors.CYAN
                )
            return False
            
    except Exception as e:
        print_colored(f"\n✗ Error running programming command: {e}", Colors.RED)
        return False


def program_pic(args) -> None:
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
    
    # Validate HEX file
    if not validate_hex_file(args.file):
        sys.exit(1)
    
    # Validate IPECMD
    if not validate_ipecmd(ipecmd_path, version_info):
        sys.exit(1)
    
    # Display configuration
    print_colored("\nProgramming in progress...", Colors.YELLOW)
    print_colored("Make sure that:", Colors.BLUE)
    print_colored(f"  - {args.tool} is connected via USB", Colors.GRAY)
    print_colored(f"  - PIC {args.part} is in the socket", Colors.GRAY)
    print_colored(
        f"  - Circuit will be powered by {args.tool} (voltage: {args.power}V)", Colors.GRAY
    )
    
    # Test programmer detection if requested
    if args.test_programmer:
        if not test_programmer_detection(ipecmd_path, args.part, args.tool):
            sys.exit(1)
    
    # Build command
    cmd_args = build_ipecmd_command(args, ipecmd_path)
    
    # Execute programming
    if not execute_programming(cmd_args, args.part, args.tool, args.ipecmd_version):
        sys.exit(1)
