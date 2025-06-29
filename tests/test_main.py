"""
Unit tests for main module functions.
"""
import pytest
from unittest.mock import patch, Mock, MagicMock
import argparse
from pata_password_cracker.__main__ import (
    plugin_processor, 
    process_input,
    generate_password_list
)


class TestPluginProcessor:
    """Tests for plugin_processor function."""
    
    def test_plugin_processor_single_plugin(self):
        """Test processing single plugin."""
        result = plugin_processor('pata_password_cracker.encryption', 'md5')
        expected = {'pata_password_cracker.encryption': ['md5']}
        assert result == expected
    
    def test_plugin_processor_multiple_plugins(self):
        """Test processing multiple plugins."""
        result = plugin_processor('pata_password_cracker.encryption', 'md5,sha1,sha256')
        expected = {'pata_password_cracker.encryption': ['md5', 'sha1', 'sha256']}
        assert result == expected
    
    def test_plugin_processor_empty_plugins(self):
        """Test processing empty plugin list."""
        result = plugin_processor('pata_password_cracker.encryption', '')
        expected = {'pata_password_cracker.encryption': ['']}
        assert result == expected
    
    def test_plugin_processor_different_category(self):
        """Test processing with different category."""
        result = plugin_processor('pata_password_cracker.substitutors', 'simple,common')
        expected = {'pata_password_cracker.substitutors': ['simple', 'common']}
        assert result == expected


class TestProcessInput:
    """Tests for process_input function."""
    
    @patch('pata_password_cracker.__main__.generate_password_list')
    @patch('pata_password_cracker.__main__.ProcessInputWords')
    @patch('pata_password_cracker.__main__.ProcessInputYaml')
    @patch('builtins.print')
    def test_process_input_basic(self, mock_print, mock_yaml_class, mock_words_class, mock_generate):
        """Test basic process_input functionality."""
        # Mock the YAML processor
        mock_yaml_instance = Mock()
        mock_yaml_instance.yaml_processor.return_value = [
            {
                'individuals': [
                    {'John Doe': 'john_data'},
                    {'Jane Smith': 'jane_data'}
                ]
            }
        ]
        mock_yaml_class.return_value = mock_yaml_instance
        
        # Mock the words processor
        mock_words_instance = Mock()
        mock_words_instance.words_processor.return_value = ['word1', 'word2']
        mock_words_class.return_value = mock_words_instance
        
        # Call the function
        plugins = {'pata_password_cracker.encryption': ['md5']}
        process_input('test.yaml', 'words.txt', plugins)
        
        # Verify calls
        mock_print.assert_called_with("Processing input YAML")
        mock_yaml_instance.yaml_processor.assert_called_once_with('test.yaml')
        mock_words_instance.words_processor.assert_called_once_with('words.txt')
        
        # Should call generate_password_list for each individual
        assert mock_generate.call_count == 2
        mock_generate.assert_any_call({'John Doe': 'john_data'}, ['word1', 'word2'], plugins)
        mock_generate.assert_any_call({'Jane Smith': 'jane_data'}, ['word1', 'word2'], plugins)
    
    @patch('pata_password_cracker.__main__.generate_password_list')
    @patch('pata_password_cracker.__main__.ProcessInputWords')
    @patch('pata_password_cracker.__main__.ProcessInputYaml')
    @patch('builtins.print')
    def test_process_input_empty_individuals(self, mock_print, mock_yaml_class, mock_words_class, mock_generate):
        """Test process_input with empty individuals list."""
        # Mock empty individuals
        mock_yaml_instance = Mock()
        mock_yaml_instance.yaml_processor.return_value = [
            {'individuals': []}
        ]
        mock_yaml_class.return_value = mock_yaml_instance
        
        mock_words_instance = Mock()
        mock_words_instance.words_processor.return_value = ['word1']
        mock_words_class.return_value = mock_words_instance
        
        plugins = {'pata_password_cracker.encryption': ['md5']}
        process_input('test.yaml', 'words.txt', plugins)
        
        # Should not call generate_password_list
        mock_generate.assert_not_called()
    
    @patch('pata_password_cracker.__main__.generate_password_list')
    @patch('pata_password_cracker.__main__.ProcessInputWords')
    @patch('pata_password_cracker.__main__.ProcessInputYaml')
    @patch('builtins.print')
    def test_process_input_multiple_document_sections(self, mock_print, mock_yaml_class, mock_words_class, mock_generate):
        """Test process_input with multiple document sections."""
        # Mock multiple document sections
        mock_yaml_instance = Mock()
        mock_yaml_instance.yaml_processor.return_value = [
            {'individuals': [{'Person1': 'data1'}]},
            {'individuals': [{'Person2': 'data2'}]}
        ]
        mock_yaml_class.return_value = mock_yaml_instance
        
        mock_words_instance = Mock()
        mock_words_instance.words_processor.return_value = ['word1']
        mock_words_class.return_value = mock_words_instance
        
        plugins = {'pata_password_cracker.encryption': ['md5']}
        process_input('test.yaml', 'words.txt', plugins)
        
        # Should call generate_password_list for individuals in both sections
        assert mock_generate.call_count == 2


