from flask_restplus import Resource, fields
from resources.tenant import tenant_ns
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
        return {}
