# Command Line Reference

Complete reference for the IPECMD Wrapper command-line interface.

## Synopsis

```bash
ipecmd-wrapper [OPTIONS]
```

## Required Arguments

### `-P, --part DEVICE`
Target PIC microcontroller device.

**Example:**
```bash
ipecmd-wrapper -P PIC16F876A ...
```

### `-T, --tool PROGRAMMER`
Programmer type.

**Options:**
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

### `-F, --file HEXFILE`
Intel HEX file to program.

### `-W, --power VOLTAGE`
Target power voltage (e.g., 5.0, 3.3).

## Optional Arguments

### `-M, --memory TYPE`
Memory type to program.

**Options:**
- `P` - Program memory (default)
- `E` - EEPROM memory

### `-Y, --verify TYPE`
Verify programming.

**Options:**
- `P` - Verify program memory
- `E` - Verify EEPROM memory

### `-E, --erase`
Erase device before programming.

### `-OL, --preserve-eeprom`
Preserve EEPROM during programming.

### `-OD, --preserve-userid`
Preserve User ID during programming.

### `--test-programmer`
Test programmer connection without programming.

### `--ipecmd-version VERSION`
Specify IPECMD version.

**Options:**
- `5.50`
- `6.20`

### `--ipecmd-path PATH`
Custom path to IPECMD executable.

### `--version`
Show version information.

### `-h, --help`
Show help message.

## Examples

### Basic Programming

```bash
ipecmd-wrapper -P PIC16F876A -T PK3 -F firmware.hex -W 5.0
```

### Program with Erase and Verify

```bash
ipecmd-wrapper -P PIC16F876A -T PK3 -F firmware.hex -W 5.0 -E -Y P
```

### Test Programmer Connection

```bash
ipecmd-wrapper -P PIC16F876A -T PK3 -W 5.0 --test-programmer
```

### Program EEPROM

```bash
ipecmd-wrapper -P PIC16F876A -T PK3 -F eeprom.hex -W 5.0 -M E
```

### Use Custom IPECMD Path

```bash
ipecmd-wrapper -P PIC16F876A -T PK3 -F firmware.hex -W 5.0 --ipecmd-path "C:\custom\ipecmd.exe"
```

### Preserve EEPROM

```bash
ipecmd-wrapper -P PIC16F876A -T PK3 -F firmware.hex -W 5.0 -OL
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
