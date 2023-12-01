"""
Base settings to build other settings files upon.
"""

import environ

from config.settings.common import *  # noqa

env = environ.Env()
env.read_env('.env')

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env('DJANGO_SECRET_KEY')

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
POSTGRES_USER = env('POSTGRES_USER')
POSTGRES_PASSWORD = env('POSTGRES_PASSWORD')
POSTGRES_HOST = env('POSTGRES_HOST')
POSTGRES_PORT = env('POSTGRES_PORT')
POSTGRES_DB = env('POSTGRES_DB')
DATABASE_URL=f'postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}'  # noqa

DATABASE_DEFAULT = dict(
    ENGINE='django.db.backends.postgresql',
    USER=POSTGRES_USER,
    PASSWORD=POSTGRES_PASSWORD,
    HOST=POSTGRES_HOST,
    PORT=POSTGRES_PORT,
    NAME=POSTGRES_DB,
    DATABASE_URL=DATABASE_URL,
)

DATABASES = {'default': DATABASE_DEFAULT}
DATABASES['default']['ATOMIC_REQUESTS'] = True
