# IPECMD Wrapper

A modern Python wrapper for the IPECMD toolchain, designed for programming PIC microcontrollers.

## Overview

IPECMD Wrapper provides a clean, Pythonic interface to the IPECMD command-line tool, making it easy to integrate PIC microcontroller programming into your Python projects and build systems.

## Features

- **Cross-platform**: Works on Windows, Linux, and macOS
- **Easy to use**: Simple command-line interface and Python API
- **Flexible**: Supports various PIC microcontrollers and programmers
- **Reliable**: Comprehensive error handling and validation
- **Modern**: Built with modern Python packaging and development practices

## Quick Start

### Installation

```bash
pip install ipecmd-wrapper
```

### Command Line Usage

```bash
# Program a PIC microcontroller
ipecmd-wrapper --device PIC16F876A --programmer pickit3 --hex-file firmware.hex

# Get help
ipecmd-wrapper --help
```

### Python API

```python
from ipecmd_wrapper import upload_firmware

# Upload firmware to PIC
success = upload_firmware(
    hex_file="firmware.hex",
    device="PIC16F876A",
    programmer="pickit3"
)

if success:
    print("Upload successful!")
else:
    print("Upload failed!")
```

## Supported Features

- **Devices**: All PIC microcontrollers supported by IPECMD
- **Programmers**: PICKit 3, PICKit 4, ICD 3, ICD 4, and more
- **Operations**: Programming, verification, device detection
- **Formats**: Intel HEX files

## Requirements

- Python 3.9+
- IPECMD installed and accessible in PATH
- Compatible PIC programmer hardware

## Documentation

- [Installation Guide](installation.md)
- [Quick Start](quickstart.md)
- [Command Line Reference](cli.md)
- [Python API Reference](api.md)
- [Examples](examples.md)
- [Development Guide](development.md)

## Contributing

We welcome contributions! Please see our [Contributing Guide](contributing.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](license.md) file for details.

## Support

- [GitHub Issues](https://github.com/s-celles/ipecmd-wrapper/issues)
- [Documentation](https://s-celles.github.io/ipecmd-wrapper/)
- [Source Code](https://github.com/s-celles/ipecmd-wrapper)
