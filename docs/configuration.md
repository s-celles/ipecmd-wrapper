# Configuration

IPECMD Wrapper can be configured through command-line arguments, environment variables, or configuration files.

## Command Line Arguments

All configuration options are available as command-line arguments:

```bash
ipecmd-wrapper --help
```

## Environment Variables

You can set default values using environment variables:

### `IPECMD_PATH`
Default path to IPECMD executable:
```bash
export IPECMD_PATH="/opt/microchip/mplabx/v6.20/mplab_platform/mplab_ipe/ipecmd"
```

### `IPECMD_VERSION`
Default IPECMD version:
```bash
export IPECMD_VERSION="6.20"
```

### `PIC_PROGRAMMER`
Default programmer type:
```bash
export PIC_PROGRAMMER="PK3"
```

### `PIC_POWER_VOLTAGE`
Default target power voltage:
```bash
export PIC_POWER_VOLTAGE="5.0"
```

## Configuration Files

### Project Configuration

Create a `.ipecmd-wrapper.json` file in your project directory:

```json
{
    "device": "PIC16F876A",
    "programmer": "PK3",
    "power": 5.0,
    "ipecmd_version": "6.20",
    "default_options": {
        "erase": true,
        "verify": "P",
        "memory": "P"
    }
}
```

### User Configuration

Create a user-level configuration file:

**Windows:** `%APPDATA%\ipecmd-wrapper\config.json`
**Linux/macOS:** `~/.config/ipecmd-wrapper/config.json`

```json
{
    "ipecmd_path": "/custom/path/to/ipecmd",
    "default_programmer": "PK4",
    "default_power": 3.3
}
```

## Priority Order

Configuration values are resolved in this order (highest to lowest priority):

1. Command-line arguments
2. Environment variables
3. Project configuration file
4. User configuration file
5. Default values

## Supported Devices

The wrapper supports all PIC microcontrollers supported by IPECMD, including:

- PIC10F series
- PIC12F series
- PIC16F series
- PIC18F series
- PIC24F series
- PIC32 series
- dsPIC series

## Supported Programmers

- **PK3**: PICkit 3
- **PK4**: PICkit 4
- **PK5**: PICkit 5
- **ICD3**: MPLAB ICD 3
- **ICD4**: MPLAB ICD 4
- **ICD5**: MPLAB ICD 5
- **ICE4**: MPLAB ICE 4
- **RICE**: MPLAB REAL ICE
- **SNAP**: MPLAB SNAP
- **PM3**: MPLAB PM3
- **PKOB**: PICkit On Board
- **PKOB4**: PICkit 4 On Board
- **J32**: MPLAB J32

## Advanced Configuration

### Logging

Enable debug logging:
```bash
export IPECMD_WRAPPER_DEBUG=1
```

### Timeout Settings

Set custom timeout for operations:
```bash
export IPECMD_WRAPPER_TIMEOUT=60
```

### Custom Commands

Override default IPECMD commands:
```json
{
    "custom_commands": {
        "program": ["-P{device}", "-T{tool}", "-F{file}", "-M{memory}", "-W{power}"],
        "verify": ["-P{device}", "-T{tool}", "-F{file}", "-Y{verify}"]
    }
}
```
