import hashlib


class SHA1Encryption():

    def hash(self, pwd):
        """
        Return a sha1 hash value
        """
        hash_val = hashlib.sha1()
        hash_val.update(pwd.encode('utf-8'))
        return hash_val.hexdigest()
