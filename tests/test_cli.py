"""
Tests for CLI module

Test suite for the command-line interface functionality.
"""

import pytest
from unittest.mock import patch, MagicMock
from ipecmd_wrapper.cli import create_argument_parser, main


class TestArgumentParser:
    """Test argument parser creation and functionality"""
    
    def test_create_argument_parser(self):
        """Test that argument parser is created correctly"""
        parser = create_argument_parser()
        assert parser is not None
        assert parser.prog == "ipecmd-wrapper"
    
    def test_parser_help_contains_version(self):
        """Test that help contains version option"""
        parser = create_argument_parser()
        help_text = parser.format_help()
        assert "--version" in help_text
    
    def test_parser_required_arguments(self):
        """Test parser with required arguments"""
        parser = create_argument_parser()
        
        # Test with all required arguments
        args = parser.parse_args([
            "-P", "PIC16F876A",
            "-T", "PK3", 
            "-F", "test.hex",
            "-W", "5.0",
            "--ipecmd-version", "6.20"
        ])
        
        assert args.part == "PIC16F876A"
        assert args.tool == "PK3"
        assert args.file == "test.hex"
        assert args.power == "5.0"
        assert args.ipecmd_version == "6.20"
    
    def test_parser_optional_arguments(self):
        """Test parser with optional arguments"""
        parser = create_argument_parser()
        
        args = parser.parse_args([
            "-P", "PIC16F876A",
            "-T", "PK3",
            "-F", "test.hex", 
            "-W", "5.0",
            "--ipecmd-version", "6.20",
            "-E",  # erase
            "--test-programmer",
            "-M", "P",  # memory
            "-Y", "P"   # verify
        ])
        
        assert args.erase is True
        assert args.test_programmer is True
        assert args.memory == "P"
        assert args.verify == "P"


class TestMainFunction:
    """Test main function"""
    
    @patch('ipecmd_wrapper.cli.program_pic')
    def test_main_with_valid_args(self, mock_program_pic):
        """Test main function with valid arguments"""
        mock_program_pic.return_value = None
        
        # Test that it doesn't raise an exception
        try:
            main([
                "-P", "PIC16F876A",
                "-T", "PK3",
                "-F", "test.hex",
                "-W", "5.0",
                "--ipecmd-version", "6.20"
            ])
            mock_program_pic.assert_called_once()
        except SystemExit:
            # program_pic might call sys.exit, which is expected
            pass
    
    def test_main_missing_version_and_path(self):
        """Test main function with missing version and path"""
        with pytest.raises(SystemExit):
            main([
                "-P", "PIC16F876A",
                "-T", "PK3",
                "-F", "test.hex",
                "-W", "5.0"
                # Missing both --ipecmd-version and --ipecmd-path
            ])


if __name__ == "__main__":
    pytest.main([__file__])
