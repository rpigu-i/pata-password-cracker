import hashlib


class MD5Encryption():
    def hash(self, pwd):
        """
        Return a md5 hash value
        """
        hash_val = hashlib.md5()
        hash_val.update(pwd.encode('utf-8'))
        return hash_val.hexdigest()
