# Examples

This page provides practical examples of using IPECMD Wrapper in various scenarios.

## Basic Programming Examples

### Simple Programming

```bash
# Program a PIC16F876A with firmware.hex
ipecmd-wrapper --part PIC16F876A --tool PK3 --file firmware.hex --power 5.0
```

### Programming with Verification

```bash
# Program and verify
ipecmd-wrapper --part PIC16F876A --tool PK3 --file firmware.hex --power 5.0 --erase --verify P
```

### Programming EEPROM

```bash
# Program EEPROM data
ipecmd-wrapper --part PIC16F876A --tool PK3 --file eeprom_data.hex --power 5.0 --memory E
```

## Python API Examples

### Basic Upload

```python
from ipecmd_wrapper import upload_firmware

# Simple upload
success = upload_firmware(
    hex_file="dist/firmware.hex",
    device="PIC16F876A",
    programmer="pickit3"
)

if success:
    print("✅ Programming successful!")
else:
    print("❌ Programming failed!")
```

### Advanced Programming

```python
from ipecmd_wrapper.core import program_pic

try:
    program_pic(
        part="PIC16F876A",
        tool="PK3",
        file="dist/firmware.hex",
        power=5.0,
        erase=True,
        verify="P",
        memory="P"
    )
    print("✅ Programming and verification successful!")
except Exception as e:
    print(f"❌ Error: {e}")
```

### Batch Programming

```python
from ipecmd_wrapper import upload_firmware
import os

# Program multiple devices
devices = [
    {"hex": "firmware_16f876a.hex", "device": "PIC16F876A"},
    {"hex": "firmware_18f4550.hex", "device": "PIC18F4550"},
    {"hex": "firmware_16f628a.hex", "device": "PIC16F628A"},
]

for config in devices:
    if os.path.exists(config["hex"]):
        success = upload_firmware(
            hex_file=config["hex"],
            device=config["device"],
            programmer="pickit3"
        )
        print(f"{config['device']}: {'✅ Success' if success else '❌ Failed'}")
    else:
        print(f"{config['device']}: ❌ HEX file not found")
```

## Build System Integration

### Makefile Integration

```makefile
# Makefile for PIC project
DEVICE = PIC16F876A
PROGRAMMER = PK3
POWER = 5.0

compile:
    xc8-cc main.c -mcpu=$(DEVICE) -o firmware.hex

program: compile
    ipecmd-wrapper --part $(DEVICE) --tool $(PROGRAMMER) --file firmware.hex --power $(POWER) --erase --verify P

clean:
    rm -f *.hex *.obj *.lst
```

### Python Build Script

```python
#!/usr/bin/env python3
"""
Build and program script for PIC project
"""

import subprocess
import sys
from pathlib import Path
from ipecmd_wrapper import upload_firmware

def compile_project():
    """Compile the project using XC8"""
    cmd = [
        "xc8-cc", "main.c",
        "-mcpu=PIC16F876A",
        "-o", "firmware.hex"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Compilation failed: {result.stderr}")
        return False

    print("✅ Compilation successful!")
    return True

def program_device():
    """Program the device"""
    if not Path("firmware.hex").exists():
        print("❌ firmware.hex not found. Compile first.")
        return False

    success = upload_firmware(
        hex_file="firmware.hex",
        device="PIC16F876A",
        programmer="pickit3"
    )

    if success:
        print("✅ Programming successful!")
    else:
        print("❌ Programming failed!")

    return success

def main():
    """Main build and program workflow"""
    if len(sys.argv) > 1 and sys.argv[1] == "program-only":
        success = program_device()
    else:
        success = compile_project() and program_device()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
```

## CI/CD Examples

### GitHub Actions

```yaml
name: Build and Test PIC Firmware

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install XC8 and IPECMD
      run: |
        # Install MPLAB X and XC8 (simulation)
        echo "Installing development tools..."

    - name: Install IPECMD Wrapper
      run: pip install ipecmd-wrapper

    - name: Compile firmware
      run: |
        xc8-cc main.c -mcpu=PIC16F876A -o firmware.hex

    - name: Validate HEX file
      run: |
        python -c "
        from ipecmd_wrapper.core import validate_hex_file
        assert validate_hex_file('firmware.hex'), 'Invalid HEX file'
        print('✅ HEX file validation passed')
        "

    - name: Upload firmware artifact
      uses: actions/upload-artifact@v4
      with:
        name: firmware
        path: firmware.hex
```

