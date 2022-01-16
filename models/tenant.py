from  db import db
from typing import List


class TenantModel(db.Model):
    """
    Class Tenants Model

    Returns:
        Model: blah blah
    """
    __tablename__ = "tenants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=False, unique=False)
    cert_store = db.Column(db.String(200), nullable=False, unique=True)
    tenant_logo_url = db.Column(db.String(100), nullable=True, unique=True)

    def __init__(self, name, description, cert_store=None, tenant_logo_url=None):
        self.name = name
        self.description = description
        self.cert_store = cert_store
        self.tenant_logo_url = tenant_logo_url
        
        
    def __repr__(self):
        return 'TenantModel(name=%s, description=%s, cert_store=%s, tenant_logo_url=%s)' \
            % (self.name, self.description,self.cert_store, self.tenant_logo_url)
    
    
    def json(self):
        return {'name': self.name, 'description': self.description, \
                'cert_store': self.cert_store, 'tenant_logo_url': self.tenant_logo_url }
    
    @classmethod
    def find_by_name(cls, name) -> "TenantModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "TenantModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["TenantModel"]:
        return cls.query.all()
    
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

