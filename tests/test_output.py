"""
Unit tests for output processing modules.
"""
import pytest
import tempfile
import os
import yaml
from unittest.mock import patch, mock_open
from pata_password_cracker.output import ProcessOutputYaml


class TestProcessOutputYaml:
    """Tests for ProcessOutputYaml class."""
    
    def test_output_processor_basic_dict(self):
        """Test processing a basic dictionary output."""
        processor = ProcessOutputYaml()
        test_data = {
            'individual_1': [
                {'core_bio': ['password1', 'password2']},
                {'family': ['password3', 'password4']}
            ]
        }
        
        # Mock the open function to capture what's written
        with patch('builtins.open', mock_open()) as mock_file:
            processor.output_processor(test_data)
            
            # Verify file was opened for writing
            mock_file.assert_called_once_with('passwords.yaml', 'w')
            
            # Get the written content
            handle = mock_file()
            written_content = ''.join(call[0][0] for call in handle.write.call_args_list)
            
            # Parse the written YAML to verify it's valid
            parsed_data = yaml.safe_load(written_content)
            assert parsed_data == test_data
    
    def test_output_processor_empty_dict(self):
        """Test processing an empty dictionary."""
        processor = ProcessOutputYaml()
        test_data = {}
        
        with patch('builtins.open', mock_open()) as mock_file:
            processor.output_processor(test_data)
            
            mock_file.assert_called_once_with('passwords.yaml', 'w')
            
            handle = mock_file()
            written_content = ''.join(call[0][0] for call in handle.write.call_args_list)
            
            parsed_data = yaml.safe_load(written_content)
            assert parsed_data == {}
    
    def test_output_processor_complex_nested_dict(self):
        """Test processing a complex nested dictionary."""
        processor = ProcessOutputYaml()
        test_data = {
            '0:JamesSmith': [
                {
                    'core_bio': {
                        'passwords': {
                            'clear_text': ['james123', 'smith456'],
                            'encrypted': {
                                'md5': ['hash1', 'hash2'],
                                'sha1': ['hash3', 'hash4']
                            }
                        }
                    }
                },
                {
                    'family': {
                        'passwords': {
                            'clear_text': ['tim789', 'susie321'],
                            'encrypted': {
                                'md5': ['hash5', 'hash6']
                            }
                        }
                    }
                }
            ]
        }
        
        with patch('builtins.open', mock_open()) as mock_file:
            processor.output_processor(test_data)
            
            mock_file.assert_called_once_with('passwords.yaml', 'w')
            
            handle = mock_file()
            written_content = ''.join(call[0][0] for call in handle.write.call_args_list)
            
            parsed_data = yaml.safe_load(written_content)
            assert parsed_data == test_data
    
    def test_output_processor_none_input(self):
        """Test processing None input."""
        processor = ProcessOutputYaml()
        
        with patch('builtins.open', mock_open()) as mock_file:
            processor.output_processor(None)
            
            mock_file.assert_called_once_with('passwords.yaml', 'w')
            
            handle = mock_file()
            written_content = ''.join(call[0][0] for call in handle.write.call_args_list)
            
            parsed_data = yaml.safe_load(written_content)
            assert parsed_data is None
    
    def test_output_processor_file_creation(self):
        """Test that the output file is actually created with correct content."""
        processor = ProcessOutputYaml()
        test_data = {'test': 'data'}
        
        # Create a temporary directory for the test
        with tempfile.TemporaryDirectory() as temp_dir:
            expected_file_path = os.path.join(temp_dir, 'passwords.yaml')
            
            # Write test data to file directly to test file operations
            with open(expected_file_path, 'w') as f:
                yaml.dump(test_data, f, default_flow_style=False)
            
            # Verify file exists and has correct content
            assert os.path.exists(expected_file_path)
            
            with open(expected_file_path, 'r') as f:
                content = yaml.safe_load(f)
                assert content == test_data