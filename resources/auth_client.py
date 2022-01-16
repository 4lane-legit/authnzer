from flask import request
from flask_restplus import Resource, fields, Namespace

from models.auth_client import AuthClientModel
from models.tenant import TenantModel
from resources.tenant import tenant_ns
from schemas.auth_client import AuthClientSchema
from service.oauth_client_setup import OAuthClientSetup

CLIENT_NOT_FOUND = "OAuth client not found."
CLIENT_ALREADY_EXISTS = "OAuth client '{}' Already exists."
INVALID_TENANT_PASSED = "Request could not be processed, tenant could not be found"

auth_client_ns = Namespace('oauth', description='Operations for oauth clients')

auth_client_schema = AuthClientSchema()
auth_client_list_schema = AuthClientSchema(many=True)

# Model required by flask_restplus for expect
auth_client = auth_client_ns.model('AuthClient', {
    'name': fields.String('Oauth client name'),
    'grant_type': fields.String('Oauth grant type'),
    'tenant': fields.String('Tenant name'),
    'allowed_scopes': fields.String('Allowed oauth scopes for this client')
})

class AuthClient(Resource):
    def get(self, client_id):
        """
        Get the information of the oauth client by client ID.
        """
        auth_client_data = AuthClientModel.find_by_client_id(client_id)
        if auth_client_data:
            return auth_client_schema.dump(auth_client_data)
        return {'message': CLIENT_NOT_FOUND}, 404

    def delete(self, client_id):
        """
        Delete the specific client by client ID.
        """
        auth_client_data = AuthClientModel.find_by_client_id(client_id)
        if auth_client_data:
            auth_client_data.delete_from_db()
            return {'message': "OAuth client deleted successfully"}, 200
        return {'message': CLIENT_NOT_FOUND}, 404


class AuthClientList(Resource):
    @tenant_ns.doc('Get all the oauth clients')
    def get(self, tenant_id):
        """
        Return all oauth clients configured for specific tenant.
        """
        return auth_client_list_schema.dump(AuthClientModel.find_clients_by_tenant(tenant_id)), 200

class AuthClientRegister(Resource):
    @auth_client_ns.expect(auth_client)
    @auth_client_ns.doc('Register a new oauth client')
    def post(self):
        """
        Register a new oauth client grant types supported are cc, auth_code, ropc.
        """
        auth_client_json = request.get_json()
        name = auth_client_json['name']
        allowed_scopes = auth_client_json['allowed_scopes']
        grant_type = auth_client_json['grant_type']

        tenant = TenantModel.find_by_name(auth_client_json['tenant'])
        if not tenant:
            return {'message': INVALID_TENANT_PASSED}, 400
        tenant_id = tenant.id
        if AuthClientModel.find_by_name(name):
            return {'message': CLIENT_ALREADY_EXISTS.format(name)}, 400

        client_res = OAuthClientSetup().get_oauthclient(name, allowed_scopes, grant_type, tenant_id)
        auth_client_data = auth_client_schema.load(client_res)
        auth_client_data.save_to_db()

        return auth_client_schema.dump(auth_client_data), 201