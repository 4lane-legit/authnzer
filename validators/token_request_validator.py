
from flask import request
from functools import wraps
from marshmallow.exceptions import ValidationError
from lib.oauth.attributes import Attributes
from lib.oauth.grant_factory import OAuthGrantFactory


def expect_grant():
    """
    Deprecated.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            _json = request.get_json()
            grant_type =  _json['grant_type'] if _json['grant_type'] else  None

            if grant_type is None:
                response = {
                    "status": "error",
                    "message": "Request JSON is missing some required params",
                    "missing": "grant type"
                }
                return response, 400

            _attrs = Attributes.attrs(grant_type)
            
            missing = [r for r in _attrs.keys()
                       if r not in _json]
            if missing:
                response = {
                    "status": "error",
                    "message": "Request JSON is missing some required params",
                    "missing": missing
                }
                return response, 400

            wrong_types = [r for r in _attrs.keys()
                           if not isinstance(_json[r], _attrs[r])]
            if wrong_types:
                response = {
                    "status": "error",
                    "message": "Data types in the request JSON doesn't match the required format",
                    # "param_types": {k: str(v) for k, v in _attrs.items()}
                    "wrong_types": wrong_types
                }
                return response, 400
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def validate_grant():
    """
    Better mechanism to traceback the schema validation on the basis of passed schema, schema validation would
    happen against the Marshmallow schemas.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                _json = request.get_json()
                grant_type =  _json['grant_type'] if _json['grant_type'] else  None
                if grant_type is None:
                    response = {
                        "status": "error",
                        "message": "Request JSON is missing some required params",
                        "missing": "grant type"
                    }
                    return response, 400
                schema = OAuthGrantFactory().get_grant_schema(grant_type)
                schema.load(request.get_json())
            except ValidationError as err:
                error = {
                    "status": "error",
                    "messages": err.messages
                }
                return error, 400
            return fn(*args, **kwargs)
        return wrapper
    return decorator
