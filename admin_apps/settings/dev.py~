"""Settings for Development Server"""
from admin_apps.settings.base import *   # pylint: disable=W0614,W0401

DEBUG = True
TEMPLATE_DEBUG = DEBUG

VAR_ROOT = '/var/www/admin_apps'
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')
STATIC_ROOT = os.path.join(VAR_ROOT, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'admin_apps',
#        'USER': 'dbuser',
#        'PASSWORD': 'dbpassword',
    }
}

# WSGI_APPLICATION = 'admin_apps.wsgi.dev.application'
