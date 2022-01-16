from sys import prefix
import boto3
import os
import json
from lib.aws.secretsmanager import SecretsManagerSecret
from lib.cert.cert import Cert
from lib.jwt.jwt_helper import JWTHelper
from cache import redis_ins
from lib.util.str_util import StrUtil

class TenantSetup:
    """
    Setup requirements for tenant secrets
    """
    secrets_manager = None
    prefix = 'aws/tenant/certs/'
    RSA_KEYSIZE = int(os.environ.get("RSA_KEYSIZE"))

    def set_tenant_name(self, name):
        """
        set the name of the tenant
        """
        self.name = name
        return self

    def __init__(self, name=None) -> None:
        if os.environ.get('AWS_ENDPOINT_URL'):
            self.secrets_manager = boto3.client("secretsmanager", endpoint_url = os.environ.get('AWS_ENDPOINT_URL'))
        else:
            self.secrets_manager = boto3.client("secretsmanager")
        self.name = name

    def setup_certs_in_cloud(self) -> str:
        """
        setup the cert strings in AWS cloud and pre load in Redis for easy use
        """
        cert = Cert.set_keysize(self.RSA_KEYSIZE).generate()
        key = f'{self.prefix}{self.name}'
        if cert is None:
            return False
        client = SecretsManagerSecret(self.secrets_manager)

        if redis_ins.exists(key):
           redis_ins.delete(key)
        secret = client.create(key, {'pub': cert[0], 'priv': cert[1]})
        redis_ins.hmset(key, {'pub': cert[0], 'priv': cert[1]})
        return secret['ARN']


    def setup_jwk(self) -> None:
        """
        Setup JWK string for the tenant
        """
        key = f'{self.prefix}{self.name}'
        if redis_ins.exists(key):
            certs = redis_ins.hgetall(key)
        certs = json.loads(certs.decode('utf-8'))
        return JWTHelper.generate_jwk(certs)
    	
    def get_issuer_info(self, secret=None):
        """
        Gets the public key and issuer info handy.
        """
        key = f'{self.prefix}{self.name}'
        response = {}
        response['tenant'] = self.name
        if redis_ins.exists(key):
            certs = redis_ins.hgetall(key)
            response['public_key'] = certs['pub']
        response['token_service'] = f'{os.environ.get("BASE_URL_INTERNAL")}/.well-known/open-id'
        return response
