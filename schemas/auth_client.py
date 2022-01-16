from ma import ma
from models.auth_client import AuthClientModel


class AuthClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AuthClientModel
        load_instance = True