# 📦 Installation Guide

## 📋 Requirements

Before installing IPECMD Wrapper, ensure you have:

- 🐍 Python 3.9 or higher
- 🔧 IPECMD installed and accessible in your PATH
- 📱 Compatible PIC programmer hardware

## 🔧 Installing IPECMD

IPECMD comes as part of the MPLAB X IDE installation. Download and install MPLAB X IDE from the [🏢 Microchip website](https://www.microchip.com/mplab/mplab-x-ide).

### 🖥️ Windows
After installing MPLAB X IDE, IPECMD is typically located at:
```
C:\Program Files\Microchip\MPLABX\v[version]\mplab_platform\mplab_ipe\ipecmd.exe
```

### 🐧 Linux
```
/opt/microchip/mplabx/v[version]/mplab_platform/mplab_ipe/ipecmd
```

### 🍎 macOS
```
/Applications/microchip/mplabx/v[version]/mplab_platform/mplab_ipe/ipecmd
```

## Installing IPECMD Wrapper

### From PyPI (Recommended)

```bash
pip install ipecmd-wrapper
```

### From Source

```bash
git clone https://github.com/s-celles/ipecmd-wrapper.git
cd ipecmd-wrapper
pip install -e .
```

### Development Installation

For development work:

```bash
git clone https://github.com/s-celles/ipecmd-wrapper.git
cd ipecmd-wrapper
pip install -e .[dev]
```

## Verify Installation

Test that the installation worked:

```bash
ipecmd-wrapper --help
```

Or in Python:

```python
import ipecmd_wrapper
print(ipecmd_wrapper.__version__)
```

## Troubleshooting

### IPECMD Not Found

If you get an error that IPECMD is not found:

1. Verify IPECMD is installed
2. Add IPECMD to your PATH environment variable
3. Or specify the full path using `--ipecmd-path`

### Permission Errors

On Linux/macOS, you might need to add your user to the dialout group:

```bash
sudo usermod -a -G dialout $USER
```

Then log out and log back in.

### Windows Driver Issues

Make sure you have the latest PICkit drivers installed from Microchip.
