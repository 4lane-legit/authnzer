from flask import request
from flask_restplus import Resource, fields, Namespace
from models.tenant import TenantModel
from schemas.tenant import TenantSchema
from service.tenant_setup import TenantSetup

TENANT_NOT_FOUND = "Tenant not found."


tenant_ns = Namespace('tenant', description='API operations for setting up a tenant, this includes operations to register a new tenant.')

tenant_schema = TenantSchema()
tenant_list_schema = TenantSchema(many=True)

#Model required by flask_restplus for expect
tenant = tenant_ns.model('Tenant', {
    'name': fields.String('Name of the Tenant'),
    'description': fields.String('Description of the tenant account'),
    # 'cert_store': fields.String('Cert resource name stored on cloud'),
    'tenant_logo_url': fields.String('Logo URL string from cloud')
})

@tenant_ns.doc(False)
class Tenant(Resource):

    def get(self, id):
        """
        Get the information on the tenants by ID.
        """
        tenant_data = TenantModel.find_by_id(id)
        if tenant_data:
            return tenant_schema.dump(tenant_data)
        return {'message': TENANT_NOT_FOUND}, 404

    def delete(self, id):
        """
        Delete the info of tenant and also purge the associated keys.
        """
        tenant_data = TenantModel.find_by_id(id)
        if tenant_data:
            tenant_data.delete_from_db()
            return {'message': "Tenant Deleted successfully"}, 200
        return {'message': TENANT_NOT_FOUND}, 404

    @tenant_ns.expect(tenant)
    def put(self, id):
        """
        Edit the information of the tenant by ID.
        """
        tenant_data = TenantModel.find_by_id(id)
        tenant_json = request.get_json()

        if tenant_data:
            tenant_data.description = tenant_json['description']
            tenant_data.name = tenant_json['name']
        else:
            tenant_data = tenant_schema.load(tenant_json)

        tenant_data.save_to_db()
        return tenant_schema.dump(tenant_data), 200

class TenantList(Resource):
    # @tenant_ns.doc('Get the list of all the available tenants.')
    @tenant_ns.doc(False)
    def get(self):
        """
        Get the informaton of all the tenants.
        """
        return tenant_list_schema.dump(TenantModel.find_all()), 200

    @tenant_ns.expect(tenant)
    @tenant_ns.doc('Register a new tenant with the auth service.')
    def post(self):
        """
        Register a new oauth client for specific grant types.
        """
        tenant_json = request.get_json()
        secret = TenantSetup().set_tenant_name(tenant_json['name']).setup_certs_in_cloud()
        tenant_json['cert_store'] = secret
        tenant_data = tenant_schema.load(tenant_json)  
        tenant_data.save_to_db()

        return tenant_schema.dump(tenant_data), 201
    
class TenantOpenId(Resource):
    """
    Tenant Secrets and OIDC style wellknown endpoints
    """
    def get(self, tenant_name):
        """
        Get the open id scopes, this is the service discovery endpoint for a specific tenant.
        """
        tenant_data = TenantModel.find_by_name(tenant_name)
        if tenant_data:
            return None
        return {'message': TENANT_NOT_FOUND}, 404

class TenantPublic(Resource):
    """
    Tenant public key endpoint to fetch the info of public key to verify the JWT token.
    """
    def get(self, tenant_name):
        """
        This endpoint hosts the public key the token consumer to verify the tokens.
        """
        tenant_data = TenantModel.find_by_name(tenant_name)
        if tenant_data:
           return TenantSetup().set_tenant_name(tenant_name).get_issuer_info(tenant_data.cert_store)
        return {'message': TENANT_NOT_FOUND}, 404