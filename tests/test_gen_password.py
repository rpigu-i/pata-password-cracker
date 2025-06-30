"""
Unit tests for password generator module.
"""
import pytest
from unittest.mock import patch, Mock, MagicMock
from pata_password_cracker.generators.gen_password import PasswordGenerator


class TestPasswordGenerator:
    """Tests for PasswordGenerator class."""
    
    def test_init(self):
        """Test PasswordGenerator initialization."""
        key = 'test_key'
        words = ['word1', 'word2']
        bio_data = {'name': 'John', 'age': 30}
        encryption_dict = {'md5': Mock}
        substitutors_dict = {'simple': Mock}
        
        generator = PasswordGenerator(key, words, bio_data, encryption_dict, substitutors_dict)
        
        assert generator.key == key
        assert generator.words == words
        assert generator.bio_data == bio_data
        assert generator.encryption_dict == encryption_dict
        assert generator.substitutors_dict == substitutors_dict
    
    @patch.object(PasswordGenerator, 'gen_pata_data')
    def test_process_individual_string_values(self, mock_gen_pata_data):
        """Test process_individual with string values."""
        mock_gen_pata_data.return_value = 'processed_data'
        
        generator = PasswordGenerator(
            'test_key',
            ['word1'],
            {'name': 'John', 'city': 'NYC'},
            {'md5': Mock},
            {'simple': Mock}
        )
        
        result = generator.process_individual()
        
        # Should call gen_pata_data for each value
        assert mock_gen_pata_data.call_count == 2
        mock_gen_pata_data.assert_any_call('John')
        mock_gen_pata_data.assert_any_call('NYC')
        
        # Should return processed individual data
        assert 'test_key' in result
        assert 'name' in result
        assert 'city' in result
        assert result['name'] == 'processed_data'
        assert result['city'] == 'processed_data'
    
    @patch.object(PasswordGenerator, 'gen_pata_data')
    def test_process_individual_list_values(self, mock_gen_pata_data):
        """Test process_individual with list values."""
        mock_gen_pata_data.return_value = 'processed_data'
        
        generator = PasswordGenerator(
            'test_key',
            ['word1'],
            {'pets': ['cat', 'dog']},
            {'md5': Mock},
            {'simple': Mock}
        )
        
        result = generator.process_individual()
        
        # Should call gen_pata_data for each list item
        assert mock_gen_pata_data.call_count == 2
        mock_gen_pata_data.assert_any_call('cat')
        mock_gen_pata_data.assert_any_call('dog')
        
        # Should return list of processed data
        assert 'pets' in result
        assert isinstance(result['pets'], list)
        assert len(result['pets']) == 2
        assert all(item == 'processed_data' for item in result['pets'])
    
    @patch.object(PasswordGenerator, 'synonyms')
    @patch.object(PasswordGenerator, 'antonym')
    @patch.object(PasswordGenerator, 'syzygy')
    @patch.object(PasswordGenerator, 'anomaly')
    @patch.object(PasswordGenerator, 'clinamen')
    def test_gen_pata_data(self, mock_clinamen, mock_anomaly, mock_syzygy, mock_antonym, mock_synonyms):
        """Test gen_pata_data method."""
        # Mock all the pata methods
        mock_synonyms.return_value = {'synonym_data': 'test'}
        mock_antonym.return_value = {'antonym_data': 'test'}
        mock_syzygy.return_value = {'syzygy_data': 'test'}
        mock_anomaly.return_value = {'anomaly_data': 'test'}
        mock_clinamen.return_value = {'clinamen_data': 'test'}
        
        generator = PasswordGenerator('key', ['word'], {}, {}, {})
        
        result = generator.gen_pata_data('test_value')
        
        # Should return list with original value and all pata transformations
        assert isinstance(result, list)
        assert len(result) == 6  # original + 5 transformations
        
        # First item should be original
        assert result[0] == {'original': 'test_value'}
        
        # Should call all pata methods
        mock_synonyms.assert_called_once_with('test_value')
        mock_antonym.assert_called_once_with('test_value')
        mock_syzygy.assert_called_once_with('test_value')
        mock_anomaly.assert_called_once_with('test_value')
        mock_clinamen.assert_called_once_with('test_value')
    
    def test_gen_enc_list_basic(self):
        """Test gen_enc_list method."""
        mock_md5 = Mock()
        mock_md5.return_value.hash.side_effect = lambda x: f'md5_{x}'
        
        mock_sha1 = Mock()
        mock_sha1.return_value.hash.side_effect = lambda x: f'sha1_{x}'
        
        generator = PasswordGenerator(
            'key',
            ['word'],
            {},
            {'md5': mock_md5, 'sha1': mock_sha1},
            {}
        )
        
        clear_text = ['password1', 'password2']
        result = generator.gen_enc_list(clear_text)
        
        # Should return dictionary with encrypted values
        assert isinstance(result, dict)
        assert 'md5' in result
        assert 'sha1' in result
        
        # Should contain hashed values
        assert result['md5'] == ['md5_password1', 'md5_password2']
        assert result['sha1'] == ['sha1_password1', 'sha1_password2']
    
    def test_gen_enc_list_empty_list(self):
        """Test gen_enc_list with empty clear_text list."""
        mock_md5 = Mock()
        
        generator = PasswordGenerator(
            'key',
            ['word'],
            {},
            {'md5': mock_md5},
            {}
        )
        
        result = generator.gen_enc_list([])
        
        # Should return dictionary with empty lists
        assert result == {'md5': []}
    
    def test_subsitutor_basic(self):
        """Test subsitutor method."""
        mock_simple = Mock()
        mock_simple.return_value.substitute.return_value = 'substituted'
        
        mock_common = Mock()
        mock_common.return_value.substitute.return_value = 'common_sub'
        
        generator = PasswordGenerator(
            'key',
            ['word'],
            {},
            {},
            {'simple': mock_simple, 'common': mock_common}
        )
        
        result = generator.subsitutor('password')
        
        # Should return list of substituted passwords
        assert isinstance(result, list)
        assert len(result) == 2
        assert 'substituted' in result
        assert 'common_sub' in result
        
        # Should call substitute on each substitutor
        mock_simple.assert_called_once()
        mock_common.assert_called_once()
        mock_simple.return_value.substitute.assert_called_once_with('password')
        mock_common.return_value.substitute.assert_called_once_with('password')
    
    def test_subsitutor_empty_dict(self):
        """Test subsitutor with empty substitutors_dict."""
        generator = PasswordGenerator('key', ['word'], {}, {}, {})
        
        result = generator.subsitutor('password')
        
        # Should return empty list
        assert result == []
    
    @patch('pata_password_cracker.generators.gen_password.Synonym')
    @patch.object(PasswordGenerator, 'subsitutor')
    @patch.object(PasswordGenerator, 'gen_enc_list')
    def test_synonyms(self, mock_gen_enc_list, mock_subsitutor, mock_synonym_class):
        """Test synonyms method."""
        # Mock Synonym class
        mock_synonym_instance = Mock()
        mock_synonym_instance.generate_synonym.return_value = {'results': ['syn1', 'syn2', 'syn1']}  # Include duplicate
        mock_synonym_class.return_value = mock_synonym_instance
        
        # Mock subsitutor
        mock_subsitutor.side_effect = [['sub1'], ['sub2']]
        
        # Mock gen_enc_list
        mock_gen_enc_list.return_value = {'md5': ['hash1', 'hash2']}
        
        generator = PasswordGenerator('key', ['word'], {}, {}, {})
        
        result = generator.synonyms('test_word')
        
        # Should call Synonym.generate_synonym
        mock_synonym_instance.generate_synonym.assert_called_once_with('test_word')
        
        # Should call subsitutor for each unique synonym
        assert mock_subsitutor.call_count == 2
        
        # Should call gen_enc_list with clear text
        mock_gen_enc_list.assert_called_once()
        clear_text_arg = mock_gen_enc_list.call_args[0][0]
        assert 'syn1' in clear_text_arg
        assert 'syn2' in clear_text_arg
        assert 'sub1' in clear_text_arg
        assert 'sub2' in clear_text_arg
        
        # Should return correct structure
        assert result == {'synonym': {'clear_text': clear_text_arg, 'encrypted': {'md5': ['hash1', 'hash2']}}}
    
    @patch('pata_password_cracker.generators.gen_password.Antonym')
    @patch.object(PasswordGenerator, 'subsitutor')
    @patch.object(PasswordGenerator, 'gen_enc_list')
    def test_antonym(self, mock_gen_enc_list, mock_subsitutor, mock_antonym_class):
        """Test antonym method."""
        # Mock Antonym class
        mock_antonym_instance = Mock()
        mock_antonym_instance.generate_antonym.return_value = {'results': ['ant1', 'ant2']}
        mock_antonym_class.return_value = mock_antonym_instance
        
        mock_subsitutor.side_effect = [['sub1'], ['sub2']]
        mock_gen_enc_list.return_value = {'md5': ['hash1']}
        
        generator = PasswordGenerator('key', ['word'], {}, {}, {})
        
        result = generator.antonym('test_word')
        
        # Should call Antonym.generate_antonym
        mock_antonym_instance.generate_antonym.assert_called_once_with('test_word')
        
        # Should return correct structure
        assert 'antonyms' in result
        assert 'clear_text' in result['antonyms']
        assert 'encrypted' in result['antonyms']
    
    @patch('pata_password_cracker.generators.gen_password.Syzygy')
    @patch.object(PasswordGenerator, 'subsitutor')
    @patch.object(PasswordGenerator, 'gen_enc_list')
    def test_syzygy(self, mock_gen_enc_list, mock_subsitutor, mock_syzygy_class):
        """Test syzygy method."""
        # Mock Syzygy class
        mock_syzygy_instance = Mock()
        mock_syzygy_instance.generate_syzygy.return_value = {'results': ['syz1', 'syz2']}
        mock_syzygy_class.return_value = mock_syzygy_instance
        
        mock_subsitutor.side_effect = [['sub1'], ['sub2']]
        mock_gen_enc_list.return_value = {'md5': ['hash1']}
        
        generator = PasswordGenerator('key', ['word'], {}, {}, {})
        
        result = generator.syzygy('test_word')
        
        # Should call Syzygy.generate_syzygy
        mock_syzygy_instance.generate_syzygy.assert_called_once_with('test_word')
        
        # Should return correct structure
        assert 'syzygys' in result
        assert 'clear_text' in result['syzygys']
        assert 'encrypted' in result['syzygys']
    
    @patch('pata_password_cracker.generators.gen_password.Anomaly')
    @patch.object(PasswordGenerator, 'subsitutor')
    @patch.object(PasswordGenerator, 'gen_enc_list')
    def test_anomaly(self, mock_gen_enc_list, mock_subsitutor, mock_anomaly_class):
        """Test anomaly method."""
        # Mock Anomaly class
        mock_anomaly_instance = Mock()
        mock_anomaly_instance.generate_anomaly.return_value = {'results': ['anom1', 'anom2']}
        mock_anomaly_class.return_value = mock_anomaly_instance
        
        mock_subsitutor.side_effect = [['sub1'], ['sub2']]
        mock_gen_enc_list.return_value = {'md5': ['hash1']}
        
        generator = PasswordGenerator('key', ['word1', 'word2'], {}, {}, {})
        
        result = generator.anomaly('test_word')
        
        # Should call Anomaly.generate_anomaly with words list
        mock_anomaly_instance.generate_anomaly.assert_called_once_with('test_word', ['word1', 'word2'], 1)
        
        # Should return correct structure
        assert 'anomalies' in result
        assert 'clear_text' in result['anomalies']
        assert 'encrypted' in result['anomalies']
    
    @patch('pata_password_cracker.generators.gen_password.Clinamen')
    @patch.object(PasswordGenerator, 'subsitutor')
    @patch.object(PasswordGenerator, 'gen_enc_list')
    def test_clinamen(self, mock_gen_enc_list, mock_subsitutor, mock_clinamen_class):
        """Test clinamen method."""
        # Mock Clinamen class
        mock_clinamen_instance = Mock()
        mock_clinamen_instance.generate_clinamen.return_value = {'results': ['clin1', 'clin2']}
        mock_clinamen_class.return_value = mock_clinamen_instance
        
        mock_subsitutor.side_effect = [['sub1'], ['sub2']]
        mock_gen_enc_list.return_value = {'md5': ['hash1']}
        
        generator = PasswordGenerator('key', ['word1', 'word2'], {}, {}, {})
        
        result = generator.clinamen('test_word')
        
        # Should call Clinamen.generate_clinamen with words list
        mock_clinamen_instance.generate_clinamen.assert_called_once_with('test_word', ['word1', 'word2'], 1)
        
        # Should return correct structure
        assert 'clinamen' in result
        assert 'clear_text' in result['clinamen']
        assert 'encrypted' in result['clinamen']
    
    def test_integration_basic_workflow(self):
        """Test basic integration of PasswordGenerator workflow."""
        # Create real instances for substitutors and encryption
        from pata_password_cracker.substitutors.simple import MungSubstitutor
        from pata_password_cracker.encryption.md5 import MD5Encryption
        
        # Mock the patalib components since they're external dependencies
        with patch('pata_password_cracker.generators.gen_password.Synonym') as mock_synonym, \
             patch('pata_password_cracker.generators.gen_password.Antonym') as mock_antonym, \
             patch('pata_password_cracker.generators.gen_password.Syzygy') as mock_syzygy, \
             patch('pata_password_cracker.generators.gen_password.Anomaly') as mock_anomaly, \
             patch('pata_password_cracker.generators.gen_password.Clinamen') as mock_clinamen:
            
            # Set up mock returns
            for mock_obj in [mock_synonym, mock_antonym, mock_syzygy, mock_anomaly, mock_clinamen]:
                mock_instance = Mock()
                mock_instance.generate_synonym.return_value = {'results': ['test_result']}
                mock_instance.generate_antonym.return_value = {'results': ['test_result']}
                mock_instance.generate_syzygy.return_value = {'results': ['test_result']}
                mock_instance.generate_anomaly.return_value = {'results': ['test_result']}
                mock_instance.generate_clinamen.return_value = {'results': ['test_result']}
                mock_obj.return_value = mock_instance
            
            generator = PasswordGenerator(
                'test_key',
                ['word1', 'word2'],
                {'name': 'John', 'pets': ['cat', 'dog']},
                {'md5': MD5Encryption},
                {'simple': MungSubstitutor}
            )
            
            result = generator.process_individual()
            
            # Should return dictionary with processed data
            assert isinstance(result, dict)
            assert 'test_key' in result
            assert 'name' in result
            assert 'pets' in result
            
            # Should process string and list values differently
            assert isinstance(result['name'], list)  # gen_pata_data returns list
            assert isinstance(result['pets'], list)
            assert len(result['pets']) == 2  # Two pets processed