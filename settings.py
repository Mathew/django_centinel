# Django settings for django_centinel project.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

CENTINEL_PROCESSOR_ID = "123"
CENTINEL_MERCHANT_ID = "123"
CENTINEL_CALLBACK_URL = "http://callback.url"
CENTINEL_TRANSACTION_PASSWORD = "password"
CENTINEL_DEBUG = True
