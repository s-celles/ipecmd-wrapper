"""
Tests for IPECMD Wrapper Core

Basic test suite for the IPECMD wrapper core functionality.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from ipecmd_wrapper.core import (
    get_ipecmd_path, 
    validate_ipecmd, 
    validate_hex_file,
    build_ipecmd_command,
    test_programmer_detection,
    TOOL_CHOICES, 
    VERSION_CHOICES, 
    TOOL_MAP
)


class TestIPECMDPath:
    """Test IPECMD path resolution"""
    
    def test_get_ipecmd_path_with_version(self):
        """Test getting IPECMD path with version"""
        path = get_ipecmd_path(version="6.20")
        expected_path = r"C:\Program Files\Microchip\MPLABX\v6.20\mplab_platform\mplab_ipe\ipecmd.exe"
        assert path == expected_path
    
    def test_get_ipecmd_path_with_custom_path(self):
        """Test getting IPECMD path with custom path"""
        custom_path = r"C:\custom\path\ipecmd.exe"
        path = get_ipecmd_path(custom_path=custom_path)
        assert path == custom_path
    
    def test_get_ipecmd_path_no_version_or_path(self):
        """Test error when neither version nor path is provided"""
        with pytest.raises(ValueError, match="Either version or custom_path must be provided"):
            get_ipecmd_path()


class TestValidation:
    """Test validation functions"""
    
    @patch('os.path.exists')
    def test_validate_ipecmd_exists(self, mock_exists):
        """Test validation when IPECMD exists"""
        mock_exists.return_value = True
        result = validate_ipecmd("fake_path", "v6.20")
        assert result is True
    
    @patch('os.path.exists')
    def test_validate_ipecmd_not_exists(self, mock_exists):
        """Test validation when IPECMD doesn't exist"""
        mock_exists.return_value = False
        result = validate_ipecmd("fake_path", "v6.20")
        assert result is False
    
    @patch('os.path.exists')
    def test_validate_hex_file_exists(self, mock_exists):
        """Test validation when HEX file exists"""
        mock_exists.return_value = True
        result = validate_hex_file("fake_file.hex")
        assert result is True
    
    @patch('os.path.exists')
    def test_validate_hex_file_not_exists(self, mock_exists):
        """Test validation when HEX file doesn't exist"""
        mock_exists.return_value = False
        result = validate_hex_file("fake_file.hex")
        assert result is False


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
            "-W5.0"
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
            "-OL"
        ]
        
        assert cmd_args == expected_args


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


class TestProgrammerDetection:
    """Test programmer detection functionality"""
    
    @patch('subprocess.run')
    def test_programmer_detection_success(self, mock_run):
        """Test successful programmer detection"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        result = test_programmer_detection("ipecmd.exe", "PIC16F876A", "PK3")
        assert result is True
    
    @patch('subprocess.run')
    def test_programmer_detection_failure(self, mock_run):
        """Test failed programmer detection"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Error message"
        mock_run.return_value = mock_result
        
        result = test_programmer_detection("ipecmd.exe", "PIC16F876A", "PK3")
        assert result is False
    
    @patch('subprocess.run')
    def test_programmer_detection_exception(self, mock_run):
        """Test programmer detection with exception"""
        mock_run.side_effect = Exception("Test exception")
        
        result = test_programmer_detection("ipecmd.exe", "PIC16F876A", "PK3")
        assert result is False


if __name__ == "__main__":
    pytest.main([__file__])
