from authlib.jose import jwk

class JWTHelper:

    @staticmethod
    def generate_jwk(cert_pair):
        pub = jwk.dumps(cert_pair['pub'], kty='RSA')
        return pub
    