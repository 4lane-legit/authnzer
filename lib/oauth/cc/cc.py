import time as t
import logging
import json
import jwt
from lib.oauth.grant import AuthGrant
from models.auth_client import AuthClientModel
from cache import redis_ins

logger = logging.getLogger(__name__)
class ClientCredentials(AuthGrant):

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
        client_id = client['client_id']
        client_secret = client['client_secret']
        issuer = ''
        if not self.authenticate_client(client_id, client_secret):
            return False
        
        payload = {
            "iss": issuer,
            "exp": t.time() + 3600,
        }

        certs = redis_ins.get(tenant_name).decode('utf-8')
        certs = json.loads(certs)
        access_token = jwt.encode(payload, certs['priv'], algorithm = 'RS256')
        return access_token


    def generate_refresh_token(self, tenant_name, client):
        pass
        




        
        
        

        