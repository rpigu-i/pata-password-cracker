import hashlib


class SHA224Encryption():
    def hash(self, pwd):
        """
        Return a sha224 hash value
        """
        hash_val = hashlib.sha224()
        hash_val.update(pwd.encode('utf-8'))
        return hash_val.hexdigest()
