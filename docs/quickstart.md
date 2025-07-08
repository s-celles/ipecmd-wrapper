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
ipecmd-wrapper --part PIC16F876A --tool PK3 --file firmware.hex --power 5.0
```

### 3️⃣ Verify Programming

```bash
ipecmd-wrapper --part PIC16F876A --tool PK3 --file firmware.hex --power 5.0 --verify P
```

## Command Line Options

- `--part` / `-P`: Target device (e.g., PIC16F876A)
- `--tool` / `-T`: Programmer type (PK3, PK4, ICD3, etc.)
- `--file` / `-F`: Hex file to program
- `--power` / `-W`: Target power voltage (e.g., 5.0, 3.3)
- `--verify` / `-Y`: Verify programming (P for program memory)
- `--erase` / `-E`: Erase device before programming
- `--memory` / `-M`: Memory type (P for program, E for EEPROM)

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
ipecmd-wrapper --part PIC16F876A --tool PK3 --file firmware.hex --power 5.0 --erase --verify P
```

### Test Programmer Connection

```bash
ipecmd-wrapper --part PIC16F876A --tool PK3 --power 5.0 --test-programmer
```

### Use Custom IPECMD Path

```bash
ipecmd-wrapper --part PIC16F876A --tool PK3 --file firmware.hex --power 5.0 --ipecmd-path "C:\custom\path\ipecmd.exe"
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
