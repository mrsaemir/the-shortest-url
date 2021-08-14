"""
The production settings file for the_shortest_url project.
Note that this is a sample production.py file and is here for
demonstration purposes. The real file has many other properties
such as logging handlers that send critical events to email, connect to
crash report services, etc.
You may add more features to this file as the project grows.
"""

from .base import *  # noqa
from .base import env

SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# We should change this to something like REDIS for production
# but for now it is ok.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}


REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
]

STATIC_ROOT = '/home/static'
