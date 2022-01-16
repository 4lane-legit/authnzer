
from typing import List


class Attributes:

    GRANT_ATTRS: dict = {
        'client_credentials': {
            'client_id': str,
            'client_secret': str,
            'audience': List
        },
        'ropc': {
            'client_id': str,
            'client_secret': str,
            'audience': List,
            'username': str,
            'password': str,
            'scopes': List
        },
        'auth_code': {
            'client_id': str,
            'client_secret': str,
            'audience': List,
            'username': str,
            'password': str,
            'scopes': List,
            'redirect_urls': List
        }
    }
    
    @staticmethod
    def attrs(type):
        """
        Returns all the auth grant attributes for a particular grant type
        """
        return Attributes.GRANT_ATTRS[type]
