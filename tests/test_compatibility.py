"""
Compatibility tests for IPECMD Wrapper

Test compatibility across different Python versions, platforms, and environments.
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from ipecmd_wrapper.core import (
    get_ipecmd_path,
    validate_hex_file,
    validate_ipecmd,
)


@pytest.mark.compatibility
class TestPythonVersionCompatibility:
    """Test compatibility across Python versions"""

    def test_pathlib_compatibility(self):
        """Test pathlib usage across Python versions"""
        # Test Path operations that might vary across versions
        test_path = Path(
            "C:\\Program Files\\Microchip\\MPLABX\\v6.20\\mplab_platform\\"
            "mplab_ipe\\ipecmd.exe"
        )

        # These operations should work in Python 3.9+
        assert isinstance(test_path.name, str)
        assert isinstance(test_path.parent, Path)
        assert isinstance(test_path.suffix, str)

        # Test path resolution
        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.return_value = True
            resolved_path = get_ipecmd_path("6.20")
            assert isinstance(resolved_path, str)

    def test_subprocess_compatibility(self):
        """Test subprocess usage across Python versions"""
        # Test subprocess.run with text parameter (Python 3.7+)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "MPLAB IPE version 6.20"
            mock_run.return_value.stderr = ""

            result = validate_ipecmd("test_path", "6.20")
            assert isinstance(result, bool)

    def test_string_formatting_compatibility(self):
        """Test string formatting methods used in the package"""
        # f-strings (Python 3.6+)
        part = "16F876A"
        tool = "PK3"
        voltage = 5.0

        formatted = f"Programming {part} with {tool} at {voltage}V"
        assert "16F876A" in formatted
        assert "PK3" in formatted
        assert "5.0" in formatted

    def test_type_hints_compatibility(self):
        """Test that type hints don't break execution"""
        # Import modules that use type hints
        from ipecmd_wrapper.cli import ToolChoice, app
        from ipecmd_wrapper.core import get_ipecmd_path

        # These should work regardless of type hint support
        assert callable(get_ipecmd_path)
        assert app is not None  # Typer app should be created
        assert hasattr(ToolChoice, "PK3")  # Enum should be available


@pytest.mark.compatibility
class TestPlatformCompatibility:
    """Test compatibility across different platforms"""

    @patch("sys.platform", "win32")
    def test_windows_path_handling(self):
        """Test Windows-specific path handling"""
        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.return_value = False  # Force default path selection
            path = get_ipecmd_path("6.20")

            # Should use Windows path format
            assert "Program Files" in path
            assert path.endswith("ipecmd.exe")
            # Check that it's a Windows-style path structure
            assert "C:" in path or "C:/" in path
            assert "Microchip" in path
            assert "MPLABX" in path

    @patch("sys.platform", "linux")
    def test_linux_path_handling(self):
        """Test Linux-specific path handling"""
        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.return_value = False  # Force default path selection
            path = get_ipecmd_path("6.20")

            # Should use Linux path format
            assert path.startswith("/opt/microchip/mplabx")
            assert path.endswith("ipecmd")  # No .exe extension on Linux
            assert "v6.20" in path
            assert "mplab_platform" in path

    @patch("sys.platform", "darwin")
    def test_macos_path_handling(self):
        """Test macOS-specific path handling"""
        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.return_value = False  # Force default path selection
            path = get_ipecmd_path("6.20")

            # Should use macOS path format
            assert path.startswith("/Applications/microchip/mplabx")
            assert path.endswith("ipecmd")  # No .exe extension on macOS
            assert "v6.20" in path
            assert "mplab_platform" in path

    def test_unicode_path_handling(self):
        """Test Unicode characters in file paths"""
        unicode_paths = [
            "C:\\Français\\MPLABX\\ipecmd.exe",
            "C:\\Русский\\MPLABX\\ipecmd.exe",
            "C:\\中文\\MPLABX\\ipecmd.exe",
            "C:\\🔧Tools\\MPLABX\\ipecmd.exe",
        ]

        for unicode_path in unicode_paths:
            with patch("pathlib.Path.exists") as mock_exists:
                mock_exists.return_value = True
                # Should not crash with Unicode paths
                result = validate_hex_file(
                    unicode_path.replace("ipecmd.exe", "test.hex")
                )
                assert isinstance(result, bool)

    def test_long_path_handling(self):
        """Test very long file paths"""
        # Create a very long path
        long_path = (
            "C:\\"
            + "\\".join([f"very_long_directory_name_{i}" for i in range(20)])
            + "\\test.hex"
        )

        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.return_value = True
            # Should handle long paths without issues
            result = validate_hex_file(long_path)
            assert isinstance(result, bool)


