"""
Unit tests for input processing modules.
"""
import pytest
import tempfile
import os
import yaml
from pata_password_cracker.input import ProcessInputYaml, ProcessInputWords


class TestProcessInputYaml:
    """Tests for ProcessInputYaml class."""
    
    def test_yaml_processor_valid_file(self, temp_yaml_file):
        """Test processing a valid YAML file."""
        processor = ProcessInputYaml()
        result = processor.yaml_processor(temp_yaml_file)
        
        # Convert generator to list for testing
        result_list = list(result)
        
        assert len(result_list) == 1
        assert 'individuals' in result_list[0]
        assert len(result_list[0]['individuals']) == 1
        
        individual = result_list[0]['individuals'][0]
        assert 'James Smith' in individual
        
        james_data = individual['James Smith']
        assert len(james_data) == 3  # core_bio, family, free_data
        
        # Check core_bio data
        core_bio = james_data[0]['core_bio']
        assert core_bio['first_name'] == 'James'
        assert core_bio['last_name'] == 'Smith'
        assert core_bio['city'] == 'New York'
    
    def test_yaml_processor_nonexistent_file(self):
        """Test processing a non-existent YAML file."""
        processor = ProcessInputYaml()
        
        with pytest.raises(FileNotFoundError):
            list(processor.yaml_processor('nonexistent.yaml'))
    
    def test_yaml_processor_invalid_yaml(self):
        """Test processing an invalid YAML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: content: [unclosed")
            f.flush()
            
            processor = ProcessInputYaml()
            
            with pytest.raises(yaml.YAMLError):
                list(processor.yaml_processor(f.name))
        
        os.unlink(f.name)
    
    def test_yaml_processor_empty_file(self):
        """Test processing an empty YAML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("")
            f.flush()
            
            processor = ProcessInputYaml()
            result = list(processor.yaml_processor(f.name))
            
            # Empty YAML should return empty list
            assert result == []
        
        os.unlink(f.name)


class TestProcessInputWords:
    """Tests for ProcessInputWords class."""
    
    def test_words_processor_valid_file(self, temp_words_file):
        """Test processing a valid words file."""
        processor = ProcessInputWords()
        result = processor.words_processor(temp_words_file)
        
        expected_words = ["apple", "banana", "cherry", "dog", "elephant", "fox", "guitar", "house"]
        assert result == expected_words
    
    def test_words_processor_nonexistent_file(self):
        """Test processing a non-existent words file."""
        processor = ProcessInputWords()
        
        with pytest.raises(FileNotFoundError):
            processor.words_processor('nonexistent.txt')
    
    def test_words_processor_empty_file(self):
        """Test processing an empty words file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("")
            f.flush()
            
            processor = ProcessInputWords()
            result = processor.words_processor(f.name)
            
            assert result == []
        
        os.unlink(f.name)
    
    def test_words_processor_whitespace_handling(self):
        """Test processing words with whitespace."""
        words_content = "  apple  \n\n  banana\t\n  cherry  \n\n"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(words_content)
            f.flush()
            
            processor = ProcessInputWords()
            result = processor.words_processor(f.name)
            
            expected = ["apple", "", "banana", "cherry", ""]
            assert result == expected
        
        os.unlink(f.name)
    
    def test_words_processor_single_word(self):
        """Test processing file with single word."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("singleword")
            f.flush()
            
            processor = ProcessInputWords()
            result = processor.words_processor(f.name)
            
            assert result == ["singleword"]
        
        os.unlink(f.name)