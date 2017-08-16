import hashlib


class SHA256Encryption():

    def hash(self, pwd):
        """
        Return a sha256 hash value
        """
        hash_val = hashlib.sha256()
        hash_val.update(pwd.encode('utf-8'))
        return hash_val.hexdigest()
