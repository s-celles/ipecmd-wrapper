"""
Tests for CLI module

Test suite for the command-line interface functionality.
"""

import os
import tempfile
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from ipecmd_wrapper.cli import ToolChoice, VersionChoice, app


@pytest.mark.unit
@pytest.mark.cli
class TestTyperCLI:
    """Test Typer CLI functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.runner = CliRunner()
        # Create a temporary hex file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_hex_file = os.path.join(self.temp_dir, "test.hex")
        with open(self.test_hex_file, "w") as f:
            f.write(":00000001FF\n")  # Simple Intel hex format

    def _get_error_output(self, result):
        """Get error output from CLI result, handling different Typer versions"""
        # Try to get stderr first, fall back to stdout if not available
        try:
            return result.stderr if result.stderr else result.stdout
        except (ValueError, AttributeError):
            return result.stdout

    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_help_command(self):
        """Test that help command works"""
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "IPECMD wrapper for PIC programming" in result.stdout

    def test_version_command(self):
        """Test version command"""
        result = self.runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "ipecmd-wrapper" in result.stdout

    def test_missing_required_arguments(self):
        """Test CLI with missing required arguments"""
        result = self.runner.invoke(app, [])
        assert result.exit_code != 0
        error_output = self._get_error_output(result)
        assert (
            "missing option" in error_output.lower()
            or "required" in error_output.lower()
            or "usage" in error_output.lower()
        )

    def test_valid_tool_choices(self):
        """Test that valid tool choices are accepted"""
        for tool in ToolChoice:
            result = self.runner.invoke(
                app,
                [
                    "--tool",
                    tool.value,
                    "--part",
                    "PIC16F877A",
                    "--file",
                    self.test_hex_file,
                    "--power",
                    "5.0",
                    "--test-programmer",
                ],
            )
            # Should not fail due to invalid tool choice
            assert "is not one of" not in result.stdout

    def test_invalid_tool_choice(self):
        """Test that invalid tool choices are rejected"""
        result = self.runner.invoke(
            app,
            [
                "--tool",
                "INVALID",
                "--part",
                "PIC16F877A",
                "--file",
                self.test_hex_file,
                "--power",
                "5.0",
            ],
        )
        assert result.exit_code != 0
        error_output = self._get_error_output(result)
        assert (
            "not one of" in error_output
            or "invalid choice" in error_output.lower()
            or "choose from" in error_output.lower()
        )

    def test_valid_version_choices(self):
        """Test that valid version choices are accepted"""
        for version in VersionChoice:
            result = self.runner.invoke(
                app,
                [
                    "--tool",
                    "PK4",
                    "--part",
                    "PIC16F877A",
                    "--file",
                    self.test_hex_file,
                    "--power",
                    "5.0",
                    "--ipecmd-version",
                    version.value,
                    "--test-programmer",
                ],
            )
            # Should not fail due to invalid version choice
            assert "is not one of" not in result.stdout

    def test_nonexistent_file_rejected(self):
        """Test that nonexistent files are rejected"""
        result = self.runner.invoke(
            app,
            [
                "--tool",
                "PK4",
                "--part",
                "PIC16F877A",
                "--file",
                "nonexistent.hex",
                "--power",
                "5.0",
            ],
        )
        assert result.exit_code != 0
        error_output = self._get_error_output(result)
        assert (
            "does not exist" in error_output
            or "not found" in error_output.lower()
            or "no such file" in error_output.lower()
        )

    @patch("ipecmd_wrapper.cli.program_pic")
    def test_successful_program_call(self, mock_program_pic):
        """Test that program_pic is called with correct arguments"""
        mock_program_pic.return_value = None

        self.runner.invoke(
            app,
            [
                "--tool",
                "PK4",
                "--part",
                "PIC16F877A",
                "--file",
                self.test_hex_file,
                "--power",
                "5.0",
                "--ipecmd-version",
                "6.20",
                "--memory",
                "P",
                "--verify",
                "P",
                "--erase",
            ],
        )

        # Check that program_pic was called
        mock_program_pic.assert_called_once()

        # Check the call arguments (program_pic expects an args object)
        args = mock_program_pic.call_args[0][
            0
        ]  # Get first positional argument (args object)
        assert args.part == "PIC16F877A"
        assert args.tool == "PK4"  # String value from enum
        assert args.file == self.test_hex_file
        assert args.power == "5.0"
        assert args.ipecmd_version == "6.20"  # String value from enum
        assert args.memory == "P"
        assert args.verify == "P"
        assert args.erase

    @patch("ipecmd_wrapper.cli.program_pic")
    def test_test_programmer_mode(self, mock_program_pic):
        """Test test programmer mode"""
        mock_program_pic.return_value = None

        self.runner.invoke(
            app,
            [
                "--tool",
                "PK4",
                "--part",
                "PIC16F877A",
                "--file",
                self.test_hex_file,
                "--power",
                "5.0",
                "--ipecmd-version",
                "6.20",  # Required parameter
                "--test-programmer",
            ],
        )

        mock_program_pic.assert_called_once()
        args = mock_program_pic.call_args[0][0]  # Get first positional argument
        assert args.test_programmer


@pytest.mark.unit
@pytest.mark.cli
class TestEnums:
    """Test enum definitions"""

    def test_tool_choice_enum(self):
        """Test ToolChoice enum values"""
        assert ToolChoice.PK3.value == "PK3"
        assert ToolChoice.PK4.value == "PK4"
        assert ToolChoice.PK5.value == "PK5"
        # Test that all expected tools are present
        expected_tools = {
            "PK3",
            "PK4",
            "PK5",
            "ICD3",
            "ICD4",
            "ICD5",
            "ICE4",
            "RICE",
            "SNAP",
            "PM3",
            "PKOB",
            "PKOB4",
            "J32",
        }
        actual_tools = {tool.value for tool in ToolChoice}
        assert actual_tools == expected_tools

    def test_version_choice_enum(self):
        """Test VersionChoice enum values"""
        assert VersionChoice.V5_50.value == "5.50"
        assert VersionChoice.V6_00.value == "6.00"
        assert VersionChoice.V6_25.value == "6.25"
        # Test that all expected versions are present
        expected_versions = {"5.50", "6.00", "6.05", "6.10", "6.15", "6.20", "6.25"}
        actual_versions = {version.value for version in VersionChoice}
        assert actual_versions == expected_versions


if __name__ == "__main__":
    pytest.main([__file__])
