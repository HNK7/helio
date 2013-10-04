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
        'HOST': 'db.us.phoenixdart.com',
        'PORT': '5440',
        'USER': 'pxprogram',
        'PASSWORD': 'vlslrtm'
    }
}