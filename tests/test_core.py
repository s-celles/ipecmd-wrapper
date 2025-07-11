"""
Tests for IPECMD Wrapper Core

Basic test suite for the IPECMD wrapper core functionality.
"""

import sys
from unittest.mock import MagicMock, patch

import pytest

from ipecmd_wrapper.core import (
    TOOL_CHOICES,
    TOOL_MAP,
    VERSION_CHOICES,
    _get_version_suggestions,
    build_ipecmd_command,
    detect_programmer,
    execute_programming,
    get_ipecmd_path,
    program_pic,
    validate_hex_file,
    validate_ipecmd,
)


@pytest.mark.unit
@pytest.mark.core
class TestIPECMDPath:
    """Test IPECMD path resolution"""

    def test_get_ipecmd_path_with_version(self):
        """Test getting IPECMD path with version"""
        path = get_ipecmd_path(version="6.20")

        # Cross-platform expected path - now using string formatting for consistency
        if sys.platform == "win32":
            expected_path = (
                "C:/Program Files/Microchip/MPLABX/v6.20/"
                "mplab_platform/mplab_ipe/ipecmd.exe"
            )
        elif sys.platform == "darwin":  # macOS
            expected_path = (
                "/Applications/microchip/mplabx/v6.20/mplab_platform/mplab_ipe/ipecmd"
            )
        else:  # Linux and other Unix systems
            expected_path = (
                "/opt/microchip/mplabx/v6.20/mplab_platform/mplab_ipe/ipecmd"
            )

        assert path == expected_path

    @patch("sys.platform", "darwin")
    def test_get_ipecmd_path_macos(self):
        """Test getting IPECMD path on macOS"""
        path = get_ipecmd_path(version="6.20")
        expected_path = (
            "/Applications/microchip/mplabx/v6.20/mplab_platform/mplab_ipe/ipecmd"
        )
        assert path == expected_path

    @patch("sys.platform", "linux")
    def test_get_ipecmd_path_linux(self):
        """Test getting IPECMD path on Linux"""
        path = get_ipecmd_path(version="6.20")
        expected_path = "/opt/microchip/mplabx/v6.20/mplab_platform/mplab_ipe/ipecmd"
        assert path == expected_path

    def test_get_ipecmd_path_with_custom_path(self):
        """Test getting IPECMD path with custom path"""
        custom_path = "/custom/path/ipecmd"
        path = get_ipecmd_path(custom_path=custom_path)
        assert path == custom_path

    def test_get_ipecmd_path_no_version_or_path(self):
        """Test error when neither version nor path is provided"""
        with pytest.raises(
            ValueError, match="Either version or custom_path must be provided"
        ):
            get_ipecmd_path()


@pytest.mark.unit
@pytest.mark.core
class TestValidation:
    """Test validation functions"""

    @patch("pathlib.Path.exists")
    def test_validate_ipecmd_exists(self, mock_exists):
        """Test validation when IPECMD exists"""
        mock_exists.return_value = True
        result = validate_ipecmd("fake_path", "v6.20")
        assert result is True

    @patch("pathlib.Path.exists")
    @patch("ipecmd_wrapper.core.log")
    def test_validate_ipecmd_not_exists(self, mock_log, mock_exists):
        """Test validation when IPECMD doesn't exist"""
        mock_exists.return_value = False
        result = validate_ipecmd("fake_path", "v6.20")
        assert result is False
        # Check that error messages were logged
        assert mock_log.error.call_count >= 1

    @patch("pathlib.Path.exists")
    @patch("ipecmd_wrapper.core.log")
    def test_validate_ipecmd_not_exists_custom_path(self, mock_log, mock_exists):
        """Test validation when IPECMD doesn't exist with custom path"""
        mock_exists.return_value = False
        result = validate_ipecmd("fake_path", "custom path")
        assert result is False
        # Check that custom path error message was logged
        mock_log.warning.assert_any_call("Check the provided --ipecmd-path")

    @patch("pathlib.Path.exists")
    def test_validate_hex_file_exists(self, mock_exists):
        """Test validation when HEX file exists"""
        mock_exists.return_value = True
        result = validate_hex_file("fake_file.hex")
        assert result is True

    @patch("pathlib.Path.exists")
    def test_validate_hex_file_not_exists(self, mock_exists):
        """Test validation when HEX file doesn't exist"""
        mock_exists.return_value = False
        result = validate_hex_file("fake_file.hex")
        assert result is False


