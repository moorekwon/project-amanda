from ._base import *

SECRETS = SECRETS_FULL['dev']

DEBUG = True
WSGI_APPLICATION = 'config.wsgi.dev.application'

ALLOWED_HOSTS += [
    '*'
]

DATABASES = SECRETS['DATABASES']
