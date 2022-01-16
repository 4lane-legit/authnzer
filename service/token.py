import logging
from lib.oauth.grant_factory import OAuthGrantFactory

logger = logging.getLogger(__name__)

class TokenService:

    @classmethod
    def get_token(cls, tenant_name, client):
        try:
            token: dict = {}
            grant = OAuthGrantFactory.get_grant_object(client['grant_type'])
            token['access_token'] = grant.generate_access_token(tenant_name, client)
            if client['grant_type'] == "refresh_token":
                token['refresh_token'] = grant.generate_refresh_token(tenant_name, client)
            return token
        except ValueError:
            logging.exception('Error occured processing token')
            return False

