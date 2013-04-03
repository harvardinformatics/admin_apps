"""
Example settings for local development

Use this file as a base for your local development settings and copy
it to admin_apps/settings/local.py. It should not be checked into
your code repository.

"""
from admin_apps.settings.base import *   # pylint: disable=W0614,W0401

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Eric', 'mattison@g.harvard.edu'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(VAR_ROOT, 'dev.db'),
    }
}

# ROOT_URLCONF = 'admin_apps.urls.local'
# WSGI_APPLICATION = 'admin_apps.wsgi.local.application'
