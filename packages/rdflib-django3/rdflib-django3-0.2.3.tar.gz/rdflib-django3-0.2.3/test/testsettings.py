"""
Settings for testing the application.
"""
from django.conf.global_settings import *  # noqa
import os

DEBUG = True
SECRET_KEY = "FKJSLSOIIDSPOSOPDS"

DJANGO_RDFLIB_DEVELOP = True

DB_PATH = os.path.abspath(os.path.join(__file__, '..', 'rdflib_django.db'))

# TEST_RUNNER = "unittest.TextTestRunner"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_PATH,
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}

SITE_ID = 1

STATIC_URL = '/static/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'rdflib_django',
    )
ROOT_URLCONF = 'test.urls'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        },
    'loggers': {
        '': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
            },
        }
}
