# Command Line Reference

Complete reference for the IPECMD Wrapper command-line interface.

## Synopsis

```bash
ipecmd-wrapper [OPTIONS]
```

The IPECMD Wrapper now features a modern, rich command-line interface powered by Typer, providing enhanced validation, beautiful help output, and improved user experience.

## Required Arguments

All required arguments must be provided for the command to execute successfully.

### `--part`, `-P` DEVICE
Target PIC microcontroller device.

**Type:** TEXT
**Required:** Yes

**Example:**
```bash
ipecmd-wrapper --part PIC16F876A ...
```

### `--tool`, `-T` PROGRAMMER
Programmer type. The tool choice is validated against supported programmers.

**Type:** Enum (validated choices)
**Required:** Yes

**Supported Options:**
- `PK3` - PICkit 3
- `PK4` - PICkit 4
- `PK5` - PICkit 5
- `ICD3` - MPLAB ICD 3
- `ICD4` - MPLAB ICD 4
- `ICD5` - MPLAB ICD 5
- `ICE4` - MPLAB ICE 4
- `RICE` - MPLAB REAL ICE
- `SNAP` - MPLAB SNAP
- `PM3` - MPLAB PM3
- `PKOB` - PICkit On Board
- `PKOB4` - PICkit 4 On Board
- `J32` - MPLAB J32

**Example:**
```bash
ipecmd-wrapper --tool PK4 ...
```

### `--file`, `-F` HEXFILE
Intel HEX file to program. The file path is validated to ensure it exists.

**Type:** PATH (automatically validated)
**Required:** Yes

**Example:**
```bash
ipecmd-wrapper --file firmware.hex ...
```

### `--power`, `-W` VOLTAGE
Target power voltage (VDD voltage from tool).

**Type:** TEXT
**Required:** Yes

**Example:**
```bash
ipecmd-wrapper --power 5.0 ...
# or
ipecmd-wrapper --power 3.3 ...
```

## Optional Arguments

### `--memory`, `-M` TYPE
Program Device memory regions.

**Type:** TEXT
**Options:**
- `P` - Program memory (default)
- `E` - EEPROM memory
- `I` - ID memory
- `C` - Configuration memory
- `B` - Boot memory
- `A` - Auxiliary memory

### `--verify`, `-Y` TYPE
Verify Device memory regions after programming.

**Type:** TEXT
**Options:**
- `P` - Verify program memory
- `E` - Verify EEPROM memory
- `I` - Verify ID memory
- `C` - Verify configuration memory
- `B` - Verify boot memory
- `A` - Verify auxiliary memory

### `--erase`, `-E`
Erase Flash Device before programming.

**Type:** Flag (no value required)

### `--logout`, `-OL`
Release from Reset after programming.

**Type:** Flag (no value required)

### `--vdd-first`, `-OD`
VDD First programming sequence (default is VPP First).

**Type:** Flag (no value required)

### `--test-programmer`
Test programmer detection before programming without actually programming the device.

**Type:** Flag (no value required)

### `--ipecmd-version` VERSION
Specify MPLAB IPE version to use. This option is ignored if `--ipecmd-path` is provided.

**Type:** Enum (validated choices)
**Supported Versions:**
- `5.50`
- `6.00`
- `6.05`
- `6.10`
- `6.15`
- `6.20`
- `6.25`

### `--ipecmd-path` PATH
Full path to ipecmd.exe. This overrides `--ipecmd-version` when provided.

**Type:** TEXT

### `--version`
Show version information and exit.

**Type:** Flag

### `--help`
Show help message and exit.

## Examples

### Basic Programming

Program a PIC16F876A with firmware.hex using PICkit 3:

```bash
ipecmd-wrapper --part PIC16F876A --tool PK3 --file firmware.hex --power 5.0 --ipecmd-version 6.20
```

### Program with Erase and Verify

Erase the device, program it, and verify the program memory:

```bash
ipecmd-wrapper --part PIC16F876A --tool PK4 --file firmware.hex --power 5.0 --erase --verify P --ipecmd-version 6.20
```