@pytest.mark.unit
@pytest.mark.core
class TestCommandBuilding:
    """Test command building functionality"""

    def test_build_ipecmd_command_basic(self):
        """Test building basic IPECMD command"""
        # Mock args object
        args = MagicMock()
        args.tool = "PK3"
        args.part = "PIC16F876A"
        args.file = "test.hex"
        args.memory = ""
        args.verify = ""
        args.power = "5.0"
        args.erase = False
        args.vdd_first = False
        args.logout = False

        cmd_args = build_ipecmd_command(args, "ipecmd.exe")

        expected_args = [
            "ipecmd.exe",
            "-TPPK3",
            "-PPIC16F876A",
            "-Ftest.hex",
            "-M",
            "-W5.0",
        ]

        assert cmd_args == expected_args

    def test_build_ipecmd_command_with_options(self):
        """Test building IPECMD command with additional options"""
        # Mock args object
        args = MagicMock()
        args.tool = "PK4"
        args.part = "PIC18F4550"
        args.file = "program.hex"
        args.memory = "P"
        args.verify = "P"
        args.power = "3.3"
        args.erase = True
        args.vdd_first = True
        args.logout = True

        cmd_args = build_ipecmd_command(args, "ipecmd.exe")

        expected_args = [
            "ipecmd.exe",
            "-TPPK4",
            "-PPIC18F4550",
            "-Fprogram.hex",
            "-MP",
            "-YP",
            "-W3.3",
            "-E",
            "-OD",
            "-OL",
        ]

        assert cmd_args == expected_args


@pytest.mark.unit
@pytest.mark.core
class TestConstants:
    """Test package constants"""

    def test_tool_choices_not_empty(self):
        """Test that TOOL_CHOICES is not empty"""
        assert len(TOOL_CHOICES) > 0
        assert "PK3" in TOOL_CHOICES
        assert "PK4" in TOOL_CHOICES

    def test_version_choices_not_empty(self):
        """Test that VERSION_CHOICES is not empty"""
        assert len(VERSION_CHOICES) > 0
        assert "5.50" in VERSION_CHOICES or "6.20" in VERSION_CHOICES

    def test_tool_map_consistency(self):
        """Test that TOOL_MAP is consistent with TOOL_CHOICES"""
        for tool in TOOL_CHOICES:
            assert tool in TOOL_MAP
            assert TOOL_MAP[tool].startswith("TP")


@pytest.mark.unit
@pytest.mark.core
class TestProgrammerDetection:
    """Test programmer detection functionality"""

    @patch("subprocess.run")
    def test_programmer_detection_success(self, mock_run):
        """Test successful programmer detection"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = detect_programmer("ipecmd.exe", "PIC16F876A", "PK3")
        assert result is True

    @patch("subprocess.run")
    @patch("ipecmd_wrapper.core.log")
    def test_programmer_detection_failure(self, mock_log, mock_run):
        """Test failed programmer detection"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Error message"
        mock_run.return_value = mock_result

        result = detect_programmer("ipecmd.exe", "PIC16F876A", "PK3")
        assert result is False
        # Verify error messages were logged
        mock_log.error.assert_any_call("Programmer detection failed!")
        mock_log.warning.assert_any_call("Check programmer connection and try again")

    @patch("subprocess.run")
    def test_programmer_detection_exception(self, mock_run):
        """Test programmer detection with exception"""
        mock_run.side_effect = Exception("Test exception")

        result = detect_programmer("ipecmd.exe", "PIC16F876A", "PK3")
        assert result is False


