from .base import *

ACTIVE_SETTING = 'test'

TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = BASE_DIR
TEST_DISCOVER_ROOT = BASE_DIR
TEST_DISCOVER_PATTERN = 'test_*'

########## IN-MEMORY TEST DATABASE
DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
},
}


#########################
# CUSTOM SETTINGS