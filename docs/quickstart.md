# 🚀 Quick Start Guide

This guide will help you get started with IPECMD Wrapper quickly.

## 📋 Prerequisites

- 🐍 Python 3.9+
- 🔧 IPECMD installed (comes with MPLAB X IDE)
- 📱 PIC programmer hardware (PICkit 3, PICkit 4, etc.)
- 📄 Compiled hex file for your PIC microcontroller

## 🎯 Basic Usage

### 1️⃣ Install IPECMD Wrapper

```bash
pip install ipecmd-wrapper
```

### 2️⃣ Program a PIC Microcontroller

```bash
ipecmd-wrapper PIC16F876A PK3 --file firmware.hex --power 5.0 --ipecmd-version 6.20
```

### 3️⃣ Verify Programming

```bash
ipecmd-wrapper PIC16F876A PK3 --file firmware.hex --power 5.0 --verify P --ipecmd-version 6.20
```

## 🎨 Modern CLI Features

The new Typer-powered CLI provides:

- ✅ **Rich Help Output**: Beautiful, organized help with syntax highlighting
- 🔍 **Input Validation**: Automatic validation of tool choices, file paths, and versions
- 🎯 **Clear Error Messages**: Helpful error messages with suggestions
- 📝 **Required vs Optional**: Clear distinction between required and optional arguments

### Get Help

```bash
# See beautiful, organized help
ipecmd-wrapper --help
```

## Command Line Options

### Required Arguments

- `PART`: Target device (e.g., PIC16F876A) - **positional argument**
- `TOOL`: Programmer type (PK3, PK4, ICD3, etc.) - **positional argument with validated choices**

### Required Options

- `--file` / `-F`: Hex file to program - **automatically validates file exists**
- `--power` / `-W`: Target power voltage (e.g., 5.0, 3.3)

### Optional Options

- `--ipecmd-version`: MPLAB IPE version - **validated choices** (5.50, 6.00, 6.05, 6.10, 6.15, 6.20, 6.25)
- `--ipecmd-path`: Custom path to ipecmd.exe (overrides version)
- `--verify` / `-Y`: Verify programming (P for program memory, E for EEPROM)
- `--erase` / `-E`: Erase device before programming
- `--memory` / `-M`: Memory type (P for program, E for EEPROM)
- `--test-programmer`: Test programmer connection only
- `--vdd-first` / `-OD`: Use VDD-first programming sequence
- `--logout` / `-OL`: Release from reset after programming

## ✨ Input Validation Examples

### Valid Commands
```bash
# ✅ Valid tool choice
ipecmd-wrapper PIC16F876A PK4 --file firmware.hex --power 5.0

# ✅ Valid version choice
ipecmd-wrapper PIC16F876A PK3 --file firmware.hex --power 5.0 --ipecmd-version 6.20
```

### Invalid Commands (with helpful errors)
```bash
# ❌ Invalid tool choice
ipecmd-wrapper PIC16F876A INVALID --file firmware.hex --power 5.0
# Error: Invalid value for 'TOOL': 'INVALID' is not one of 'PK3', 'PK4', 'PK5', ...

# ❌ Missing file
ipecmd-wrapper PIC16F876A PK3 --file missing.hex --power 5.0
# Error: Invalid value for '--file' / '-F': Path 'missing.hex' does not exist.
```

## Python API

### Basic Programming

```python
from ipecmd_wrapper import upload_firmware

success = upload_firmware(
    hex_file="firmware.hex",
    device="PIC16F876A",
    programmer="pickit3"
)

if success:
    print("Programming successful!")
else:
    print("Programming failed!")
```

### Advanced Usage

```python
from ipecmd_wrapper.core import program_pic

# Program with custom options
program_pic(
    part="PIC16F876A",
    tool="PK3",
    file="firmware.hex",
    power=5.0,
    erase=True,
    verify="P",
    memory="P"
)
```

## Common Examples

### Program and Verify

```bash
ipecmd-wrapper PIC16F876A PK3 --file firmware.hex --power 5.0 --erase --verify P
```

### Test Programmer Connection

```bash
ipecmd-wrapper PIC16F876A PK3 --power 5.0 --test-programmer
```

### Use Custom IPECMD Path

```bash
ipecmd-wrapper PIC16F876A PK3 --file firmware.hex --power 5.0 --ipecmd-path "C:\custom\path\ipecmd.exe"
```

## Troubleshooting

### Device Not Found

- Check programmer connection
- Verify target device is powered
- Ensure correct device name

### Programming Failed

- Check hex file exists and is valid
- Verify target voltage matches device requirements
- Try erasing device first with `--erase`

### Permission Denied

- Run as administrator (Windows)
- Check user permissions for USB devices (Linux/macOS)

## Next Steps

- Read the [Command Line Reference](cli.md) for all available options
- Check the [Python API Reference](api.md) for programmatic usage
- See [Examples](examples.md) for more use cases