class TestGeneratePasswordList:
    """Tests for generate_password_list function."""
    
    @patch('pata_password_cracker.__main__.ProcessOutputYaml')
    @patch('pata_password_cracker.__main__.Categories')
    def test_generate_password_list_basic(self, mock_categories_class, mock_output_class):
        """Test basic generate_password_list functionality."""
        # Mock Categories
        mock_categories_instance = Mock()
        mock_categories_instance.process_categories.return_value = {'passwords': 'test_data'}
        mock_categories_class.return_value = mock_categories_instance
        
        # Mock ProcessOutputYaml
        mock_output_instance = Mock()
        mock_output_class.return_value = mock_output_instance
        
        # Call the function
        individual = {'John Doe': 'test_data'}
        words_list = ['word1', 'word2']
        plugins = {'pata_password_cracker.encryption': ['md5']}
        
        generate_password_list(individual, words_list, plugins)
        
        # Verify Categories was called correctly
        mock_categories_class.assert_called_once_with(individual, words_list, plugins)
        mock_categories_instance.process_categories.assert_called_once()
        
        # Verify output processor was called
        mock_output_class.assert_called_once()
        mock_output_instance.output_processor.assert_called_once_with({'passwords': 'test_data'})
    
    @patch('pata_password_cracker.__main__.ProcessOutputYaml')
    @patch('pata_password_cracker.__main__.Categories')
    def test_generate_password_list_empty_data(self, mock_categories_class, mock_output_class):
        """Test generate_password_list with empty data."""
        # Mock Categories returning empty data
        mock_categories_instance = Mock()
        mock_categories_instance.process_categories.return_value = {}
        mock_categories_class.return_value = mock_categories_instance
        
        mock_output_instance = Mock()
        mock_output_class.return_value = mock_output_instance
        
        individual = {}
        words_list = []
        plugins = {}
        
        generate_password_list(individual, words_list, plugins)
        
        # Should still process the empty data
        mock_categories_class.assert_called_once_with(individual, words_list, plugins)
        mock_output_instance.output_processor.assert_called_once_with({})


class TestMainFunction:
    """Tests for main function integration."""
    
    @patch('pata_password_cracker.__main__.process_input')
    @patch('pata_password_cracker.__main__.plugin_processor')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('pata_password_cracker.__main__.Logo')
    def test_main_function_argument_parsing(self, mock_logo_class, mock_parse_args, mock_plugin_processor, mock_process_input):
        """Test main function argument parsing and flow."""
        from pata_password_cracker.__main__ import main
        
        # Mock Logo
        mock_logo_instance = Mock()
        mock_logo_class.return_value = mock_logo_instance
        
        # Mock argument parsing
        mock_args = Mock()
        mock_args.yaml = 'test.yaml'
        mock_args.words = 'words.txt'
        mock_args.encryption = 'md5,sha1'
        mock_parse_args.return_value = mock_args
        
        # Mock plugin processor
        mock_plugin_processor.return_value = {'pata_password_cracker.encryption': ['md5', 'sha1']}
        
        # Call main
        main()
        
        # Verify Logo was called
        mock_logo_class.assert_called_once()
        mock_logo_instance.generate_logo.assert_called_once()
        
        # Verify plugin processor was called
        mock_plugin_processor.assert_called_once_with('pata_password_cracker.encryption', 'md5,sha1')
        
        # Verify process_input was called
        mock_process_input.assert_called_once_with(
            'test.yaml', 
            'words.txt', 
            {'pata_password_cracker.encryption': ['md5', 'sha1']}
        )