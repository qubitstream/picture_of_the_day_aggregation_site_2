from django.contrib.messages import constants as message_constants
from .base import *

DEBUG = True

INTERNAL_IPS = ['127.0.0.1']

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

INSTALLED_APPS += (
    'debug_toolbar',
)

MESSAGE_LEVEL = message_constants.DEBUG
