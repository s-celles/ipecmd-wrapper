"""
Integration tests for IPECMD Wrapper

Test the integration between different components of the IPECMD wrapper.
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from ipecmd_wrapper.cli import main


@pytest.mark.integration
class TestIntegration:
    """Integration tests for IPECMD wrapper components"""

    def test_cli_to_core_integration(self):
        """Test integration between CLI and core modules"""
        with (
            patch("ipecmd_wrapper.core.get_ipecmd_path") as mock_get_path,
            patch("ipecmd_wrapper.core.validate_ipecmd") as mock_validate,
            patch("ipecmd_wrapper.core.validate_hex_file") as mock_validate_hex,
            patch("ipecmd_wrapper.core.execute_programming") as mock_program,
        ):

            # Setup mocks
            mock_get_path.return_value = (
                r"C:\MPLABX\v6.20\mplab_platform\mplab_ipe\ipecmd.exe"
            )
            mock_validate.return_value = True
            mock_validate_hex.return_value = True
            mock_program.return_value = True

            # Test CLI to core integration
            try:
                main(
                    [
                        "-P",
                        "16F876A",
                        "-T",
                        "PK3",
                        "-F",
                        "test.hex",
                        "--ipecmd-version",
                        "6.20",
                    ]
                )
            except SystemExit:
                # Expected when tool execution completes
                pass

            # Verify the integration chain
            mock_get_path.assert_called()
            mock_validate.assert_called()

    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test hex file
            hex_file = Path(temp_dir) / "test.hex"
            hex_file.write_text(
                """
:10000000FF30FF30FF30FF30FF30FF30FF30FF3070
:10001000FF30FF30FF30FF30FF30FF30FF30FF3060
:00000001FF
"""
            )

            with (
                patch("ipecmd_wrapper.core.validate_ipecmd") as mock_validate,
                patch("ipecmd_wrapper.core.get_ipecmd_path") as mock_get_path,
                patch("ipecmd_wrapper.core.execute_programming") as mock_program,
            ):

                # Setup mocks
                mock_get_path.return_value = (
                    r"C:\MPLABX\v6.20\mplab_platform\mplab_ipe\ipecmd.exe"
                )
                mock_validate.return_value = True
                mock_program.return_value = True

                # Test complete workflow
                try:
                    main(
                        [
                            "-P",
                            "16F876A",
                            "-T",
                            "PK3",
                            "-F",
                            str(hex_file),
                            "--ipecmd-version",
                            "6.20",
                            "-W",
                            "5.0",
                        ]
                    )
                except SystemExit:
                    pass

                # Verify workflow executed
                mock_get_path.assert_called()
                mock_validate.assert_called()
                mock_program.assert_called()

    def test_error_handling_integration(self):
        """Test error handling across components"""
        with patch("ipecmd_wrapper.core.get_ipecmd_path") as mock_get_path:
            # Test error propagation from core to CLI
            mock_get_path.side_effect = ValueError("Test error")

            with pytest.raises(SystemExit):
                main(
                    [
                        "-P",
                        "16F876A",
                        "-T",
                        "PK3",
                        "-F",
                        "test.hex",
                        "--ipecmd-version",
                        "6.20",
                    ]
                )

    def test_configuration_integration(self):
        """Test configuration handling across components"""
        with (
            patch("ipecmd_wrapper.core.get_ipecmd_path") as mock_get_path,
            patch("ipecmd_wrapper.core.validate_ipecmd") as mock_validate,
            patch("ipecmd_wrapper.core.validate_hex_file") as mock_validate_hex,
            patch("ipecmd_wrapper.core.execute_programming") as mock_program,
        ):

            # Setup mocks
            mock_get_path.return_value = r"C:\custom\path\ipecmd.exe"
            mock_validate.return_value = True
            mock_validate_hex.return_value = True
            mock_program.return_value = True

            # Test custom path configuration
            try:
                main(
                    [
                        "-P",
                        "16F876A",
                        "-T",
                        "PK3",
                        "-F",
                        "test.hex",
                        "--ipecmd-path",
                        r"C:\custom\path\ipecmd.exe",
                    ]
                )
            except SystemExit:
                pass

            # Verify custom configuration was used
            mock_validate.assert_called_with(r"C:\custom\path\ipecmd.exe")


@pytest.mark.integration
class TestPackageIntegration:
    """Test package-level integration"""

    def test_package_imports(self):
        """Test that package imports work correctly"""
        import ipecmd_wrapper

        # Test that main exports are available
        assert hasattr(ipecmd_wrapper, "get_ipecmd_path")
        assert hasattr(ipecmd_wrapper, "validate_ipecmd")
        assert hasattr(ipecmd_wrapper, "TOOL_CHOICES")

        # Test version information
        assert hasattr(ipecmd_wrapper, "__version__")
        assert hasattr(ipecmd_wrapper, "__author__")
        assert hasattr(ipecmd_wrapper, "__email__")

    def test_cli_entry_point(self):
        """Test that CLI entry point works"""
        from ipecmd_wrapper.cli import main

        # Test that main function exists and is callable
        assert callable(main)

    def test_demo_script_integration(self):
        """Test that demo script can import and use the package"""
        # This would normally import and run the demo script
        # For now, we'll just test the imports it uses
        from ipecmd_wrapper import TOOL_CHOICES
        from ipecmd_wrapper.core import get_ipecmd_path

        # Test that demo script dependencies are available
        assert callable(get_ipecmd_path)
        assert isinstance(TOOL_CHOICES, list)


if __name__ == "__main__":
    pytest.main([__file__])
