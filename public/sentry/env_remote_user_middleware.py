import os

from django.contrib.auth.middleware import RemoteUserMiddleware

class EnvRemoteUserMiddleware(RemoteUserMiddleware):
    header = os.environ.get('REMOTE_USER_HEADER', 'REMOTE_USER')

    def configure_user(user):
        if 'REMOTE_USER_EMAIL_SUFFIX' in os.environ:
            user.email = "{0}{1}".format(user.username, os.environ['REMOTE_USER_EMAIL_SUFFIX'])
            user.save()
        return user
