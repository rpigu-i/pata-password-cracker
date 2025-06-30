"""
Integration tests for the complete pata-password-cracker workflow.
"""
import pytest
import tempfile
import os
from unittest.mock import patch, Mock
from pata_password_cracker.__main__ import main, process_input, generate_password_list


class TestIntegration:
    """Integration tests for the complete workflow."""
    
    @patch('pata_password_cracker.__main__.generate_password_list')
    @patch('sys.argv', ['pata_password_cracker', 'test.yaml', 'words.txt', 'md5'])
    def test_main_integration(self, mock_generate, temp_yaml_file, temp_words_file):
        """Test complete main function integration."""
        # Create temporary files for the test
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as yaml_f:
            yaml_f.write("""
individuals:
- John Doe:
    - core_bio:
        first_name: John
        last_name: Doe
        dob: 1990-01-01
    - free_data:
        pet: cat
""")
            yaml_f.flush()
            yaml_file = yaml_f.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as words_f:
            words_f.write("test\nword\nlist")
            words_f.flush()
            words_file = words_f.name
        
        try:
            # Mock sys.argv to use our temp files
            with patch('sys.argv', ['pata_password_cracker', yaml_file, words_file, 'md5']):
                with patch('pata_password_cracker.__main__.Logo') as mock_logo:
                    main()
            
            # Should call generate_password_list for each individual
            mock_generate.assert_called()
            mock_logo.assert_called_once()
        finally:
            os.unlink(yaml_file)
            os.unlink(words_file)
    
    @patch('pata_password_cracker.__main__.Categories')
    @patch('pata_password_cracker.__main__.ProcessOutputYaml')
    def test_generate_password_list_integration(self, mock_output_class, mock_categories_class):
        """Test generate_password_list integration."""
        # Mock Categories
        mock_categories_instance = Mock()
        mock_categories_instance.process_categories.return_value = {'passwords': ['test123', 'test456']}
        mock_categories_class.return_value = mock_categories_instance
        
        # Mock ProcessOutputYaml
        mock_output_instance = Mock()
        mock_output_class.return_value = mock_output_instance
        
        # Test data
        individual = {'John Doe': [{'core_bio': {'first_name': 'John'}}]}
        words_list = ['test', 'word']
        plugins = {'pata_password_cracker.encryption': ['md5']}
        
        # Call the function
        generate_password_list(individual, words_list, plugins)
        
        # Verify the workflow
        mock_categories_class.assert_called_once_with(individual, words_list, plugins)
        mock_categories_instance.process_categories.assert_called_once()
        mock_output_class.assert_called_once()
        mock_output_instance.output_processor.assert_called_once_with({'passwords': ['test123', 'test456']})
    
    def test_end_to_end_with_real_components(self):
        """Test end-to-end with real components (minimal external dependencies)."""
        from pata_password_cracker.input import ProcessInputYaml, ProcessInputWords
        from pata_password_cracker.output import ProcessOutputYaml
        from pata_password_cracker.encryption.md5 import MD5Encryption
        from pata_password_cracker.substitutors.simple import MungSubstitutor
        
        # Create test files
        yaml_content = """
individuals:
- TestUser:
    - free_data:
        pet: cat
        hobby: reading
"""
        words_content = "test\nword\nsample"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as yaml_f:
            yaml_f.write(yaml_content)
            yaml_f.flush()
            yaml_file = yaml_f.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as words_f:
            words_f.write(words_content)
            words_f.flush()
            words_file = words_f.name
        
        try:
            # Test input processing
            yaml_processor = ProcessInputYaml()
            yaml_data = list(yaml_processor.yaml_processor(yaml_file))
            
            words_processor = ProcessInputWords()
            words_data = words_processor.words_processor(words_file)
            
            # Verify input processing
            assert len(yaml_data) == 1
            assert 'individuals' in yaml_data[0]
            assert len(words_data) == 3
            assert 'test' in words_data
            
            # Test that components can be instantiated
            md5_enc = MD5Encryption()
            simple_sub = MungSubstitutor()
            
            # Test basic functionality
            hash_result = md5_enc.hash("test")
            assert isinstance(hash_result, str)
            assert len(hash_result) == 32  # MD5 hex length
            
            sub_result = simple_sub.substitute("test")
            assert isinstance(sub_result, str)
            
        finally:
            os.unlink(yaml_file)
            os.unlink(words_file)
    
    def test_plugin_system_integration(self):
        """Test that the plugin system works correctly."""
        from pata_password_cracker.categories import Categories
        
        # Test with minimal data that doesn't require external patalib
        bio_data = {'TestUser': [{'unknown_category': {'data': 'value'}}]}
        words = ['test']
        plugins = {'pata_password_cracker.encryption': ['md5']}
        
        # This should not crash even with unknown category
        categories = Categories(bio_data, words, plugins)
        result = categories.process_categories()
        
        # Should return processed data structure
        assert isinstance(result, dict)
        
        # Should have loaded some plugins
        assert hasattr(categories, 'loaded_encryption_plugin_dict')
        assert hasattr(categories, 'loaded_cat_plugin_dict')
        assert hasattr(categories, 'loaded_substitutors_plugin_dict')
    
    @patch('pata_password_cracker.output.yaml.dump')
    @patch('builtins.open')
    def test_output_integration(self, mock_open, mock_yaml_dump):
        """Test output processing integration."""
        from pata_password_cracker.output import ProcessOutputYaml
        
        processor = ProcessOutputYaml()
        test_data = {
            'user1': {
                'passwords': {
                    'clear_text': ['password123', 'secret456'],
                    'encrypted': {'md5': ['hash1', 'hash2']}
                }
            }
        }
        
        processor.output_processor(test_data)
        
        # Should open file for writing
        mock_open.assert_called_once_with('passwords.yaml', 'w')
        
        # Should call yaml.dump with the data
        mock_yaml_dump.assert_called_once()