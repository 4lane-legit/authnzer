from Crypto.PublicKey import RSA

class Cert:
    """
    Class to generate JWK private/public key certificates
    """
    key_size = 0

    @classmethod
    def set_keysize(self, key_size):
        self.key_size = key_size
        return self

    @classmethod
    def generate(self):
        key = RSA.generate(self.key_size)
        pubkey = key.publickey().exportKey('PEM')
        priv_key = key.exportKey('PEM')
        return  [pubkey.decode("utf-8"), priv_key.decode("utf-8")]

    