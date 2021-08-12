from rest_framework import serializers
from . import utils


class EncodeSerializer(serializers.Serializer): # noqa
    """
    This class will serialize the original url
    received from the user and create the shortened version.
    """
    url = serializers.URLField()

    def create(self, validated_data):
        original_url = validated_data['url']
        key = utils.shorten(url=original_url)
        shortened_url = utils.save_shortened_url(
            key=key,
            url=original_url,
            request=self.context['request']
        )
        return {'url': shortened_url}


class DecodeSerializer(serializers.Serializer): # noqa
    """
    This class will serialize the shortened url
    received from the user.
    """

    url = serializers.URLField()
