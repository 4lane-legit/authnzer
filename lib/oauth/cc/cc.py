from datetime import time
import logging
import jwt
from lib.oauth.grant import AuthGrant
from models.auth_client import AuthClientModel
from resources.tenant import Tenant
from cache import redis_ins

logger = logging.getLogger(__name__)
class ClientCredentials(AuthGrant):

    issuer: str

    def __init__(self, issuer=None) -> None:
        self.issuer = issuer

    def __authenticate_client(self, client_id, client_secret):
        try:

            client = AuthClientModel.find_by_client_id(client_id)
            if client is None:
                logger.info('Auth not found')
                return False
            if client.client_id == client_id and client.client_secret == client_secret:
                return True
        except Exception:
            logger.exception('Some error occured while autheticating the client')
            return False

    def set_issuer(self, issuer):
        self.issuer = issuer
        return self

    def set_token_settings(self): 
        pass

    def generate_access_token(self, tenant_name, client_id, client_secret):
        if not self.__authenticate_client(client_id, client_secret):
            return False
        
        payload = {
            "iss": self.issuer,
            "exp": time.time() + 3600,
        }

        certs = redis_ins.get(tenant_name)
        return ""

        




        
        
        

        