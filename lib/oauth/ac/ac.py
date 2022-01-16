from lib.oauth.grant import AuthGrant
from models.auth_client import AuthClientModel
import logging

logger = logging.getLogger(__name__)
class AuthCodeGrant(AuthGrant):
    
    def authenticate_client(self, client_id, client_secret):
        return True
    
    def generate_access_token(self):
        return True