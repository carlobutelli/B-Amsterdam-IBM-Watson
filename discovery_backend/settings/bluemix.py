from discovery_backend.settings.base import *

import os

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])

postgresql_credentials_env = VCAP_SERVICES['postgresql'][0]['credentials']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': postgresql_credentials_env['name'],
        'USER': postgresql_credentials_env['user'],
        'PASSWORD': postgresql_credentials_env['password'],
        'HOST': postgresql_credentials_env['host'],
        'PORT': postgresql_credentials_env['port'],
    }
}