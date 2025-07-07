# API Reference

Auto-generated API documentation for IPECMD Wrapper.

## Core Module (`ipecmd_wrapper.core`)

### Functions

#### `upload_firmware(hex_file, device, programmer, **kwargs)`

Primary function for uploading firmware to PIC microcontrollers.

**Parameters:**
- `hex_file` (str): Path to Intel HEX file
- `device` (str): Target device name
- `programmer` (str): Programmer type
- `**kwargs`: Additional options

**Returns:**
- `bool`: Success status

#### `program_pic(**kwargs)`

Low-level programming function with detailed control.

**Parameters:**
- `part` (str): Target device
- `tool` (str): Programmer type
- `file` (str): HEX file path
- `power` (float): Target voltage
- Additional options...

**Raises:**
- `RuntimeError`: Programming failure
- `FileNotFoundError`: File not found

#### `get_ipecmd_path(version=None, custom_path=None)`

Get IPECMD executable path.

**Returns:**
- `str`: Path to IPECMD

#### `validate_ipecmd(ipecmd_path, version_info)`

Validate IPECMD installation.

**Returns:**
- `bool`: Validation result

#### `validate_hex_file(hex_file_path)`

Validate Intel HEX file format.

**Returns:**
- `bool`: Validation result

#### `build_ipecmd_command(**kwargs)`

Build IPECMD command arguments.

**Returns:**
- `list`: Command arguments

#### `test_programmer_detection(ipecmd_path, part, tool)`

Test programmer connectivity.

**Returns:**
- `bool`: Detection result

### Constants

#### `TOOL_CHOICES`
List of supported programmer types.

#### `VERSION_CHOICES`
List of supported IPECMD versions.

#### `TOOL_MAP`
Mapping of tool names to identifiers.

## CLI Module (`ipecmd_wrapper.cli`)

### Functions

#### `create_argument_parser()`

Create command-line argument parser.

**Returns:**
- `argparse.ArgumentParser`: Configured parser

#### `main(args=None)`

Main CLI entry point.

**Parameters:**
- `args` (list, optional): Command arguments

## Exception Classes

### `IPECMDError`
Base exception for IPECMD-related errors.

### `ProgrammingError`
Raised when programming operations fail.

### `ValidationError`
Raised when validation fails.

## Type Definitions

### `DeviceType`
Type alias for device names (str).

### `ProgrammerType`
Type alias for programmer types (str).

### `VoltageType`
Type alias for voltage values (float).

## Usage Examples

See [Examples](examples.md) for comprehensive usage examples.