@pytest.mark.unit
@pytest.mark.core
class TestVersionSuggestions:
    """Test version suggestion functionality"""

    def test_get_version_suggestions_latest(self):
        """Test version suggestions when using latest version"""
        latest_version = VERSION_CHOICES[-1]
        suggestions = _get_version_suggestions(latest_version)

        # Should suggest previous version(s) only
        assert len(suggestions) <= 2
        if len(suggestions) > 0:
            assert suggestions[0] != latest_version

    def test_get_version_suggestions_middle(self):
        """Test version suggestions when using middle version"""
        if len(VERSION_CHOICES) >= 3:
            middle_version = VERSION_CHOICES[1]
            suggestions = _get_version_suggestions(middle_version)

            # Should suggest latest and previous/next versions
            assert len(suggestions) <= 2
            assert VERSION_CHOICES[-1] in suggestions  # Latest should be suggested

    def test_get_version_suggestions_first(self):
        """Test version suggestions when using first version"""
        first_version = VERSION_CHOICES[0]
        suggestions = _get_version_suggestions(first_version)

        # Should suggest latest and next version
        assert len(suggestions) <= 2
        assert VERSION_CHOICES[-1] in suggestions  # Latest should be suggested

    def test_get_version_suggestions_invalid(self):
        """Test version suggestions for invalid version"""
        suggestions = _get_version_suggestions("invalid_version")
        assert suggestions == []


