from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangostack',
        'HOST': 'dartoo.com',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': 'tnvkfdl2'
    },
    'hi': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'phoenix',
        'HOST': 'localhost',
        'PORT': '5400',
        'USER': 'pxprogram',
        'PASSWORD': 'vlslrtm'
    }
}
