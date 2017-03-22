from django.contrib.messages import constants as message_constants
from .base import *

DEBUG = True

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INSTALLED_APPS += (
    'debug_toolbar',
)

MESSAGE_LEVEL = message_constants.DEBUG
