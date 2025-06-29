"""
Unit tests for logo generator module.
"""
import pytest
from unittest.mock import patch
from pata_password_cracker.gen_logo import Logo


class TestLogo:
    """Tests for Logo class."""
    
    @patch('builtins.print')
    def test_generate_logo_calls_print(self, mock_print):
        """Test that generate_logo calls print with ASCII art."""
        logo = Logo()
        logo.generate_logo()
        
        # Should call print multiple times
        assert mock_print.call_count > 0
        
        # Check that some expected text is printed
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        
        # Should contain parts of the ASCII art
        assert any("Pata" in call for call in print_calls)
        assert any("Cracker" in call for call in print_calls)
    
    @patch('builtins.print')
    def test_generate_logo_complete_output(self, mock_print):
        """Test that generate_logo outputs complete ASCII art."""
        logo = Logo()
        logo.generate_logo()
        
        # Should print a reasonable number of lines
        assert mock_print.call_count >= 20  # ASCII art has many lines
    
    @patch('builtins.print')
    def test_generate_logo_contains_quote(self, mock_print):
        """Test that generate_logo contains the Jarry quote."""
        logo = Logo()
        logo.generate_logo()
        
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        
        # Should contain the Jarry quote
        assert any("Pataphysics" in call for call in print_calls)
        assert any("metaphysics" in call for call in print_calls)
        assert any("A. Jarry" in call for call in print_calls)
    
    @patch('builtins.print')
    def test_generate_logo_contains_attribution(self, mock_print):
        """Test that generate_logo contains attribution."""
        logo = Logo()
        logo.generate_logo()
        
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        
        # Should contain attribution
        assert any("LesPatamechanix" in call for call in print_calls)
    
    def test_generate_logo_no_exceptions(self):
        """Test that generate_logo doesn't raise exceptions."""
        logo = Logo()
        # Should not raise any exceptions
        logo.generate_logo()
    
    def test_logo_initialization(self):
        """Test Logo class initialization."""
        logo = Logo()
        assert isinstance(logo, Logo)
        assert hasattr(logo, 'generate_logo')
    
    @patch('builtins.print')
    def test_generate_logo_consistent_output(self, mock_print):
        """Test that generate_logo produces consistent output."""
        logo = Logo()
        
        # Call twice and compare
        logo.generate_logo()
        first_call_count = mock_print.call_count
        first_calls = [call[0][0] for call in mock_print.call_args_list]
        
        mock_print.reset_mock()
        
        logo.generate_logo()
        second_call_count = mock_print.call_count
        second_calls = [call[0][0] for call in mock_print.call_args_list]
        
        # Should have same number of calls and same content
        assert first_call_count == second_call_count
        assert first_calls == second_calls
    
    @patch('builtins.print')
    def test_generate_logo_all_lines_are_strings(self, mock_print):
        """Test that all printed lines are strings."""
        logo = Logo()
        logo.generate_logo()
        
        # All print calls should be with string arguments
        for call in mock_print.call_args_list:
            assert len(call[0]) == 1  # Single argument
            assert isinstance(call[0][0], str)  # String argument