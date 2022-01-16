
import env
from flask import Flask, Blueprint, jsonify
from flask_restplus import Api
from ma import ma
from db import db
from resources.tenant import Tenant, TenantList, TenantOpenId, TenantPublic, tenant_ns
from resources.auth_client import AuthClient, AuthClientList, AuthClientRegister, auth_client_ns
from resources.settings import Setting, SettingRegister, SettingsTemplates, settings_ns
from marshmallow import ValidationError
from config import Config
from resources.token import Token, TokenIntrospect

app = Flask(__name__)
app.config.from_object(Config)

bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint, doc='/doc', title='Pickaxe oauth provider', description="auth provider service, supporting all major oauth grant flavours")
app.register_blueprint(bluePrint)

api.add_namespace(tenant_ns)
api.add_namespace(auth_client_ns)
api.add_namespace(settings_ns)

@app.before_first_request
def create_tables():
    db.create_all()

@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400

# Routes:
# tenants module routes.
tenant_ns.add_resource(Tenant, '/<int:id>')
tenant_ns.add_resource(TenantOpenId, '/<string:tenant_name>/.well_known/open-id')
tenant_ns.add_resource(TenantPublic, '/<string:tenant_name>/auth')
tenant_ns.add_resource(TenantList, '')
tenant_ns.add_resource(AuthClientList, "/<int:tenant_id>/clients")

tenant_ns.add_resource(Token, '/<string:tenant_name>/token')
tenant_ns.add_resource(TokenIntrospect, '/<string:tenant_name>/introspect')

# oauth clients route module
auth_client_ns.add_resource(AuthClient, '/<string:client_id>')
auth_client_ns.add_resource(AuthClientRegister, "/register")

# settings route module.
settings_ns.add_resource(SettingRegister, '/register')
settings_ns.add_resource(SettingsTemplates, '/template')
settings_ns.add_resource(Setting, '')

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True,host='0.0.0.0')