"""
Unit tests for encryption modules.
"""
import pytest
import hashlib
from unittest.mock import patch, Mock
from pata_password_cracker.encryption.md5 import MD5Encryption
from pata_password_cracker.encryption.sha1 import SHA1Encryption
from pata_password_cracker.encryption.sha256 import SHA256Encryption
from pata_password_cracker.encryption.sha512 import SHA512Encryption
from pata_password_cracker.encryption.sha224 import SHA224Encryption
from pata_password_cracker.encryption.sha384 import SHA384Encryption
from pata_password_cracker.encryption.bcrypt import BcryptEncryption


class TestMD5Encryption:
    """Tests for MD5Encryption class."""
    
    def test_hash_simple_string(self):
        """Test MD5 hashing of a simple string."""
        encryptor = MD5Encryption()
        result = encryptor.hash("hello")
        expected = hashlib.md5("hello".encode('utf-8')).hexdigest()
        assert result == expected
    
    def test_hash_empty_string(self):
        """Test MD5 hashing of empty string."""
        encryptor = MD5Encryption()
        result = encryptor.hash("")
        expected = hashlib.md5("".encode('utf-8')).hexdigest()
        assert result == expected
    
    def test_hash_unicode_string(self):
        """Test MD5 hashing of unicode string."""
        encryptor = MD5Encryption()
        result = encryptor.hash("héllo")
        expected = hashlib.md5("héllo".encode('utf-8')).hexdigest()
        assert result == expected
    
    def test_hash_long_string(self):
        """Test MD5 hashing of long string."""
        encryptor = MD5Encryption()
        long_string = "a" * 10000
        result = encryptor.hash(long_string)
        expected = hashlib.md5(long_string.encode('utf-8')).hexdigest()
        assert result == expected
    
    def test_hash_consistent_results(self):
        """Test that MD5 hashing produces consistent results."""
        encryptor = MD5Encryption()
        password = "test_password"
        result1 = encryptor.hash(password)
        result2 = encryptor.hash(password)
        assert result1 == result2


class TestSHA1Encryption:
    """Tests for SHA1Encryption class."""
    
    def test_hash_simple_string(self):
        """Test SHA1 hashing of a simple string."""
        encryptor = SHA1Encryption()
        result = encryptor.hash("hello")
        expected = hashlib.sha1("hello".encode('utf-8')).hexdigest()
        assert result == expected
    
    def test_hash_empty_string(self):
        """Test SHA1 hashing of empty string."""
        encryptor = SHA1Encryption()
        result = encryptor.hash("")
        expected = hashlib.sha1("".encode('utf-8')).hexdigest()
        assert result == expected
    
    def test_hash_unicode_string(self):
        """Test SHA1 hashing of unicode string."""
        encryptor = SHA1Encryption()
        result = encryptor.hash("héllo")
        expected = hashlib.sha1("héllo".encode('utf-8')).hexdigest()
        assert result == expected


class TestSHA256Encryption:
    """Tests for SHA256Encryption class."""
    
    def test_hash_simple_string(self):
        """Test SHA256 hashing of a simple string."""
        encryptor = SHA256Encryption()
        result = encryptor.hash("hello")
        expected = hashlib.sha256("hello".encode('utf-8')).hexdigest()
        assert result == expected
    
    def test_hash_empty_string(self):
        """Test SHA256 hashing of empty string."""
        encryptor = SHA256Encryption()
        result = encryptor.hash("")
        expected = hashlib.sha256("".encode('utf-8')).hexdigest()
        assert result == expected


class TestSHA512Encryption:
    """Tests for SHA512Encryption class."""
    
    def test_hash_simple_string(self):
        """Test SHA512 hashing of a simple string."""
        encryptor = SHA512Encryption()
        result = encryptor.hash("hello")
        expected = hashlib.sha512("hello".encode('utf-8')).hexdigest()
        assert result == expected
    
    def test_hash_empty_string(self):
        """Test SHA512 hashing of empty string."""
        encryptor = SHA512Encryption()
        result = encryptor.hash("")
        expected = hashlib.sha512("".encode('utf-8')).hexdigest()
        assert result == expected


class TestSHA224Encryption:
    """Tests for SHA224Encryption class."""
    
    def test_hash_simple_string(self):
        """Test SHA224 hashing of a simple string."""
        encryptor = SHA224Encryption()
        result = encryptor.hash("hello")
        expected = hashlib.sha224("hello".encode('utf-8')).hexdigest()
        assert result == expected
    
    def test_hash_empty_string(self):
        """Test SHA224 hashing of empty string."""
        encryptor = SHA224Encryption()
        result = encryptor.hash("")
        expected = hashlib.sha224("".encode('utf-8')).hexdigest()
        assert result == expected


