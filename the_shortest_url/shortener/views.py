from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.viewsets import GenericViewSet

from . import utils
from .serializers import DecodeSerializer, EncodeSerializer


class Encode(
    GenericViewSet,
    CreateAPIView,
):
    """
    This class is designed to shorten the url.
    """

    serializer_class = EncodeSerializer


class Decode(
    GenericViewSet,
    RetrieveAPIView
):
    """
    This class is designed to provide you the original url from the shortened one.
    """

    serializer_class = DecodeSerializer
    lookup_field = 'key'

    def get_object(self):
        key = self.kwargs[self.lookup_field]
        return {'url': utils.get_original_url(key)}
