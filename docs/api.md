# Python API Reference

Complete reference for the IPECMD Wrapper Python API.

## Core Functions

### `upload_firmware(hex_file, device, programmer, **kwargs)`

Upload firmware to a PIC microcontroller.

**Parameters:**
- `hex_file` (str): Path to Intel HEX file
- `device` (str): Target device name (e.g., "PIC16F876A")
- `programmer` (str): Programmer type (e.g., "pickit3")
- `**kwargs`: Additional options

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
from ipecmd_wrapper import upload_firmware

success = upload_firmware(
    hex_file="firmware.hex",
    device="PIC16F876A",
    programmer="pickit3"
)
```

### `program_pic(**kwargs)`

Program a PIC microcontroller with detailed options.

**Parameters:**
- `part` (str): Target device
- `tool` (str): Programmer type
- `file` (str): HEX file path
- `power` (float): Target voltage
- `erase` (bool): Erase before programming
- `verify` (str): Verification type ("P" or "E")
- `memory` (str): Memory type ("P" or "E")
- `ipecmd_path` (str): Custom IPECMD path
- `ipecmd_version` (str): IPECMD version

**Returns:**
- `None`: Raises exception on error

**Example:**
```python
from ipecmd_wrapper.core import program_pic

program_pic(
    part="PIC16F876A",
    tool="PK3",
    file="firmware.hex",
    power=5.0,
    erase=True,
    verify="P"
)
```

## Utility Functions

### `get_ipecmd_path(version=None, custom_path=None)`

Get the path to IPECMD executable.

**Parameters:**
- `version` (str, optional): IPECMD version
- `custom_path` (str, optional): Custom path override

**Returns:**
- `str`: Path to IPECMD executable

**Example:**
```python
from ipecmd_wrapper.core import get_ipecmd_path

path = get_ipecmd_path(version="6.20")
print(f"IPECMD path: {path}")
```

### `validate_ipecmd(ipecmd_path, version_info)`

Validate IPECMD installation.

**Parameters:**
- `ipecmd_path` (str): Path to IPECMD executable
- `version_info` (str): Expected version information

**Returns:**
- `bool`: True if valid, False otherwise

**Example:**
```python
from ipecmd_wrapper.core import validate_ipecmd

is_valid = validate_ipecmd(
    "C:\\Program Files\\Microchip\\MPLABX\\v6.20\\mplab_platform\\mplab_ipe\\ipecmd.exe",
    "6.20"
)
```

### `validate_hex_file(hex_file_path)`

Validate Intel HEX file.

**Parameters:**
- `hex_file_path` (str): Path to HEX file

**Returns:**
- `bool`: True if valid, False otherwise

**Example:**
```python
from ipecmd_wrapper.core import validate_hex_file

is_valid = validate_hex_file("firmware.hex")
if not is_valid:
    print("Invalid HEX file")
```

### `build_ipecmd_command(**kwargs)`

Build IPECMD command line arguments.

**Parameters:**
- Various command options as keyword arguments

**Returns:**
- `list`: Command line arguments

**Example:**
```python
from ipecmd_wrapper.core import build_ipecmd_command

cmd = build_ipecmd_command(
    part="PIC16F876A",
    tool="PK3",
    file="firmware.hex",
    power=5.0
)
print(f"Command: {' '.join(cmd)}")
```

### `test_programmer_detection(ipecmd_path, part, tool)`

Test programmer detection.

**Parameters:**
- `ipecmd_path` (str): Path to IPECMD
- `part` (str): Target device
- `tool` (str): Programmer type

**Returns:**
- `bool`: True if programmer detected, False otherwise

**Example:**
```python
from ipecmd_wrapper.core import test_programmer_detection

detected = test_programmer_detection(
    ipecmd_path="ipecmd.exe",
    part="PIC16F876A",
    tool="PK3"
)
```

## Constants

### `TOOL_CHOICES`

List of supported programmer types:
```python
from ipecmd_wrapper.core import TOOL_CHOICES

print(TOOL_CHOICES)
# ['PK3', 'PK4', 'PK5', 'ICD3', 'ICD4', 'ICD5', 'ICE4', 'RICE', 'SNAP', 'PM3', 'PKOB', 'PKOB4', 'J32']
```

### `VERSION_CHOICES`

List of supported IPECMD versions:
```python
from ipecmd_wrapper.core import VERSION_CHOICES

print(VERSION_CHOICES)
# ['5.50', '6.20']
```

### `TOOL_MAP`

Mapping of tool names to IPECMD identifiers:
```python
from ipecmd_wrapper.core import TOOL_MAP

print(TOOL_MAP['PK3'])  # PICkit 3 identifier
```

## CLI Functions

### `create_argument_parser()`

Create command-line argument parser.

**Returns:**
- `argparse.ArgumentParser`: Configured parser

**Example:**
```python
from ipecmd_wrapper.cli import create_argument_parser

parser = create_argument_parser()
args = parser.parse_args(["-P", "PIC16F876A", "-T", "PK3", "-F", "firmware.hex", "-W", "5.0"])
```

### `main(args=None)`

Main entry point for CLI.

**Parameters:**
- `args` (list, optional): Command line arguments

**Returns:**
- `None`: Exits with appropriate code

**Example:**
```python
from ipecmd_wrapper.cli import main

# Run with custom arguments
main(["-P", "PIC16F876A", "-T", "PK3", "-F", "firmware.hex", "-W", "5.0"])
```

## Exception Handling

The API raises various exceptions for different error conditions:

```python
try:
    upload_firmware("firmware.hex", "PIC16F876A", "pickit3")
except FileNotFoundError:
    print("HEX file not found")
except RuntimeError as e:
    print(f"Programming failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Configuration

### Environment Variables

You can set environment variables to configure defaults:

```python
import os

# Set default IPECMD path
os.environ['IPECMD_PATH'] = '/custom/path/to/ipecmd'

# Set default programmer
os.environ['PIC_PROGRAMMER'] = 'PK4'

# Now use the API
from ipecmd_wrapper import upload_firmware
upload_firmware("firmware.hex", "PIC16F876A", "pickit4")
```

## Advanced Usage

### Custom IPECMD Commands

For advanced users who need custom IPECMD commands:

```python
import subprocess
from ipecmd_wrapper.core import get_ipecmd_path

ipecmd_path = get_ipecmd_path()
custom_cmd = [ipecmd_path, "-P", "PIC16F876A", "-TP", "-M", "P"]

result = subprocess.run(custom_cmd, capture_output=True, text=True)
print(result.stdout)
```

### Batch Programming

Program multiple devices:

```python
from ipecmd_wrapper import upload_firmware

devices = ["PIC16F876A", "PIC16F877A", "PIC18F4550"]
hex_files = ["firmware1.hex", "firmware2.hex", "firmware3.hex"]

for device, hex_file in zip(devices, hex_files):
    success = upload_firmware(hex_file, device, "pickit3")
    print(f"{device}: {'Success' if success else 'Failed'}")
```
