from .base import *  # noqa
from .base import env

DEBUG = True

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="d+rndt+l^57msx@r=o+^ja1_=y0yojt*ow0g8iaiuqgr#r!6e*"
)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

ALLOWED_HOSTS = [
    "127.0.0.1",
    "0.0.0.0"
]