### Test Programmer Connection

Test if the programmer is properly connected without programming:

```bash
ipecmd-wrapper --part PIC16F876A --tool PK4 --file firmware.hex --power 5.0 --test-programmer
```

### Program EEPROM Memory

Program only EEPROM memory:

```bash
ipecmd-wrapper --part PIC16F876A --tool PK3 --file eeprom_data.hex --power 5.0 --memory E --ipecmd-version 6.20
```

### Use Custom IPECMD Path

Use a custom installation path for ipecmd.exe:

```bash
ipecmd-wrapper --part PIC16F876A --tool PK3 --file firmware.hex --power 5.0 --ipecmd-path "C:\custom\path\ipecmd.exe"
```

### Advanced Programming with Multiple Options

Program with erase, verify, and VDD-first sequence:

```bash
ipecmd-wrapper --part PIC18F4550 --tool PK4 --file firmware.hex --power 3.3 --erase --verify P --vdd-first --ipecmd-version 6.25
```

## Rich Help Output

The new Typer-based CLI provides beautiful, organized help output. To see all available options with detailed descriptions:

```bash
ipecmd-wrapper --help
```

This will display a rich, color-coded help message with:
- ✅ Clear separation between required and optional arguments
- 🎨 Syntax highlighting and formatting
- 📝 Detailed descriptions for each option
- 🔍 Validation information for enum choices

## Input Validation

The new CLI provides enhanced validation:

### Tool Validation
```bash
# ✅ Valid tool choice
ipecmd-wrapper --tool PK4 ...

# ❌ Invalid tool choice (will show available options)
ipecmd-wrapper --tool INVALID ...
# Error: Invalid value for '--tool' / '-T': 'INVALID' is not one of 'PK3', 'PK4', 'PK5', ...
```

### File Path Validation
```bash
# ✅ Existing file
ipecmd-wrapper --file firmware.hex ...

# ❌ Non-existent file
ipecmd-wrapper --file missing.hex ...
# Error: Invalid value for '--file' / '-F': Path 'missing.hex' does not exist.
```

### Version Validation
```bash
# ✅ Valid version
ipecmd-wrapper --ipecmd-version 6.20 ...

# ❌ Invalid version
ipecmd-wrapper --ipecmd-version 7.0 ...
# Error: Invalid value for '--ipecmd-version': '7.0' is not one of '5.50', '6.00', '6.05', ...
```

## Exit Codes

- `0` - Success
- `1` - General error
- `2` - Command line argument error
- `3` - File not found
- `4` - IPECMD not found
- `5` - Programming failed
- `6` - Verification failed
- `7` - Programmer not found

## Common Device Names

### PIC10F Series
- PIC10F200, PIC10F202, PIC10F204, PIC10F206
- PIC10F220, PIC10F222

### PIC12F Series
- PIC12F508, PIC12F509, PIC12F510
- PIC12F629, PIC12F675
- PIC12F683, PIC12F685

### PIC16F Series
- PIC16F84A, PIC16F88
- PIC16F628A, PIC16F648A
- PIC16F876A, PIC16F877A
- PIC16F886, PIC16F887

### PIC18F Series
- PIC18F2455, PIC18F2550
- PIC18F4455, PIC18F4550
- PIC18F2620, PIC18F4620
- PIC18F46K22, PIC18F47K22

## Troubleshooting

### Device Not Recognized

Make sure the device name exactly matches the IPECMD supported devices:
```bash
ipecmd-wrapper -P PIC16F876A  # Correct
ipecmd-wrapper -P pic16f876a  # Incorrect (case sensitive)
```

### Invalid Programmer

Verify the programmer type is supported:
```bash
ipecmd-wrapper -T PK3  # Correct
ipecmd-wrapper -T PICKIT3  # Incorrect
```

### File Not Found

Use absolute paths for hex files:
```bash
ipecmd-wrapper -F "C:\project\firmware.hex"  # Windows
ipecmd-wrapper -F "/home/user/project/firmware.hex"  # Linux/macOS
```
