"""
Unit tests for generator modules.
"""
import pytest
from unittest.mock import patch, Mock, MagicMock
from datetime import date
from pata_password_cracker.generators.core_bio import CoreBioGenerator
from pata_password_cracker.generators.family import FamilyGenerator
from pata_password_cracker.generators.free_data import FreeDataGenerator
from pata_password_cracker.generators.date_name_mixin import DateNameMixin


class TestCoreRooBioGenerator:
    """Tests for CoreBioGenerator class."""
    
    @patch('pata_password_cracker.generators.core_bio.PasswordGenerator')
    def test_process_data_basic(self, mock_password_generator):
        """Test basic process_data functionality."""
        mock_instance = Mock()
        mock_instance.process_individual.return_value = {'passwords': ['test1', 'test2']}
        mock_password_generator.return_value = mock_instance
        
        generator = CoreBioGenerator()
        
        # Mock the name_dob method
        generator.name_dob = Mock(return_value={'name_dob': ['john1982', 'doe1982']})
        
        core_bio_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'dob': date(1982, 5, 6),
            'city': 'New York'
        }
        
        words = ['test', 'word']
        encryption_dict = {'md5': Mock}
        substitutors_dict = {'simple': Mock}
        
        result = generator.process_data(
            'core_bio',
            words,
            core_bio_data,
            encryption_dict,
            substitutors_dict
        )
        
        # Should return list with name_dob result and password generator result
        assert isinstance(result, list)
        assert len(result) == 2
        assert {'name_dob': ['john1982', 'doe1982']} in result
        assert {'passwords': ['test1', 'test2']} in result
        
        # Should call PasswordGenerator
        mock_password_generator.assert_called_once_with(
            'core_bio',
            words,
            core_bio_data,
            encryption_dict,
            substitutors_dict
        )
    
    def test_process_data_sets_instance_variables(self):
        """Test that process_data sets instance variables correctly."""
        generator = CoreBioGenerator()
        generator.name_dob = Mock(return_value={})
        
        with patch('pata_password_cracker.generators.core_bio.PasswordGenerator'):
            generator.process_data(
                'test_cat',
                ['word1', 'word2'],
                {'data': 'value'},
                {'enc': 'dict'},
                {'sub': 'dict'}
            )
        
        assert generator.cat == 'test_cat'
        assert generator.words == ['word1', 'word2']
        assert generator.encryption_dict == {'enc': 'dict'}
        assert generator.substitutors_dict == {'sub': 'dict'}
    
    def test_inherits_from_date_name_mixin(self):
        """Test that CoreBioGenerator inherits from DateNameMixin."""
        generator = CoreBioGenerator()
        assert isinstance(generator, DateNameMixin)
        assert hasattr(generator, 'name_dob')
        assert hasattr(generator, 'date_and_name_processor')


class TestFamilyGenerator:
    """Tests for FamilyGenerator class."""
    
    @patch('pata_password_cracker.generators.family.PasswordGenerator')
    def test_process_data_basic(self, mock_password_generator):
        """Test basic process_data functionality."""
        mock_instance = Mock()
        mock_instance.process_individual.return_value = {'passwords': ['family1', 'family2']}
        mock_password_generator.return_value = mock_instance
        
        generator = FamilyGenerator()
        
        # Mock the name_dob method
        generator.name_dob = Mock(return_value={'family_name_dob': ['tim1945', 'smith1945']})
        
        family_data = [
            {
                'individual_1': {
                    'relationship': 'father',
                    'first_name': 'Tim',
                    'last_name': 'Smith',
                    'dob': date(1945, 12, 21)
                }
            }
        ]
        
        words = ['test', 'word']
        encryption_dict = {'md5': Mock}
        substitutors_dict = {'simple': Mock}
        
        result = generator.process_data(
            'family',
            words,
            family_data,
            encryption_dict,
            substitutors_dict
        )
        
        # Should return dictionary, not list
        assert isinstance(result, dict)
        assert len(result) == 1
        assert 'individual_1' in result
    
    def test_process_data_flattens_family_data(self):
        """Test that process_data flattens family data correctly."""
        generator = FamilyGenerator()
        generator.name_dob = Mock(return_value={})
        
        family_data = [
            {
                'individual_1': {
                    'first_name': 'Tim',
                    'last_name': 'Smith'
                }
            },
            {
                'individual_2': {
                    'first_name': 'Sue',
                    'last_name': 'Smith'
                }
            }
        ]
        
        with patch('pata_password_cracker.generators.family.PasswordGenerator') as mock_pg:
            generator.process_data(
                'family',
                ['word'],
                family_data,
                {},
                {}
            )
        
        # Should process each individual separately
        assert mock_pg.call_count == 2  # Two individuals
    
    def test_inherits_from_date_name_mixin(self):
        """Test that FamilyGenerator inherits from DateNameMixin."""
        generator = FamilyGenerator()
        assert isinstance(generator, DateNameMixin)


