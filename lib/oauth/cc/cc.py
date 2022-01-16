import os
import time as t
import logging
import json
import jwt
from lib.oauth.grant import AuthGrant
from models.auth_client import AuthClientModel
from cache import redis_ins

logger = logging.getLogger(__name__)
class ClientCredentials(AuthGrant):

    prefix = 'aws/tenant/certs/'

    def authenticate_client(self, client_id, client_secret):
        try:

            client = AuthClientModel.find_by_client_id(client_id)
            if client is None:
                logger.info('Auth not found')
                return False
            if client.client_id == client_id and client.client_secret == client_secret:
                return True
        except ValueError:
            logger.exception('Some error occured while autheticating the client')
            return False

    def __set_token_settings(self):
        pass

    def generate_access_token(self, tenant_name, client):
        key = f'{self.prefix}{tenant_name}'
        client_id = client['client_id']
        client_secret = client['client_secret']
        if not self.authenticate_client(client_id, client_secret):
            return False
        
        payload = {
            "iss": f'{os.environ.get("BASE_URL_INTERNAL")}/api/tenant/{tenant_name}/auth',
            "exp": t.time() + 3600,
            "nbf": t.time()+10,
            "iat": t.time()+10,
            "jti": t.time(),
            "aud": client['audience']
        }

        certs = redis_ins.hgetall(key)
        access_token = jwt.encode(payload, certs['priv'], algorithm = 'RS256')
        return access_token


    def generate_refresh_token(self, tenant_name, client):
        pass
        




        
        
        

        