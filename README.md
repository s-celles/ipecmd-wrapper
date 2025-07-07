# IPECMD Wrapper

A Python wrapper for Microchip's IPECMD tool for PIC microcontroller programming.

## Installation

```bash
pip install ipecmd-wrapper
```

## Usage

```bash
# Basic programming with PICkit3
ipecmd-wrapper -P PIC16F876A -T PK3 -F build/main.hex -W 5.0 --ipecmd-version 6.20

# With erase before programming
ipecmd-wrapper -P PIC16F876A -T PK3 -F build/main.hex -W 5.0 --ipecmd-version 6.20 -E

# Test programmer detection first
ipecmd-wrapper -P PIC16F876A -T PK3 -F build/main.hex -W 5.0 --ipecmd-version 6.20 --test-programmer

# With custom IPECMD path
ipecmd-wrapper -P PIC16F876A -T PK3 -F build/main.hex -W 5.0 --ipecmd-path "C:\\Custom\\MPLAB\\ipecmd.exe"

# Program specific memory regions
ipecmd-wrapper -P PIC16F876A -T PK3 -F build/main.hex -W 5.0 --ipecmd-version 6.20 -M P -Y P
```

## Features

- Complete wrapper around MPLAB IPE's ipecmd.exe
- Support for all major PIC programmers (PICkit3, PICkit4, ICD3, ICD4, SNAP, etc.)
- Flexible configuration options
- Colored output for better readability
- Cross-platform support (Windows, Linux, macOS)
- Programmer detection testing

## Supported Programmers

- PICkit3 (PK3)
- PICkit4 (PK4) 
- PICkit5 (PK5)
- ICD3, ICD4, ICD5
- ICE4, RICE
- SNAP
- PM3, PKOB, PKOB4
- J32

## Requirements

- Python 3.8+
- MPLAB X IDE installed (for ipecmd.exe)
- colorama package (installed automatically)
- Compatible PIC programmer hardware

## Development

```bash
# Clone the repository
git clone https://github.com/s-celles/ipecmd-wrapper.git
cd ipecmd-wrapper

# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Format code
black .

# Type checking
mypy .
```

## Important Legal Notice

**This package is a wrapper for Microchip's proprietary MPLAB IPE/IPECMD tools.**

### What This Package Provides
This package provides Python wrapper code that interfaces with Microchip's MPLAB IPE command-line tool (IPECMD). It does NOT include the actual MPLAB IPE software.

### Microchip MPLAB IPE License
The MPLAB IPE tools (`ipecmd.exe` and related software) are **proprietary software owned exclusively by Microchip Technology Inc.** and are subject to Microchip's own license terms. You must:

1. **Download and install** MPLAB X IDE from Microchip's official website
2. **Obtain proper licenses** from Microchip to use the MPLAB IPE tools
3. **Comply with Microchip's license terms** for the MPLAB IPE software

### This Package's License
The Python wrapper code in this package is released under the **MIT License** (see LICENSE file).

### Your Responsibility
**You are responsible for obtaining proper licenses for the Microchip MPLAB IPE tools that this wrapper interfaces with.**

For more information about MPLAB IPE licensing, visit:
- [Microchip MPLAB X IDE](https://www.microchip.com/en-us/tools-resources/develop/mplab-x-ide)
- [Microchip License Terms](https://www.microchip.com/en-us/legal/terms-of-use)

## License

**Wrapper Code**: MIT License (see LICENSE file)
**Microchip MPLAB IPE Tools**: Proprietary Microchip licenses (separate licensing required)