@pytest.mark.compatibility
class TestEnvironmentCompatibility:
    """Test compatibility in different environments"""

    def test_virtual_environment_compatibility(self):
        """Test running in virtual environments"""
        # Test that package works in virtual environments
        import ipecmd_wrapper

        # Should be able to import and use the package
        assert hasattr(ipecmd_wrapper, "__version__")
        assert callable(ipecmd_wrapper.get_ipecmd_path)

    def test_frozen_application_compatibility(self):
        """Test behavior when running as frozen application (PyInstaller, etc.)"""
        # Simulate frozen application
        with patch("sys.frozen", True, create=True):
            # Package should still work
            from ipecmd_wrapper.core import get_ipecmd_path

            with patch("pathlib.Path.exists") as mock_exists:
                mock_exists.return_value = True
                path = get_ipecmd_path("6.20")
                assert isinstance(path, str)

    def test_no_write_permissions(self):
        """Test behavior when write permissions are limited"""
        with tempfile.TemporaryDirectory() as temp_dir:
            read_only_file = Path(temp_dir) / "readonly.hex"
            read_only_file.write_text(":00000001FF\n")

            # Make file read-only on Windows
            if sys.platform == "win32":
                os.chmod(read_only_file, 0o444)

            # Should still be able to validate read-only files
            result = validate_hex_file(str(read_only_file))
            assert isinstance(result, bool)

    def test_missing_dependencies(self):
        """Test graceful handling of missing optional dependencies"""
        # Test that core functionality works even if optional deps are missing
        with patch.dict("sys.modules", {"colorama": None}):
            # Should still work without colorama (graceful degradation)
            from ipecmd_wrapper.core import get_ipecmd_path

            with patch("pathlib.Path.exists") as mock_exists:
                mock_exists.return_value = True
                path = get_ipecmd_path("6.20")
                assert isinstance(path, str)


@pytest.mark.compatibility
class TestIntegrationCompatibility:
    """Test compatibility with external tools and systems"""

    def test_command_line_encoding(self):
        """Test handling of different command line encodings"""
        import os
        import tempfile

        from typer.testing import CliRunner

        from ipecmd_wrapper.cli import app

        # Create a temporary hex file for testing
        temp_dir = tempfile.mkdtemp()
        test_hex_file = os.path.join(temp_dir, "test.hex")
        with open(test_hex_file, "w") as f:
            f.write(":00000001FF\n")

        runner = CliRunner()

        test_commands = [
            [
                "--part",
                "16F876A",
                "--tool",
                "PK3",
                "--file",
                test_hex_file,
                "--power",
                "5.0",
                "--test-programmer",
            ],
            [
                "--part",
                "18F4550",
                "--tool",
                "PK4",
                "--file",
                test_hex_file,
                "--power",
                "5.0",
                "--test-programmer",
            ],
        ]

        for cmd in test_commands:
            # Should handle different argument formats
            with patch("ipecmd_wrapper.cli.program_pic") as mock_program_pic:
                mock_program_pic.return_value = None
                result = runner.invoke(app, cmd)
                # Test should not crash due to encoding issues (check both stdout and output)
                assert result.exit_code == 0 or "Error:" in result.output

        # Clean up
        import shutil

        shutil.rmtree(temp_dir)

    def test_exit_code_compatibility(self):
        """Test that exit codes are handled consistently"""
        import os
        import tempfile

        from typer.testing import CliRunner

        from ipecmd_wrapper.cli import app

        # Create a temporary hex file for testing
        temp_dir = tempfile.mkdtemp()
        test_hex_file = os.path.join(temp_dir, "test.hex")
        with open(test_hex_file, "w") as f:
            f.write(":00000001FF\n")

        runner = CliRunner()

        with patch("ipecmd_wrapper.core.get_ipecmd_path") as mock_get_path:
            mock_get_path.side_effect = FileNotFoundError("IPECMD not found")

            # Should exit with appropriate code
            result = runner.invoke(
                app,
                [
                    "--part",
                    "16F876A",
                    "--tool",
                    "PK3",
                    "--file",
                    test_hex_file,
                    "--power",
                    "5.0",
                    "--ipecmd-version",
                    "6.20",
                ],
            )

            # Should exit with error code
            assert result.exit_code != 0

        # Clean up
        import shutil

        shutil.rmtree(temp_dir)

    def test_environment_variable_handling(self):
        """Test handling of environment variables"""
        # Test with custom environment variables
        with patch.dict(os.environ, {"IPECMD_PATH": "C:\\custom\\ipecmd.exe"}):
            # Should respect environment variables if implemented
            path = get_ipecmd_path("6.20")
            assert isinstance(path, str)


if __name__ == "__main__":
    pytest.main([__file__])
