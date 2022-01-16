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

    def setup_certs_in_cloud(self) -> bool:
        """
        setup the cert strings in AWS cloud and pre load in Redis for easy use
        """
        cert = Cert().set_keysize(self.RSA_KEYSIZE).generate()
        if cert is None:
            return False
        client = SecretsManagerSecret(self.secrets_manager)

        secret = client.create(self.prefix+self.name, {'pub': cert[0], 'priv': cert[1]})
        if redis_ins.exists(self.name):
           redis_ins.delete(self.name)

        redis_ins.set(self.name, json.dumps({'pub': cert[0], 'priv': cert[1]}))
        return secret['ARN']


    def setup_jwk(self) -> None:
        """
        Setup JWK string for the tenant
        """
        if redis_ins.exists(self.name):
            certs = redis_ins.get(self.name)
        certs = json.loads(certs.decode('utf-8'))
        return JWTHelper.generate_jwk(certs)
    	
    def get_issuer_info(self, secret_arn) -> None:
        """
        Gets the public key and issuer info handy.
        """
        response = {}
        response['tenant'] = self.name
        if redis_ins.exists(self.name):
            certs = redis_ins.get(self.name)
            certs = json.loads(certs.decode('utf-8'))
            response['public_key'] = StrUtil.strip_key_headers(certs['pub'])
        response['token_service'] = f'{os.environ.get("BASE_URL_INTERNAL")}/.well-known/open-id'
        return response
