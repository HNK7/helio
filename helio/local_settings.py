DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangostack',
        'HOST': '/Applications/djangostack-1.4.5-0/postgresql',
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

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)

FEES = {
    'CARD': 5,
    'MEMBERSHIP': 15,
}

TWILIO_ACCOUNT_SID = 'AC23c0e5f6e7a76d5a3680f3669f6e2d1a'
TWILIO_AUTH_TOKEN = '6d32191bbb9f19664bfe72e0771b5961'
