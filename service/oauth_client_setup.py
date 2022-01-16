import json
from lib.util.str_util import StrUtil


class OAuthClientSetup:
    """
    Setup requirements for oauth client secrets
    """
    def __init__(self) -> None:
        pass


    def get_oauthclient(self, name, scopes, grant_type, tenant_id):
        """
        :param name name of the client
        :param scopes: allowed scopes.
        :param grant_type: grant_type associated
        :return: OAuthClient object for OAuthClientModel Hydration
        """
        res = {}
        res['name'] = name
        res['client_id'] = StrUtil.uuid()
        res['client_secret'] = StrUtil.uuid_hex()
        res['allowed_scopes'] = json.loads(scopes)
        res['grant_type'] = grant_type
        res['tenant_id'] = tenant_id
        return res
        