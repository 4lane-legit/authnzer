from flask_restplus import Resource, fields
from flask import request
from service.token import TokenService
from validators.token_request_validator import validate_grant
from resources.tenant import tenant_ns

prefix = 'aws/tenant/certs/'
#Model required by flask_restplus for expect
token = tenant_ns.model('Token', {
    'token': fields.String('JWT token')
})

class Token(Resource):
    """
    Tenant public key endpoint to fetch the info of public key to verify the JWT token.
    """
    @validate_grant()
    def post (self, tenant_name):
        """
        Generates the access token of the specific type
        """
        auth_client_json = request.get_json()
        return TokenService.get_token(tenant_name, auth_client_json), 200
    
class TokenIntrospect(Resource):
    @tenant_ns.expect(token)
    def get (self, tenant_name):
        """
        Token introspection endpoint
        """
        token = request.get_json()
        token = token['token']
        return TokenService.introspect(tenant_name, token), 200