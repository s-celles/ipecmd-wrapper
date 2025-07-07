# IPECMD Wrapper

A Python wrapper for Microchip's IPECMD tool for PIC microcontroller programming.

## 📚 Documentation

**For complete documentation, installation instructions, usage examples, and API reference, visit:**

**[https://s-celles.github.io/ipecmd-wrapper/](https://s-celles.github.io/ipecmd-wrapper/)**

## Quick Start

```bash
# Install the package
pip install ipecmd-wrapper

# Basic usage
ipecmd-wrapper -P PIC16F876A -T PK3 -F firmware.hex -W 5.0 --ipecmd-version 6.20
```

## Features

- Complete wrapper around MPLAB IPE's ipecmd.exe
- Support for all major PIC programmers (PICkit3, PICkit4, ICD3, ICD4, SNAP, etc.)
- Cross-platform support (Windows, Linux, macOS)
- Colored output for better readability

## Important Legal Notice

**This package is a wrapper for Microchip's proprietary MPLAB IPE/IPECMD tools.**

### What This Package Provides
This package provides Python wrapper code that interfaces with Microchip's MPLAB IPE command-line tool (IPECMD). It does NOT include the actual MPLAB IPE software.

### Microchip MPLAB IPE License
The MPLAB IPE tools are **proprietary software owned exclusively by Microchip Technology Inc.** You must obtain proper licenses from Microchip to use the MPLAB IPE tools.

### This Package's License
The Python wrapper code in this package is released under the **MIT License** (see LICENSE file).

**For detailed licensing information and legal requirements, see the [License section](https://s-celles.github.io/ipecmd-wrapper/license/) in the documentation.**

## Links

- **[Documentation](https://s-celles.github.io/ipecmd-wrapper/)** - Complete documentation
- **[Repository](https://github.com/s-celles/ipecmd-wrapper)** - Source code
- **[Issues](https://github.com/s-celles/ipecmd-wrapper/issues)** - Bug reports and feature requests
- **[Changelog](https://github.com/s-celles/ipecmd-wrapper/blob/main/CHANGELOG.md)** - Release history

## License

**Wrapper Code**: MIT License (see LICENSE file)
**Microchip MPLAB IPE Tools**: Proprietary Microchip licenses (separate licensing required)
