from django.apps import AppConfig


class ShortenerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'the_shortest_url.shortener'
