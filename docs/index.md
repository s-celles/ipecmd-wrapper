# 🔧 IPECMD Wrapper

A modern Python wrapper for the IPECMD command line interface (CLI) program, designed for programming PIC microcontrollers with a beautiful, validated CLI interface.

## 🌟 Overview

IPECMD Wrapper provides a clean, Pythonic interface to the IPECMD command-line tool, making it easy to integrate PIC microcontroller programming into your Python projects and build systems. The latest version features a modern Typer-powered CLI with rich formatting and comprehensive input validation.

!!! warning
    This project is currently in active development. APIs may change between versions.

!!! info "AI-Generated Content Notice"
    A significant portion of this project's content (including code, documentation, and examples) has been generated using AI assistance. Please review all code and documentation carefully before use in production environments. We recommend thorough testing and validation of any AI-generated components.

## ✨ Features

- **🌐 Cross-platform**: Works on Windows, Linux, and macOS
- **🚀 Easy to use**: Modern CLI with rich help output and Python API
- **🎯 Flexible**: Supports various PIC microcontrollers and programmers
- **🛡️ Reliable**: Comprehensive error handling and input validation
- **🔧 Modern**: Built with modern Python packaging, Typer CLI, and development practices
- **✅ Validated**: Automatic validation of tool choices, file paths, and version selections
- **🎨 Beautiful**: Rich, color-coded CLI output with clear error messages

## 🚀 Quick Start

### 📦 Installation

```bash
pip install ipecmd-wrapper
```

### 💻 Modern Command Line Usage

```bash
# Program a PIC microcontroller with the new validated CLI
ipecmd-wrapper PIC16F876A PK3 --file firmware.hex --power 5.0 --ipecmd-version 6.20

# Get beautiful, organized help
ipecmd-wrapper --help

# Test programmer connection
ipecmd-wrapper PIC16F876A PK4 --file firmware.hex --power 5.0 --test-programmer
```

### 🎨 Rich CLI Features

The new CLI provides:

- **✅ Input Validation**: Tool choices, file paths, and versions are automatically validated
- **🎯 Required vs Optional**: Clear distinction between required and optional arguments
- **📝 Rich Help**: Beautiful, organized help output with syntax highlighting
- **🔍 Clear Errors**: Helpful error messages with suggestions for valid inputs

### 🐍 Python API

```python
from ipecmd_wrapper import upload_firmware

# Upload firmware to PIC
success = upload_firmware(
    hex_file="firmware.hex", device="PIC16F876A", programmer="pickit3"
)

if success:
    print("Upload successful!")
else:
    print("Upload failed!")
```

## 🎯 Supported Features

- **🔧 Devices**: All PIC microcontrollers supported by IPECMD
- **📱 Programmers**: PICKit 3, PICKit 4, ICD 3, ICD 4, and more
- **⚡ Operations**: Programming, verification, device detection
- **📄 Formats**: Intel HEX files

## 📋 Requirements

- 🐍 Python 3.9+
- 🔧 IPECMD installed and accessible in PATH
- 📱 Compatible PIC programmer hardware

## Documentation

- [📦 Installation Guide](installation.md)
- [🚀 Quick Start](quickstart.md)
- [💻 Command Line Reference](cli.md)
- [🐍 Python API Reference](api.md)
- [📝 Examples](examples.md)
- [🛠️ Development Guide](development.md)

## 🤝 Contributing

We welcome contributions! Please see our [🤝 Contributing Guide](contributing.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [📄 LICENSE](license.md) file for details.

## Related Projects

- **[🔧 XC8 Wrapper](https://s-celles.github.io/xc8-wrapper/)** - Modern Python wrapper for the XC8 C compiler toolchain
  - Perfect companion for compiling PIC microcontroller firmware before programming
  - Cross-platform support for Windows, Linux, and macOS
  - [GitHub Repository](https://github.com/s-celles/xc8-wrapper)

## Support

- [🐛 GitHub Issues](https://github.com/s-celles/ipecmd-wrapper/issues)
- [💡 Feature Requests](https://github.com/s-celles/ipecmd-wrapper/discussions)
- [📚 Documentation](https://s-celles.github.io/ipecmd-wrapper/)
- [💾 Source Code](https://github.com/s-celles/ipecmd-wrapper)
