import os
import datetime
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..'))


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = 'Set the {} env variable'.format(setting)
        raise ImproperlyConfigured(error_msg)


def get_env_setting_or_default(setting, default_val):
    """ Get the environment setting or given default value """
    try:
        return os.environ[setting]
    except KeyError:
        return default_val


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_setting('POTD_II_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'easy_thumbnails',
    'rest_framework',
    'django_filters',
    'core',
    'picture_of_the_day',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'potd_ii.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                ###
                'core.context_processors.core',
            ],
        },
    },
]

WSGI_APPLICATION = 'potd_ii.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'potd_ii_db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, '..', 'logs', 'potd_app.log'),
            'formatter': 'verbose'
        },
        'management_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, '..', 'logs', 'potd_management.log'),
            'formatter': 'verbose'
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'django_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, '..', 'logs', 'potd_django.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['django_file', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'management': {
            'handlers': ['management_file', 'console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

for appname in 'core,picture_of_the_day'.split(','):
    LOGGING['loggers'][appname] = {
        'handlers': ['file', 'console'],
        'level': 'DEBUG',
    }



##################
# General settings
##################

POTD_AT_START = datetime.date(2004, 5, 14)

CACHE_TIME_POTD_LIST = 60 * 60
CACHE_TIME_POTD_DETAIL = 60 * 60

ALLOWED_IMAGE_EXTENSIONS = tuple('.jpg,.jpeg,.gif,.png,.svg'.lower().split(','))

THUMBNAIL_ALIASES = {
    '': {
        'potd2000': {'size': (2000, 2000), 'upscale': False},
        'potd1200': {'size': (1200, 1200), 'upscale': False},
        'potd600': {'size': (600, 600), 'upscale': False},
        'potd400x400': {'size': (400, 400), 'crop': 'smart', 'upscale': True},
    },
}

THUMBNAIL_ALIASES_TO_PREGENERATE = ['potd400x400', 'potd1200']

# The maximum length of the longest side of the image
THUMBNAIL_MAX_SCRAPE_SIZE = int(get_env_setting_or_default('THUMBNAIL_MAX_SCRAPE_SIZE', 2400))

NAME_OF_SITE_LONG = 'Picture of the Day'
NAME_OF_SITE_SHORT = 'PotD'

SITE_DOMAIN = get_env_setting_or_default('POTD_II_SITE_DOMAIN', 'http://localhost:8000')

ACTIVE_SETTING = get_env_setting('DJANGO_SETTINGS_MODULE').split('.')[-1]