class TestFreeDataGenerator:
    """Tests for FreeDataGenerator class."""
    
    @patch('pata_password_cracker.generators.free_data.PasswordGenerator')
    def test_process_data_basic(self, mock_password_generator):
        """Test basic process_data functionality."""
        mock_instance = Mock()
        mock_instance.process_individual.return_value = {'passwords': ['pet1', 'pet2']}
        mock_password_generator.return_value = mock_instance
        
        generator = FreeDataGenerator()
        
        free_data = {
            'pet1': 'cat',
            'pet1_name': 'ginger',
            'pet2': 'dog',
            'pet2_name': 'Tin Tin'
        }
        
        words = ['test', 'word']
        encryption_dict = {'md5': Mock}
        substitutors_dict = {'simple': Mock}
        
        result = generator.process_data(
            'free_data',
            words,
            free_data,
            encryption_dict,
            substitutors_dict
        )
        
        # Should return the result from PasswordGenerator
        assert result == {'passwords': ['pet1', 'pet2']}
        
        # Should call PasswordGenerator with correct parameters
        mock_password_generator.assert_called_once_with(
            'free_data',
            words,
            free_data,
            encryption_dict,
            substitutors_dict
        )
    
    def test_process_data_empty_data(self):
        """Test process_data with empty free data."""
        generator = FreeDataGenerator()
        
        with patch('pata_password_cracker.generators.free_data.PasswordGenerator') as mock_pg:
            mock_instance = Mock()
            mock_instance.process_individual.return_value = {}
            mock_pg.return_value = mock_instance
            
            result = generator.process_data(
                'free_data',
                ['word'],
                {},
                {},
                {}
            )
            
            assert result == {}
            mock_pg.assert_called_once()
    
    def test_process_data_passes_through_parameters(self):
        """Test that process_data passes through all parameters correctly."""
        generator = FreeDataGenerator()
        
        with patch('pata_password_cracker.generators.free_data.PasswordGenerator') as mock_pg:
            mock_instance = Mock()
            mock_instance.process_individual.return_value = 'result'
            mock_pg.return_value = mock_instance
            
            k = 'test_key'
            words = ['word1', 'word2']
            data = {'key': 'value'}
            encryption = {'md5': Mock}
            substitutors = {'simple': Mock}
            
            result = generator.process_data(k, words, data, encryption, substitutors)
            
            # Should pass all parameters to PasswordGenerator
            mock_pg.assert_called_once_with(k, words, data, encryption, substitutors)
            mock_instance.process_individual.assert_called_once()
            assert result == 'result'


