from lib.oauth.ac.ac import AuthCodeGrant
from lib.oauth.cc.cc import ClientCredentials
from schemas.grants import AuthCodeSchema, ClientCredentialsSchema

class OAuthGrantFactory:

    def get_grant_object(self, grant_type):
        if grant_type == 'client_credentials':
            return ClientCredentials()
        elif grant_type == 'auth_code':
            return AuthCodeGrant()
        else:
            raise ValueError(grant_type)

        
    def get_grant_schema(self, grant_type):
        if grant_type == 'client_credentials':
            return ClientCredentialsSchema()
        elif grant_type == 'auth_code':
            return AuthCodeSchema()
        else:
            raise ValueError(grant_type)
