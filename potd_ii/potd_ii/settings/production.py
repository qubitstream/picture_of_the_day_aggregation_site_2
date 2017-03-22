from os import environ, path
from .base import *


ALLOWED_HOSTS = [
    'localhost:8000',
    'localhost',
    'potd.remote',
    'www.potd.remote',
]

SITE_DOMAIN = get_env_setting_or_default('SITE_DOMAIN', r'http://www.potd.remote')

DEBUG = False

try:
    db_name = get_env_setting('POTD_II_POSTGRESQL_DB_NAME')
    db_user = get_env_setting('POTD_II_POSTGRESQL_DB_USER')
    db_password = get_env_setting('POTD_II_POSTGRESQL_DB_PW')
    DATABASES = {
       'default':  {
           'ENGINE': 'django.db.backends.postgresql_psycopg2',
           'NAME': db_name,
           'USER': db_user,
           'PASSWORD': db_password,
           'HOST': get_env_setting_or_default('POTD_II_POSTGRESQL_HOST', 'localhost'),
           'PORT': '',
        }
    }
except ImproperlyConfigured:
    pass  # use SQLite settings defined in base.py instead

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'pictureoftheday',
    }
}