class TestDateNameMixin:
    """Tests for DateNameMixin class."""
    
    def test_date_and_name_processor_basic(self):
        """Test basic date and name processing."""
        mixin = DateNameMixin()
        
        name = "John"
        dob = date(1982, 5, 6)
        
        result = mixin.date_and_name_processor(name, dob)
        
        expected = [
            "John1982-05-06",  # name + str(dob)
            "John1982",        # name + str(dob.year)
            "1982John",        # str(dob.year) + name
            "82John",          # str(dob.year)[2] + str(dob.year)[3] + name
            "John82"           # name + str(dob.year)[2] + str(dob.year)[3]
        ]
        
        assert result == expected
    
    def test_date_and_name_processor_different_year(self):
        """Test date and name processing with different year."""
        mixin = DateNameMixin()
        
        name = "Jane"
        dob = date(1975, 3, 15)
        
        result = mixin.date_and_name_processor(name, dob)
        
        expected = [
            "Jane1975-03-15",
            "Jane1975",
            "1975Jane",
            "75Jane",
            "Jane75"
        ]
        
        assert result == expected
    
    def test_date_and_name_processor_edge_case_year(self):
        """Test date and name processing with edge case year."""
        mixin = DateNameMixin()
        
        name = "Bob"
        dob = date(2000, 1, 1)
        
        result = mixin.date_and_name_processor(name, dob)
        
        expected = [
            "Bob2000-01-01",
            "Bob2000",
            "2000Bob",
            "00Bob",
            "Bob00"
        ]
        
        assert result == expected
    
    @patch('pata_password_cracker.generators.date_name_mixin.PasswordGenerator')
    def test_name_dob_with_first_name_and_dob(self, mock_password_generator):
        """Test name_dob with first_name and dob."""
        mock_instance = Mock()
        mock_instance.process_individual.return_value = {'result': 'test'}
        mock_password_generator.return_value = mock_instance
        
        mixin = DateNameMixin()
        mixin.cat = 'test_cat'
        mixin.words = ['word1']
        mixin.encryption_dict = {'md5': Mock}
        mixin.substitutors_dict = {'simple': Mock}
        
        values = {
            'first_name': 'John',
            'last_name': 'Doe',
            'dob': date(1982, 5, 6)
        }
        
        result = mixin.name_dob(values)
        
        # Should call PasswordGenerator
        mock_password_generator.assert_called_once()
        call_args = mock_password_generator.call_args[0]
        
        # Check that the name_dob_combo contains expected keys
        name_dob_combo = call_args[2]
        assert 'first_name_dob' in name_dob_combo
        assert 'last_name_dob' in name_dob_combo
        
        # Check that the lists contain expected values
        first_name_list = name_dob_combo['first_name_dob']
        last_name_list = name_dob_combo['last_name_dob']
        
        assert 'John1982' in first_name_list
        assert 'Doe1982' in last_name_list
    
    @patch('pata_password_cracker.generators.date_name_mixin.PasswordGenerator')
    def test_name_dob_missing_data(self, mock_password_generator):
        """Test name_dob with missing data."""
        mock_instance = Mock()
        mock_instance.process_individual.return_value = {'result': 'test'}
        mock_password_generator.return_value = mock_instance
        
        mixin = DateNameMixin()
        mixin.cat = 'test_cat'
        mixin.words = ['word1']
        mixin.encryption_dict = {'md5': Mock}
        mixin.substitutors_dict = {'simple': Mock}
        
        values = {
            'first_name': 'John',
            'last_name': 'Doe'
            # Missing dob
        }
        
        result = mixin.name_dob(values)
        
        # Should still call PasswordGenerator but with empty combo
        mock_password_generator.assert_called_once()
        call_args = mock_password_generator.call_args[0]
        name_dob_combo = call_args[2]
        
        # Should be empty since no dob was provided
        assert name_dob_combo == {}
    
    @patch('pata_password_cracker.generators.date_name_mixin.PasswordGenerator')
    def test_name_dob_only_first_name_and_dob(self, mock_password_generator):
        """Test name_dob with only first_name and dob."""
        mock_instance = Mock()
        mock_instance.process_individual.return_value = {'result': 'test'}
        mock_password_generator.return_value = mock_instance
        
        mixin = DateNameMixin()
        mixin.cat = 'test_cat'
        mixin.words = ['word1']
        mixin.encryption_dict = {'md5': Mock}
        mixin.substitutors_dict = {'simple': Mock}
        
        values = {
            'first_name': 'John',
            'dob': date(1982, 5, 6)
            # Missing last_name
        }
        
        result = mixin.name_dob(values)
        
        mock_password_generator.assert_called_once()
        call_args = mock_password_generator.call_args[0]
        name_dob_combo = call_args[2]
        
        # Should only have first_name_dob
        assert 'first_name_dob' in name_dob_combo
        assert 'last_name_dob' not in name_dob_combo