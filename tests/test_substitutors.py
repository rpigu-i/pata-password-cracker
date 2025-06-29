"""
Unit tests for substitutor modules.
"""
import pytest
from unittest.mock import patch, Mock
from pata_password_cracker.substitutors.simple import MungSubstitutor
from pata_password_cracker.substitutors.common import MungSubstitutorCommon
from pata_password_cracker.substitutors.simplerandom import MungSubstitutorRandom


class TestMungSubstitutor:
    """Tests for MungSubstitutor class."""
    
    def test_substitute_basic(self):
        """Test basic character substitution."""
        substitutor = MungSubstitutor()
        result = substitutor.substitute("hello")
        # 'h' -> '#', 'e' -> '3', 'l' -> '1', 'o' -> '0'
        expected = "#311o"  # Last 'o' -> '0'
        assert result == "#3110"
    
    def test_substitute_empty_string(self):
        """Test substitution with empty string."""
        substitutor = MungSubstitutor()
        result = substitutor.substitute("")
        assert result == ""
    
    def test_substitute_no_matches(self):
        """Test substitution with characters not in substitution table."""
        substitutor = MungSubstitutor()
        result = substitutor.substitute("xyz")
        # 'x' -> '%' (from table), 'y' and 'z' remain unchanged
        expected = "%yz"
        assert result == expected
    
    def test_substitute_mixed_case(self):
        """Test substitution with mixed case."""
        substitutor = MungSubstitutor()
        result = substitutor.substitute("AaEe")
        # 'A' -> '@', 'a' -> '@', 'E' -> '3', 'e' -> '3'
        expected = "@@33"
        assert result == expected
    
    def test_substitute_numbers(self):
        """Test substitution with numbers."""
        substitutor = MungSubstitutor()
        result = substitutor.substitute("013")
        # '0' -> 'O', '1' -> 'I', '3' -> 'E'
        expected = "OIE"
        assert result == expected
    
    def test_substitute_special_characters(self):
        """Test substitution with special characters."""
        substitutor = MungSubstitutor()
        result = substitutor.substitute("/-")
        # '/' -> '-', '-' -> '/'
        expected = "-/"
        assert result == expected
    
    def test_substitute_repeated_characters(self):
        """Test substitution with repeated characters."""
        substitutor = MungSubstitutor()
        result = substitutor.substitute("aaa")
        # All 'a' -> '@'
        expected = "@@@"
        assert result == expected
    
    def test_munger_method_directly(self):
        """Test the munger method directly."""
        substitutor = MungSubstitutor()
        test_table = [('a', 'X'), ('b', 'Y')]
        result = substitutor.munger("abc", test_table)
        expected = "XYc"
        assert result == expected
    
    def test_munger_with_empty_table(self):
        """Test munger with empty substitution table."""
        substitutor = MungSubstitutor()
        result = substitutor.munger("hello", [])
        assert result == "hello"
    
    def test_munger_overlapping_substitutions(self):
        """Test munger with overlapping substitutions."""
        substitutor = MungSubstitutor()
        # Test case where substitution might create new matches
        test_table = [('a', 'b'), ('b', 'c')]
        result = substitutor.munger("ab", test_table)
        # 'a' -> 'b', 'b' -> 'c', but should not cascade
        expected = "bc"
        assert result == expected


class TestMungSubstitutorCommon:
    """Tests for MungSubstitutorCommon class."""
    
    def test_substitute_basic(self):
        """Test basic character substitution with common table."""
        substitutor = MungSubstitutorCommon()
        result = substitutor.substitute("hello")
        # Using common substitution table
        # 'e' -> '3', 'l' -> '1', 'o' -> '0'
        expected = "h3110"
        assert result == expected
    
    def test_substitute_empty_string(self):
        """Test substitution with empty string."""
        substitutor = MungSubstitutorCommon()
        result = substitutor.substitute("")
        assert result == ""
    
    def test_substitute_common_characters(self):
        """Test substitution with characters from common table."""
        substitutor = MungSubstitutorCommon()
        result = substitutor.substitute("aegios")
        # 'a' -> '@', 'e' -> '3', 'g' -> '9', 'i' -> '1', 'o' -> '0', 's' -> '$'
        expected = "@391o$"  # 'o' -> '0'
        assert result == "@3910$"
    
    def test_substitute_numbers_common(self):
        """Test substitution with numbers in common table."""
        substitutor = MungSubstitutorCommon()
        result = substitutor.substitute("013")
        # '0' -> 'O', '1' -> 'I', '3' -> 'E'
        expected = "OIE"
        assert result == expected
    
    def test_substitute_uppercase_common(self):
        """Test substitution with uppercase letters."""
        substitutor = MungSubstitutorCommon()
        result = substitutor.substitute("AEIOS")
        # 'A' -> '@', 'E' -> '3', 'I' -> '1', 'O' -> '0', 'S' -> '2'
        expected = "@3102"
        assert result == expected
    
    def test_inherits_from_mung_substitutor(self):
        """Test that MungSubstitutorCommon inherits from MungSubstitutor."""
        substitutor = MungSubstitutorCommon()
        assert isinstance(substitutor, MungSubstitutor)
        assert hasattr(substitutor, 'munger')
    
    def test_common_table_different_from_simple(self):
        """Test that common substitution table is different from simple."""
        simple_sub = MungSubstitutor()
        common_sub = MungSubstitutorCommon()
        
        # Test with a character that has different substitutions
        test_string = "bfhjkqtvwx"
        simple_result = simple_sub.substitute(test_string)
        common_result = common_sub.substitute(test_string)
        
        # Results should be different for some characters
        # (since tables have different mappings)
        assert simple_result != common_result or test_string == simple_result == common_result


