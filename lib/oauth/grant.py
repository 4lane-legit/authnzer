from abc import ABC, abstractmethod


class AuthGrant(ABC):

    @abstractmethod
    def authenticate_client(self, client_id, client_secret):
        pass

    @abstractmethod    
    def generate_access_token(self):
        pass
