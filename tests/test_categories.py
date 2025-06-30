"""
Unit tests for categories module.
"""
import pytest
from unittest.mock import patch, Mock, MagicMock
from pata_password_cracker.categories import Categories


class TestCategories:
    """Tests for Categories class."""
    
    @patch('pata_password_cracker.categories.pkg_resources.iter_entry_points')
    def test_init_basic(self, mock_iter_entry_points):
        """Test basic Categories initialization."""
        # Mock entry points
        mock_entry_point = Mock()
        mock_entry_point.name = 'test_plugin'
        mock_entry_point.load.return_value = Mock
        mock_iter_entry_points.return_value = [mock_entry_point]
        
        bio_data = {'John Doe': [{'core_bio': {'name': 'John'}}]}
        words = ['word1', 'word2']
        plugins = {'pata_password_cracker.encryption': ['md5']}
        
        categories = Categories(bio_data, words, plugins)
        
        assert categories.bio_data == bio_data
        assert categories.words == words
        assert categories.inc_plugins == plugins
        
        # Should call iter_entry_points for each plugin type
        assert mock_iter_entry_points.call_count == 3  # category, encryption, substitutors
    
    @patch('pata_password_cracker.categories.pkg_resources.iter_entry_points')
    def test_load_plugins(self, mock_iter_entry_points):
        """Test load_plugins method."""
        # Mock entry points
        mock_ep1 = Mock()
        mock_ep1.name = 'plugin1'
        mock_ep1.load.return_value = Mock
        
        mock_ep2 = Mock()
        mock_ep2.name = 'plugin2'
        mock_ep2.load.return_value = Mock
        
        mock_iter_entry_points.return_value = [mock_ep1, mock_ep2]
        
        bio_data = {}
        words = []
        plugins = {'pata_password_cracker.encryption': ['md5']}
        
        categories = Categories(bio_data, words, plugins)
        
        # Test the loaded plugins
        result = categories.load_plugins('test.plugin.group')
        
        assert 'plugin1' in result
        assert 'plugin2' in result
        assert len(result) == 2
    
    @patch('pata_password_cracker.categories.pkg_resources.iter_entry_points')
    def test_exclude_encrypt(self, mock_iter_entry_points):
        """Test exclude_encrypt method."""
        mock_iter_entry_points.return_value = []
        
        bio_data = {}
        words = []
        plugins = {'pata_password_cracker.encryption': ['md5', 'sha1']}
        
        categories = Categories(bio_data, words, plugins)
        
        # Manually set up encryption plugins to test exclusion
        categories.loaded_encryption_plugin_dict = {
            'md5': Mock,
            'sha1': Mock,
            'sha256': Mock,  # This should be excluded
            'bcrypt': Mock   # This should be excluded
        }
        
        # Call exclude_encrypt
        categories.exclude_encrypt()
        
        # Only md5 and sha1 should remain
        assert 'md5' in categories.loaded_encryption_plugin_dict
        assert 'sha1' in categories.loaded_encryption_plugin_dict
        assert 'sha256' not in categories.loaded_encryption_plugin_dict
        assert 'bcrypt' not in categories.loaded_encryption_plugin_dict
    
    @patch('pata_password_cracker.categories.pkg_resources.iter_entry_points')
    def test_process_categories_basic(self, mock_iter_entry_points):
        """Test basic process_categories functionality."""
        mock_iter_entry_points.return_value = []
        
        bio_data = {
            'John Doe': [
                {'core_bio': {'first_name': 'John', 'last_name': 'Doe'}},
                {'family': {'father': 'Bob'}}
            ]
        }
        words = ['test', 'word']
        plugins = {'pata_password_cracker.encryption': ['md5']}
        
        categories = Categories(bio_data, words, plugins)
        
        # Mock the plugin dictionaries
        mock_core_bio_plugin = Mock()
        mock_core_bio_plugin.return_value.process_data.return_value = 'core_bio_result'
        
        mock_family_plugin = Mock()
        mock_family_plugin.return_value.process_data.return_value = 'family_result'
        
        categories.loaded_cat_plugin_dict = {
            'core_bio': mock_core_bio_plugin,
            'family': mock_family_plugin
        }
        categories.loaded_encryption_plugin_dict = {'md5': Mock}
        categories.loaded_substitutors_plugin_dict = {'simple': Mock}
        
        result = categories.process_categories()
        
        # Should return a dictionary with processed individual
        assert isinstance(result, dict)
        assert len(result) == 1
        
        # Check the key format (should be like "0:JohnDoe")
        key = list(result.keys())[0]
        assert key.startswith('0:')
        assert 'JohnDoe' in key
        
        # Check that plugins were called
        mock_core_bio_plugin.assert_called()
        mock_family_plugin.assert_called()
    
    @patch('pata_password_cracker.categories.pkg_resources.iter_entry_points')
    def test_process_categories_no_matching_plugins(self, mock_iter_entry_points):
        """Test process_categories with no matching plugins."""
        mock_iter_entry_points.return_value = []
        
        bio_data = {
            'John Doe': [
                {'unknown_category': {'data': 'value'}}
            ]
        }
        words = ['test']
        plugins = {'pata_password_cracker.encryption': ['md5']}
        
        categories = Categories(bio_data, words, plugins)
        categories.loaded_cat_plugin_dict = {}  # No plugins loaded
        categories.loaded_encryption_plugin_dict = {'md5': Mock}
        categories.loaded_substitutors_plugin_dict = {'simple': Mock}
        
        result = categories.process_categories()
        
        # Should still return a dictionary with the individual but empty data
        assert isinstance(result, dict)
        assert len(result) == 1
        
        key = list(result.keys())[0]
        assert key.startswith('0:')
        assert result[key] == []  # No processing occurred
    
    @patch('pata_password_cracker.categories.pkg_resources.iter_entry_points')
    def test_process_categories_multiple_individuals(self, mock_iter_entry_points):
        """Test process_categories with multiple individuals."""
        mock_iter_entry_points.return_value = []
        
        bio_data = {
            'John Doe': [
                {'core_bio': {'first_name': 'John'}}
            ],
            'Jane Smith': [
                {'core_bio': {'first_name': 'Jane'}}
            ]
        }
        words = ['test']
        plugins = {'pata_password_cracker.encryption': ['md5']}
        
        categories = Categories(bio_data, words, plugins)
        
        mock_plugin = Mock()
        mock_plugin.return_value.process_data.return_value = 'result'
        categories.loaded_cat_plugin_dict = {'core_bio': mock_plugin}
        categories.loaded_encryption_plugin_dict = {'md5': Mock}
        categories.loaded_substitutors_plugin_dict = {'simple': Mock}
        
        result = categories.process_categories()
        
        # Should process both individuals
        assert len(result) == 2
        
        keys = list(result.keys())
        assert any('JohnDoe' in key for key in keys)
        assert any('JaneSmith' in key for key in keys)
        
        # Plugin should be called twice
        assert mock_plugin.call_count == 2
    
    @patch('pata_password_cracker.categories.pkg_resources.iter_entry_points')
    def test_process_categories_empty_bio_data(self, mock_iter_entry_points):
        """Test process_categories with empty bio data."""
        mock_iter_entry_points.return_value = []
        
        bio_data = {}
        words = ['test']
        plugins = {'pata_password_cracker.encryption': ['md5']}
        
        categories = Categories(bio_data, words, plugins)
        
        result = categories.process_categories()
        
        # Should return empty dictionary
        assert result == {}
    
    @patch('pata_password_cracker.categories.pkg_resources.iter_entry_points')
    def test_process_categories_plugin_exception(self, mock_iter_entry_points):
        """Test process_categories when plugin raises exception."""
        mock_iter_entry_points.return_value = []
        
        bio_data = {
            'John Doe': [
                {'core_bio': {'first_name': 'John'}}
            ]
        }
        words = ['test']
        plugins = {'pata_password_cracker.encryption': ['md5']}
        
        categories = Categories(bio_data, words, plugins)
        
        # Mock plugin that raises exception
        mock_plugin = Mock()
        mock_plugin.return_value.process_data.side_effect = Exception("Plugin error")
        categories.loaded_cat_plugin_dict = {'core_bio': mock_plugin}
        categories.loaded_encryption_plugin_dict = {'md5': Mock}
        categories.loaded_substitutors_plugin_dict = {'simple': Mock}
        
        # Should raise the exception
        with pytest.raises(Exception, match="Plugin error"):
            categories.process_categories()