@pytest.mark.unit
@pytest.mark.core
class TestExecuteProgramming:
    """Test programming execution functionality"""

    @patch("subprocess.run")
    @patch("ipecmd_wrapper.core.log")
    def test_execute_programming_success(self, mock_log, mock_run):
        """Test successful programming execution"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Programming successful"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        cmd_args = ["ipecmd.exe", "-TPPK3", "-PPIC16F876A", "-Ftest.hex"]
        result = execute_programming(cmd_args, "PIC16F876A", "PK3", "6.20")

        assert result is True
        mock_log.info.assert_any_call("SUCCESS! PIC PIC16F876A programmed!")

    @patch("subprocess.run")
    @patch("ipecmd_wrapper.core.log")
    @patch("ipecmd_wrapper.core._get_version_suggestions")
    def test_execute_programming_failure_with_suggestions(
        self, mock_suggestions, mock_log, mock_run
    ):
        """Test failed programming execution with version suggestions"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Programming failed"
        mock_run.return_value = mock_result

        mock_suggestions.return_value = ["6.25", "6.15"]

        cmd_args = ["ipecmd.exe", "-TPPK3", "-PPIC16F876A", "-Ftest.hex"]
        result = execute_programming(cmd_args, "PIC16F876A", "PK3", "6.20")

        assert result is False
        mock_log.error.assert_any_call("Programming error")
        mock_log.info.assert_any_call("You can also try with --ipecmd-version 6.25")
        mock_log.info.assert_any_call("You can also try with --ipecmd-version 6.15")

    @patch("subprocess.run")
    @patch("ipecmd_wrapper.core.log")
    def test_execute_programming_failure_no_version(self, mock_log, mock_run):
        """Test failed programming execution without version info"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Programming failed"
        mock_run.return_value = mock_result

        cmd_args = ["ipecmd.exe", "-TPPK3", "-PPIC16F876A", "-Ftest.hex"]
        result = execute_programming(cmd_args, "PIC16F876A", "PK3", None)

        assert result is False
        mock_log.error.assert_any_call("Programming error")

    @patch("subprocess.run")
    @patch("ipecmd_wrapper.core.log")
    def test_execute_programming_exception(self, mock_log, mock_run):
        """Test programming execution with exception"""
        mock_run.side_effect = Exception("Command failed")

        cmd_args = ["ipecmd.exe", "-TPPK3", "-PPIC16F876A", "-Ftest.hex"]
        result = execute_programming(cmd_args, "PIC16F876A", "PK3", "6.20")

        assert result is False
        mock_log.error.assert_any_call(
            "Error running programming command: Command failed"
        )


@pytest.mark.unit
@pytest.mark.core
class TestProgramPic:
    """Test main program_pic function"""

    @patch("ipecmd_wrapper.core.validate_hex_file")
    @patch("ipecmd_wrapper.core.validate_ipecmd")
    @patch("ipecmd_wrapper.core.get_ipecmd_path")
    @patch("ipecmd_wrapper.core.detect_programmer")
    @patch("ipecmd_wrapper.core.build_ipecmd_command")
    @patch("ipecmd_wrapper.core.execute_programming")
    @patch("sys.exit")
    def test_program_pic_success_with_custom_path(
        self,
        mock_exit,
        mock_execute,
        mock_build,
        mock_detect,
        mock_get_path,
        mock_validate_ipecmd,
        mock_validate_hex,
    ):
        """Test successful program_pic with custom IPECMD path"""
        # Setup mocks
        mock_validate_hex.return_value = True
        mock_validate_ipecmd.return_value = True
        mock_detect.return_value = True
        mock_build.return_value = ["ipecmd.exe", "-TPPK3", "-PPIC16F876A", "-Ftest.hex"]
        mock_execute.return_value = True

        # Mock args
        args = MagicMock()
        args.ipecmd_path = "/custom/ipecmd.exe"
        args.file = "test.hex"
        args.tool = "PK3"
        args.part = "PIC16F876A"
        args.power = "5.0"
        args.test_programmer = True
        args.ipecmd_version = "6.20"
        args.memory = ""
        args.verify = ""
        args.erase = False
        args.vdd_first = False
        args.logout = False

        program_pic(args)

        # Verify functions were called
        mock_validate_hex.assert_called_once_with("test.hex")
        mock_validate_ipecmd.assert_called_once_with(
            "/custom/ipecmd.exe", "custom path"
        )
        mock_detect.assert_called_once()
        mock_execute.assert_called_once()
        mock_exit.assert_not_called()

    @patch("ipecmd_wrapper.core.validate_hex_file")
    @patch("ipecmd_wrapper.core.validate_ipecmd")
    @patch("ipecmd_wrapper.core.get_ipecmd_path")
    @patch("ipecmd_wrapper.core.build_ipecmd_command")
    @patch("ipecmd_wrapper.core.execute_programming")
    @patch("sys.exit")
    def test_program_pic_success_with_version(
        self,
        mock_exit,
        mock_execute,
        mock_build,
        mock_get_path,
        mock_validate_ipecmd,
        mock_validate_hex,
    ):
        """Test successful program_pic with IPECMD version"""
        # Setup mocks
        mock_validate_hex.return_value = True
        mock_validate_ipecmd.return_value = True
        mock_get_path.return_value = (
            "/opt/microchip/mplabx/v6.20/mplab_platform/mplab_ipe/ipecmd"
        )
        mock_build.return_value = ["ipecmd", "-TPPK3", "-PPIC16F876A", "-Ftest.hex"]
        mock_execute.return_value = True

        # Mock args
        args = MagicMock()
        args.ipecmd_path = None
        args.ipecmd_version = "6.20"
        args.file = "test.hex"
        args.tool = "PK3"
        args.part = "PIC16F876A"
        args.power = "5.0"
        args.test_programmer = False
        args.memory = ""
        args.verify = ""
        args.erase = False
        args.vdd_first = False
        args.logout = False

        program_pic(args)

        # Verify functions were called
        mock_get_path.assert_called_once_with(version="6.20")
        mock_validate_ipecmd.assert_called_once_with(
            "/opt/microchip/mplabx/v6.20/mplab_platform/mplab_ipe/ipecmd", "v6.20"
        )
        mock_execute.assert_called_once()
        mock_exit.assert_not_called()

    @patch("ipecmd_wrapper.core.validate_hex_file")
    @patch("sys.exit")
    def test_program_pic_hex_validation_fails(self, mock_exit, mock_validate_hex):
        """Test program_pic when HEX file validation fails"""
        mock_validate_hex.return_value = False

        # Mock sys.exit to stop execution
        mock_exit.side_effect = SystemExit(1)

        args = MagicMock()
        args.file = "nonexistent.hex"
        args.tool = "PK3"
        args.part = "PIC16F876A"
        args.power = "5.0"
        args.test_programmer = False
        args.ipecmd_path = "/path/to/ipecmd"
        args.ipecmd_version = "6.20"
        args.memory = ""
        args.verify = ""
        args.erase = False
        args.vdd_first = False
        args.logout = False

        with pytest.raises(SystemExit):
            program_pic(args)

        mock_exit.assert_called_once_with(1)

    @patch("ipecmd_wrapper.core.validate_hex_file")
    @patch("ipecmd_wrapper.core.validate_ipecmd")
    @patch("ipecmd_wrapper.core.get_ipecmd_path")
    @patch("sys.exit")
    def test_program_pic_ipecmd_validation_fails(
        self, mock_exit, mock_get_path, mock_validate_ipecmd, mock_validate_hex
    ):
        """Test program_pic when IPECMD validation fails"""
        mock_validate_hex.return_value = True
        mock_validate_ipecmd.return_value = False
        mock_get_path.return_value = "/invalid/path/ipecmd"

        # Mock sys.exit to stop execution
        mock_exit.side_effect = SystemExit(1)

        args = MagicMock()
        args.ipecmd_path = None
        args.ipecmd_version = "6.20"
        args.file = "test.hex"
        args.tool = "PK3"
        args.part = "PIC16F876A"
        args.power = "5.0"
        args.test_programmer = False
        args.memory = ""
        args.verify = ""
        args.erase = False
        args.vdd_first = False
        args.logout = False

        with pytest.raises(SystemExit):
            program_pic(args)

        mock_exit.assert_called_once_with(1)

    @patch("ipecmd_wrapper.core.validate_hex_file")
    @patch("ipecmd_wrapper.core.validate_ipecmd")
    @patch("ipecmd_wrapper.core.get_ipecmd_path")
    @patch("ipecmd_wrapper.core.detect_programmer")
    @patch("sys.exit")
    def test_program_pic_programmer_detection_fails(
        self,
        mock_exit,
        mock_detect,
        mock_get_path,
        mock_validate_ipecmd,
        mock_validate_hex,
    ):
        """Test program_pic when programmer detection fails"""
        mock_validate_hex.return_value = True
        mock_validate_ipecmd.return_value = True
        mock_get_path.return_value = "/path/ipecmd"
        mock_detect.return_value = False

        # Mock sys.exit to stop execution
        mock_exit.side_effect = SystemExit(1)

        args = MagicMock()
        args.ipecmd_path = None
        args.ipecmd_version = "6.20"
        args.file = "test.hex"
        args.tool = "PK3"
        args.part = "PIC16F876A"
        args.power = "5.0"
        args.test_programmer = True
        args.memory = ""
        args.verify = ""
        args.erase = False
        args.vdd_first = False
        args.logout = False

        with pytest.raises(SystemExit):
            program_pic(args)

        mock_exit.assert_called_once_with(1)

    @patch("ipecmd_wrapper.core.validate_hex_file")
    @patch("ipecmd_wrapper.core.validate_ipecmd")
    @patch("ipecmd_wrapper.core.get_ipecmd_path")
    @patch("ipecmd_wrapper.core.build_ipecmd_command")
    @patch("ipecmd_wrapper.core.execute_programming")
    @patch("sys.exit")
    def test_program_pic_programming_fails(
        self,
        mock_exit,
        mock_execute,
        mock_build,
        mock_get_path,
        mock_validate_ipecmd,
        mock_validate_hex,
    ):
        """Test program_pic when programming execution fails"""
        mock_validate_hex.return_value = True
        mock_validate_ipecmd.return_value = True
        mock_get_path.return_value = "/path/ipecmd"
        mock_build.return_value = ["ipecmd", "-TPPK3", "-PPIC16F876A", "-Ftest.hex"]
        mock_execute.return_value = False

        # Mock sys.exit to stop execution
        mock_exit.side_effect = SystemExit(1)

        args = MagicMock()
        args.ipecmd_path = None
        args.ipecmd_version = "6.20"
        args.file = "test.hex"
        args.tool = "PK3"
        args.part = "PIC16F876A"
        args.power = "5.0"
        args.test_programmer = False
        args.memory = ""
        args.verify = ""
        args.erase = False
        args.vdd_first = False
        args.logout = False

        with pytest.raises(SystemExit):
            program_pic(args)

        mock_exit.assert_called_once_with(1)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.unit
@pytest.mark.core
class TestUtilities:
    """Test utility functions"""

    def test_placeholder(self):
        """Placeholder test to keep the class structure"""
        assert True


if __name__ == "__main__":
    pytest.main([__file__])