class TestSHA384Encryption:
    """Tests for SHA384Encryption class."""
    
    def test_hash_simple_string(self):
        """Test SHA384 hashing of a simple string."""
        encryptor = SHA384Encryption()
        result = encryptor.hash("hello")
        expected = hashlib.sha384("hello".encode('utf-8')).hexdigest()
        assert result == expected
    
    def test_hash_empty_string(self):
        """Test SHA384 hashing of empty string."""
        encryptor = SHA384Encryption()
        result = encryptor.hash("")
        expected = hashlib.sha384("".encode('utf-8')).hexdigest()
        assert result == expected


class TestBcryptEncryption:
    """Tests for BcryptEncryption class."""
    
    @patch('bcrypt.hashpw')
    @patch('bcrypt.gensalt')
    def test_hash_simple_string(self, mock_gensalt, mock_hashpw):
        """Test bcrypt hashing of a simple string."""
        mock_gensalt.return_value = b'$2b$12$test_salt'
        mock_hashpw.return_value = b'$2b$12$test_salt_hash'
        
        encryptor = BcryptEncryption()
        result = encryptor.hash("hello")
        
        # Verify bcrypt functions were called
        mock_gensalt.assert_called_once()
        mock_hashpw.assert_called_once_with("hello".encode('utf-8'), b'$2b$12$test_salt')
        assert result == b'$2b$12$test_salt_hash'
    
    @patch('bcrypt.hashpw')
    @patch('bcrypt.gensalt')
    def test_hash_empty_string(self, mock_gensalt, mock_hashpw):
        """Test bcrypt hashing of empty string."""
        mock_gensalt.return_value = b'$2b$12$test_salt'
        mock_hashpw.return_value = b'$2b$12$empty_hash'
        
        encryptor = BcryptEncryption()
        result = encryptor.hash("")
        
        mock_hashpw.assert_called_once_with("".encode('utf-8'), b'$2b$12$test_salt')
        assert result == b'$2b$12$empty_hash'
    
    @patch('bcrypt.hashpw')
    @patch('bcrypt.gensalt')
    def test_hash_unicode_string(self, mock_gensalt, mock_hashpw):
        """Test bcrypt hashing of unicode string."""
        mock_gensalt.return_value = b'$2b$12$test_salt'
        mock_hashpw.return_value = b'$2b$12$unicode_hash'
        
        encryptor = BcryptEncryption()
        result = encryptor.hash("héllo")
        
        mock_hashpw.assert_called_once_with("héllo".encode('utf-8'), b'$2b$12$test_salt')
        assert result == b'$2b$12$unicode_hash'
    
    def test_hash_real_bcrypt_functionality(self):
        """Test actual bcrypt functionality (integration test)."""
        encryptor = BcryptEncryption()
        password = "test_password"
        
        # Hash the password
        result = encryptor.hash(password)
        
        # Verify it's a bcrypt hash (should be bytes and start with $2b$)
        assert isinstance(result, bytes)
        assert result.startswith(b'$2b$')
        
        # Verify different calls produce different hashes (due to salt)
        result2 = encryptor.hash(password)
        assert result != result2  # Different salt should produce different hash
        
        # But both should be valid bcrypt hashes
        import bcrypt
        assert bcrypt.checkpw(password.encode('utf-8'), result)
        assert bcrypt.checkpw(password.encode('utf-8'), result2)


class TestEncryptionModulesComparison:
    """Tests comparing different encryption modules."""
    
    def test_different_algorithms_different_results(self):
        """Test that different algorithms produce different results."""
        password = "test_password"
        
        md5_result = MD5Encryption().hash(password)
        sha1_result = SHA1Encryption().hash(password)
        sha256_result = SHA256Encryption().hash(password)
        sha512_result = SHA512Encryption().hash(password)
        sha224_result = SHA224Encryption().hash(password)
        sha384_result = SHA384Encryption().hash(password)
        
        # All results should be different
        results = [md5_result, sha1_result, sha256_result, sha512_result, sha224_result, sha384_result]
        assert len(set(results)) == len(results)  # All unique
    
    def test_hash_lengths(self):
        """Test that different algorithms produce expected hash lengths."""
        password = "test_password"
        
        md5_result = MD5Encryption().hash(password)
        sha1_result = SHA1Encryption().hash(password)
        sha256_result = SHA256Encryption().hash(password)
        sha512_result = SHA512Encryption().hash(password)
        sha224_result = SHA224Encryption().hash(password)
        sha384_result = SHA384Encryption().hash(password)
        
        # Check expected lengths
        assert len(md5_result) == 32      # MD5 is 128 bits = 32 hex chars
        assert len(sha1_result) == 40     # SHA1 is 160 bits = 40 hex chars
        assert len(sha224_result) == 56   # SHA224 is 224 bits = 56 hex chars
        assert len(sha256_result) == 64   # SHA256 is 256 bits = 64 hex chars
        assert len(sha384_result) == 96   # SHA384 is 384 bits = 96 hex chars
        assert len(sha512_result) == 128  # SHA512 is 512 bits = 128 hex chars