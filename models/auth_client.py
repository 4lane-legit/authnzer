from enum import unique
from typing import List
from  db import db


class AuthClientModel(db.Model):
    """
    This class is ...
    """
    __tablename__ = "oauth_clients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    client_id = db.Column(db.String(36), nullable=True, unique=True)
    client_secret = db.Column(db.String(72), nullable=True, unique=True)
    allowed_scopes = db.Column(db.JSON, nullable=True, unique=False)
    grant_type = db.Column(db.String(100), nullable=False, unique=False)
    tenant_id = db.Column(db.Integer)


    def __init__(
        self, 
        name,
        client_id,
        client_secret=None, 
        allowed_scopes=None, 
        grant_type=None,
        tenant_id=None
        ):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.allowed_scopes = allowed_scopes
        self.grant_type = grant_type
        self.tenant_id = tenant_id

    def __repr__(self):
        return 'AuthClientModel(name=%s, client_id=%s, client_secret=%s, \
            allowed_scopes=%s, grant_type=%s, tenant_id=%s)' \
            % (self.name, self.client_id, self.client_secret, self.allowed_scopes, self.grant_type, self.tenant_id)
    

    def json(self):
        return {'name': self.name, 'client_id': self.client_id, \
                'allowed_scopes': self.allowed_scopes, 'grant_type': self.grant_type }

    @classmethod
    def find_by_name(cls, name) -> "AuthClientModel":
        """
        :param name
        :return 
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "AuthClientModel":
        """
        :param id
        :return
        """
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["AuthClientModel"]:
        """
        :return
        """
        return cls.query.all()

    @classmethod
    def find_by_client_id(cls, client_id) -> "AuthClientModel":
        """
        :return
        """
        return cls.query.filter_by(client_id=client_id).first()
    
    @classmethod
    def find_clients_by_tenant(cls, tenant_id):
        """
        :return
        """
        return cls.query.filter_by(tenant_id=tenant_id).all()

    def save_to_db(self) -> None:
        """
        :return
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """
        :return
        """
        db.session.delete(self)
        db.session.commit()
