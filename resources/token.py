from flask_restplus import Resource
from flask import request
from resources.tenant import tenant_ns
from service.token import TokenService
from validators.token_request_validator import validate_grant

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
