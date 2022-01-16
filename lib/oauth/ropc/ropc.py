from lib.oauth.grant import AuthGrant
import logging

logger = logging.getLogger(__name__)
class ResourceOwnerPasswordGrant(AuthGrant):
    
    def authenticate_client(self, client_id, client_secret):
        pass
    
    def generate_access_token(self, tenant_name, client):
        pass