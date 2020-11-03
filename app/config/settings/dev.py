from .base import *

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

# django debug toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]


MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]