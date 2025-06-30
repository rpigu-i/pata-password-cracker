"""
Test configuration and fixtures for pata-password-cracker tests.
"""
import pytest
import tempfile
import os
import yaml
from unittest.mock import Mock


@pytest.fixture
def temp_yaml_file():
    """Create a temporary YAML file for testing."""
    content = """
individuals:
- James Smith:
    - core_bio:
        first_name: James
        last_name: Smith
        street1: 123
        street2: Broadway 
        city: New York
        zip: "01234"
        dob: 1982-05-06
    - family:
        - individual_1: 
            relationship: father
            first_name: Tim
            last_name: Smith
            dob: 1945-12-21
        - individual_2: 
            relationship: mother  
            first_name: Susie
            last_name: Smith
            dob: 1944-03-03
    - free_data:
        pet1: cat
        pet1_name: ginger
        pet2: dog
        pet2_name: "Tin Tin"
        club: Masons
        lodge: Hermes
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def temp_words_file():
    """Create a temporary words file for testing."""
    words = ["apple", "banana", "cherry", "dog", "elephant", "fox", "guitar", "house"]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        for word in words:
            f.write(word + '\n')
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def sample_bio_data():
    """Sample biographical data for testing."""
    return {
        'first_name': 'John',
        'last_name': 'Doe',
        'dob': '1990-01-01',
        'city': 'New York',
        'street1': '123',
        'pet_name': 'Fluffy'
    }


@pytest.fixture
def sample_words():
    """Sample word list for testing."""
    return ["test", "word", "list", "sample", "data"]


@pytest.fixture
def mock_encryption_plugins():
    """Mock encryption plugins for testing."""
    mock_md5 = Mock()
    mock_md5.return_value.hash.return_value = "5d41402abc4b2a76b9719d911017c592"
    
    mock_sha1 = Mock()
    mock_sha1.return_value.hash.return_value = "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"
    
    return {
        'md5': mock_md5,
        'sha1': mock_sha1
    }


@pytest.fixture
def mock_substitutor_plugins():
    """Mock substitutor plugins for testing."""
    mock_simple = Mock()
    mock_simple.return_value.substitute.return_value = "t3st"
    
    return {
        'simple': mock_simple
    }


@pytest.fixture
def sample_plugins():
    """Sample plugins configuration for testing."""
    return {
        'pata_password_cracker.encryption': ['md5', 'sha1']
    }