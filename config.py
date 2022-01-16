import os
from typing import List

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    DEBUG = True
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@host.docker.internal:3306/pickaxe'
    SQLALCHEMY_TRACK_MODIFICATIONS = ''
    PROPAGATE_EXCEPTIONS = ''
    REDIS_HOST = 'host.docker.internal'