from marshmallow import Schema, fields
 
class ClientCredentialsSchema(Schema):
    client_id = fields.String(required=True)
    client_secret = fields.String(required=True)
    audience = fields.List(fields.String, required=True)
    grant_type = fields.String(required=True)

class ROPSchema(Schema):
    client_id = fields.String(required=True)
    client_secret = fields.String(required=True)
    audience = fields.List(fields.String, required=True)
    grant_type = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    optional_scopes = fields.List(fields.String, required=True)

class AuthCodeSchema(Schema):
    client_id = fields.String(required=True)
    client_secret = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    optional_scopes = fields.List(fields.String, required=True)
    redirect_urls = fields.List(fields.String, required=True)