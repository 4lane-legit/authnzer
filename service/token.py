import json
import logging
import jwt
from cache import redis_ins
from lib.oauth.grant_factory import OAuthGrantFactory

logger = logging.getLogger(__name__)
prefix = 'aws/tenant/certs/'

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
    
    @classmethod
    def introspect(cls, tenant_name: str, token: str):
        try:
            res = {}
            key = f'{prefix}{tenant_name}'
            certs = redis_ins.hgetall(key)
            is_valid = False if not jwt.decode(token, certs['pub'], ['RS256']) else True
            res['is_valid'] = is_valid
            return res
        except ValueError:
            logging.exception('Error occured verifying token')
            return False
        except jwt.exceptions.DecodeError:
            logging.exception('Tampered token!')
            return { "is_valid":  False}

