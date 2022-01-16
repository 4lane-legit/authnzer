from typing import List


class Attributes:

    __attrs: dict = {
        'client_credentials': {
            'client_id': str,
            'client_secret': str,
            'audience': List
        },
        'ropc': {
            'client_id': 'required',
            'client_secret': 'required',
            'audience': 'required',
            'username': 'required',
            'password': 'required',
            'scopes': 'optional'
        },
        'auth_code': {
            'client_id': 'required',
            'client_secret': 'required',
            'audience': 'required',
            'username': 'required',
            'password': 'required',
            'scopes': 'optional',
            'redirect_urls': 'required'
        }
    }
    @staticmethod
    def attrs(type):
        """
        Returns all the auth grant attributes for a particular grant type
        """
        return Attributes.__attrs[type]
