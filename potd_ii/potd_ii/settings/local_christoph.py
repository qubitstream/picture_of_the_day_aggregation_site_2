from .local import *

ALLOWED_HOSTS += ['*']

if DEBUG:
    SITE_DOMAIN = ''