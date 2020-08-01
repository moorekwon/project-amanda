from ._base import *

SECRETS = SECRETS_FULL['dev']

DEBUG = True
WSGI_APPLICATION = 'config.wsgi.dev.application'

INSTALLED_APPS += [
    'django_extensions',
]

ALLOWED_HOSTS += [
    '*'
]

DATABASES = SECRETS['DATABASES']