## Error Handling Examples

### Robust Programming

```python
from ipecmd_wrapper.core import program_pic, validate_hex_file, validate_ipecmd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def robust_program(hex_file, device, programmer):
    """Program device with comprehensive error handling"""

    # Validate inputs
    if not validate_hex_file(hex_file):
        logger.error(f"Invalid HEX file: {hex_file}")
        return False

    # Get IPECMD path and validate
    from ipecmd_wrapper.core import get_ipecmd_path
    ipecmd_path = get_ipecmd_path()

    if not validate_ipecmd(ipecmd_path, "6.20"):
        logger.error("IPECMD validation failed")
        return False

    # Attempt programming with retries
    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info(f"Programming attempt {attempt + 1}/{max_retries}")

            program_pic(
                part=device,
                tool=programmer,
                file=hex_file,
                power=5.0,
                erase=True,
                verify="P"
            )

            logger.info("✅ Programming successful!")
            return True

        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                logger.error("❌ All programming attempts failed")
                return False

    return False

# Usage
success = robust_program("firmware.hex", "PIC16F876A", "PK3")
```

## Configuration Examples

### Project Configuration File

Create `.ipecmd-wrapper.json` in your project:

```json
{
    "device": "PIC16F876A",
    "programmer": "PK3",
    "power": 5.0,
    "ipecmd_version": "6.20",
    "default_options": {
        "erase": true,
        "verify": "P",
        "preserve_eeprom": false
    },
    "hex_files": {
        "main": "dist/firmware.hex",
        "bootloader": "dist/bootloader.hex",
        "eeprom": "dist/eeprom_data.hex"
    }
}
```

### Using Configuration

```python
import json
from ipecmd_wrapper.core import program_pic

# Load project configuration
with open('.ipecmd-wrapper.json', 'r') as f:
    config = json.load(f)

# Program main firmware
program_pic(
    part=config["device"],
    tool=config["programmer"],
    file=config["hex_files"]["main"],
    power=config["power"],
    **config["default_options"]
)
```

## Testing Examples

### Automated Testing

```python
import unittest
from unittest.mock import patch, MagicMock
from ipecmd_wrapper.core import program_pic

class TestProgramming(unittest.TestCase):

    @patch('ipecmd_wrapper.core.subprocess.run')
    def test_successful_programming(self, mock_run):
        """Test successful programming scenario"""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        # Should not raise exception
        try:
            program_pic(
                part="PIC16F876A",
                tool="PK3",
                file="test.hex",
                power=5.0
            )
        except Exception as e:
            self.fail(f"Programming should succeed: {e}")

    @patch('ipecmd_wrapper.core.subprocess.run')
    def test_programming_failure(self, mock_run):
        """Test programming failure scenario"""
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="Error")

        # Should raise exception
        with self.assertRaises(RuntimeError):
            program_pic(
                part="PIC16F876A",
                tool="PK3",
                file="test.hex",
                power=5.0
            )

if __name__ == '__main__':
    unittest.main()
```

## Platform-Specific Examples

### Windows Batch Script

```batch
@echo off
REM Build and program PIC firmware on Windows

echo Building firmware...
xc8-cc main.c -mcpu=PIC16F876A -o firmware.hex

if %errorlevel% neq 0 (
    echo Compilation failed!
    exit /b 1
)

echo Programming device...
ipecmd-wrapper --part PIC16F876A --tool PK3 --file firmware.hex --power 5.0 --erase --verify P

if %errorlevel% neq 0 (
    echo Programming failed!
    exit /b 1
)

echo Build and programming completed successfully!
```

### Linux Shell Script

```bash
#!/bin/bash
# Build and program PIC firmware on Linux

set -e  # Exit on any error

echo "Building firmware..."
xc8-cc main.c -mcpu=PIC16F876A -o firmware.hex

echo "Programming device..."
ipecmd-wrapper --part PIC16F876A --tool PK3 --file firmware.hex --power 5.0 --erase --verify P

echo "✅ Build and programming completed successfully!"
```

These examples demonstrate various ways to integrate IPECMD Wrapper into your development workflow, from simple command-line usage to complex CI/CD pipelines.
