from .base import *

# django - inmemory storage
DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# django debug toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]
