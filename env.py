import os

os.environ['AWS_ENDPOINT_URL'] = 'http://host.docker.internal:4566'
os.environ['AWS_ACCESS_KEY_ID'] = 'foo'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'bar'
os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'
os.environ['BASE_URL_INTERNAL'] = 'http://hub.docker.internal:5000'
os.environ['RSA_KEYSIZE'] = '2048'