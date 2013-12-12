# This file is just Python, with a touch of Django which means you
# you can inherit and tweak settings to your hearts content.
from sentry.conf.server import *

import os, os.path, urlparse

_memcache_url = urlparse.urlparse(os.environ['MEMCACHE_PORT']) if 'MEMCACHE_PORT' in os.environ else None
_redis_url =    urlparse.urlparse(os.environ['REDIS_PORT'])    if 'REDIS_PORT'    in os.environ else None
_redis_db = int(os.environ['REDIS_DATABASE']) if os.environ['REDIS_DATABASE'] else 0

CONF_ROOT = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': os.environ['PGDATABASE'],
        'USER': os.environ['PGUSER'],
        'PASSWORD': os.environ['PGPASSWORD'],
        'HOST': os.environ['PGHOST'],
        'PORT': os.environ['PGPORT'],

        # If you're using Postgres, we recommend turning on autocommit
        'OPTIONS': { 'autocommit': True, }
    }
}


# If you're expecting any kind of real traffic on Sentry, we highly recommend
# configuring the CACHES and Redis settings

###########
## CACHE ##
###########

# You'll need to install the required dependencies for Memcached:
#   pip install python-memcached
#

if _memcache_url:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': [ _memcache_url.netloc ],
        }
    }

###########
## Queue ##
###########

# See http://sentry.readthedocs.org/en/latest/queue/index.html for more
# information on configuring your queue broker and workers. Sentry relies
# on a Python framework called Celery to manage queues.

# You can enable queueing of jobs by turning off the always eager setting:
if _redis_url and 'CELERY_ALWAYS_EAGER' not in os.environ:
    CELERY_ALWAYS_EAGER = False
    BROKER_URL = 'redis://{0}/{1}'.format(_redis_url.netloc, _redis_db)

####################
## Update Buffers ##
####################

# Buffers (combined with queueing) act as an intermediate layer between the
# database and the storage API. They will greatly improve efficiency on large
# numbers of the same events being sent to the API in a short amount of time.
# (read: if you send any kind of real data to Sentry, you should enable buffers)

# You'll need to install the required dependencies for Redis buffers:
#   pip install redis hiredis nydus
#

if _redis_url:
    SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'
    SENTRY_REDIS_OPTIONS = {
        'hosts': {
            0: {
                'host': _redis_url.hostname,
                'port': _redis_url.port,
                'db': _redis_db,
            }
        }
    }

################
## Web Server ##
################

# You MUST configure the absolute URI root for Sentry:
SENTRY_URL_PREFIX = os.environ.get('SENTRY_URL_PREFIX', 'http://sentry.example.com')  # No trailing slash!

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SENTRY_WEB_HOST = '0.0.0.0'
SENTRY_WEB_PORT = 9000
SENTRY_WEB_OPTIONS = {
    'workers': int(os.environ.get('SENTRY_WEB_WORKERS', 3)),  # the number of gunicorn workers
    'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
}

if 'SENTRY_WEB_REMOTE_USER_AUTH' in os.environ:
    from django.contrib.auth.middleware import RemoteUserMiddleware
    RemoteUserMiddleware.header = os.environ['SENTRY_WEB_REMOTE_USER_AUTH']
    
    MIDDLEWARE_CLASSES += ( 'django.contrib.auth.middleware.RemoteUserMiddleware', )
    AUTHENTICATION_BACKENDS = ( 'django.contrib.auth.backends.RemoteUserBackend', )

ALLOWED_HOSTS = [ '*' ]

#################
## Mail Server ##
#################

# For more information check Django's documentation:
#  https://docs.djangoproject.com/en/1.3/topics/email/?from=olddocs#e-mail-backends

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'localhost'
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_PORT = 25
EMAIL_USE_TLS = False

# The email address to send on behalf of
SERVER_EMAIL = 'root@localhost'

###########
## etc. ##
###########

# If this file ever becomes compromised, it's important to regenerate your SECRET_KEY
# Changing this value will result in all current sessions being invalidated
SECRET_KEY = open('/etc/sentry/secret').read().strip()

# http://twitter.com/apps/new
# It's important that input a callback URL, even if its useless. We have no idea why, consult Twitter.
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

# http://developers.facebook.com/setup/
FACEBOOK_APP_ID = ''
FACEBOOK_API_SECRET = ''

# http://code.google.com/apis/accounts/docs/OAuth2.html#Registering
GOOGLE_OAUTH2_CLIENT_ID = ''
GOOGLE_OAUTH2_CLIENT_SECRET = ''

# https://github.com/settings/applications/new
GITHUB_APP_ID = ''
GITHUB_API_SECRET = ''

# https://trello.com/1/appKey/generate
TRELLO_API_KEY = ''
TRELLO_API_SECRET = ''

# https://confluence.atlassian.com/display/BITBUCKET/OAuth+Consumers
BITBUCKET_CONSUMER_KEY = ''
BITBUCKET_CONSUMER_SECRET = ''
