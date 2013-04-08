"""Settings for Development Server"""
from admin_apps.settings.base import *   # pylint: disable=W0614,W0401

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PW_FILE = '/var/www/pw'
f = open(PW_FILE)
un, pw = f.read().strip().split(':')

VAR_ROOT = '/var/www/admin_apps'
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')
STATIC_ROOT = os.path.join(VAR_ROOT, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'admin_apps',
        'USER': un,
        'PASSWORD': pw,
    }
}

# WSGI_APPLICATION = 'admin_apps.wsgi.dev.application'