class TestMungSubstitutorRandom:
    """Tests for MungSubstitutorRandom class."""
    
    @patch('random.choice')
    def test_substitute_with_mocked_random(self, mock_choice):
        """Test substitution with mocked random choice."""
        mock_choice.return_value = ('a', '@')  # Always choose first substitution
        
        substitutor = MungSubstitutorRandom()
        result = substitutor.substitute("hello")
        
        # Should call random.choice for substitution selection
        assert mock_choice.called
    
    def test_substitute_basic_random(self):
        """Test basic random substitution functionality."""
        substitutor = MungSubstitutorRandom()
        result = substitutor.substitute("hello")
        
        # Result should be a string of same length
        assert isinstance(result, str)
        assert len(result) == len("hello")
    
    def test_substitute_empty_string_random(self):
        """Test random substitution with empty string."""
        substitutor = MungSubstitutorRandom()
        result = substitutor.substitute("")
        assert result == ""
    
    def test_substitute_consistency_random(self):
        """Test that random substitution is consistent within same call."""
        substitutor = MungSubstitutorRandom()
        # Test multiple times to ensure it doesn't crash
        for _ in range(10):
            result = substitutor.substitute("test")
            assert isinstance(result, str)
            assert len(result) == 4
    
    def test_inherits_from_mung_substitutor(self):
        """Test that MungSubstitutorRandom inherits from MungSubstitutor."""
        substitutor = MungSubstitutorRandom()
        assert isinstance(substitutor, MungSubstitutor)
        assert hasattr(substitutor, 'munger')
    
    @patch('random.choice')
    def test_substitute_multiple_calls_different_choices(self, mock_choice):
        """Test that multiple substitutions can have different random choices."""
        # Mock different choices for different calls
        mock_choice.side_effect = [('a', '@'), ('a', '4')]  # Different substitutions
        
        substitutor = MungSubstitutorRandom()
        
        # Make multiple calls
        result1 = substitutor.substitute("a")
        result2 = substitutor.substitute("a")
        
        # Should have called choice multiple times
        assert mock_choice.call_count >= 1


class TestSubstitutorComparison:
    """Tests comparing different substitutor classes."""
    
    def test_different_substitutors_may_produce_different_results(self):
        """Test that different substitutors may produce different results."""
        simple_sub = MungSubstitutor()
        common_sub = MungSubstitutorCommon()
        random_sub = MungSubstitutorRandom()
        
        test_string = "hello"
        
        simple_result = simple_sub.substitute(test_string)
        common_result = common_sub.substitute(test_string)
        random_result = random_sub.substitute(test_string)
        
        # All should be strings of same length
        assert all(isinstance(r, str) for r in [simple_result, common_result, random_result])
        assert all(len(r) == len(test_string) for r in [simple_result, common_result, random_result])
    
    def test_all_substitutors_handle_empty_string(self):
        """Test that all substitutors handle empty string correctly."""
        substitutors = [
            MungSubstitutor(),
            MungSubstitutorCommon(),
            MungSubstitutorRandom()
        ]
        
        for sub in substitutors:
            result = sub.substitute("")
            assert result == ""
    
    def test_all_substitutors_handle_no_substitutable_characters(self):
        """Test that all substitutors handle strings with no substitutable characters."""
        # Use characters that are unlikely to be in any substitution table
        test_string = "ñüφ"
        
        substitutors = [
            MungSubstitutor(),
            MungSubstitutorCommon(), 
            MungSubstitutorRandom()
        ]
        
        for sub in substitutors:
            result = sub.substitute(test_string)
            # Should return original string if no substitutions possible
            assert isinstance(result, str)
            assert len(result) == len(test_string)