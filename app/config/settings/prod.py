from ._base import *

SECRETS = SECRETS_FULL['prod']

DEBUG = False
WSGI_APPLICATION = 'config.wsgi.prod.application'

ALLOWED_HOSTS += []

DATABASES = SECRETS['DATABASES']
