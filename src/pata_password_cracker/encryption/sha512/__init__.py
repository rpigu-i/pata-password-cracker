import hashlib


class SHA512Encryption():

    def hash(self, pwd):
        """
        Return a sha512 hash value
        """
        hash_val = hashlib.sha512()
        hash_val.update(pwd.encode('utf-8'))
        return hash_val.hexdigest()
