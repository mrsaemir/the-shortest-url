from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException, NotFound


class KeyCollisionError(APIException):
    """
    An exception showing that a key collision is happened in
    shortener's cache.
    """

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = _('Please try again later.')
    default_code = 'error'


class URLNotFound(NotFound):
    default_detail = _("The URL you are looking for does not exist.")
