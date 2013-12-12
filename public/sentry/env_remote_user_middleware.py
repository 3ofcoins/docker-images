import os

from django.contrib.auth.middleware import RemoteUserMiddleware

class EnvRemoteUserMiddleware(RemoteUserMiddleware):
    header = os.environ.get('REMOTE_USER_HEADER', 'REMOTE_USER')
