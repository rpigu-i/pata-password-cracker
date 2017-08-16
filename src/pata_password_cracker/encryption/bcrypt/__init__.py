import bcrypt


class BcryptEncryption():

    def hash(self, pwd):
        """
        Return a bcrypt hash value
        """
        hash_val = bcrypt.hashpw(pwd, bcrypt.gensalt())
        return hash_val
