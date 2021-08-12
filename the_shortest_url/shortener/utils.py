import hashlib
import time
from random import choice
from string import ascii_lowercase, ascii_uppercase
from typing import Union

from django.conf import settings
from django.core.cache import cache
from rest_framework.reverse import reverse_lazy

from . import exceptions


def shorten(
        url: str,
        length: int = settings.SHORTENER_LENGTH,
        with_salt: bool = True
) -> str:

    """
    returns the shortened version of the url in the requested size.
    calling this function with same urls does not return the same outputs unless with_salt is False.
    A hash function is used instead of randomly generating a key for each url.
    The reason is that a hash function (without a salt) could be used to re-generate the same key for the same url
    which can be useful if we need such a feature.
    Also, great Linus Torvalds has used a hash function as a key in his great project: GIT
    """

    # a couple of things are mixed together in order to create a unique key
    # for each url and avoid collisions.
    _hash = hashlib.sha1()
    _hash.update(url.encode())

    if with_salt:
        for item in [
            str(time.time_ns()),
            "".join(choice([ascii_lowercase, ascii_uppercase]) for i in range(20))
        ]:
            # update will just concatenate the items together.
            # https://docs.python.org/3/library/hashlib.html#hashlib.hash.update
            _hash.update(item.encode())

    key = _hash.hexdigest()[-length:]
    # the output of a hash function is always lowercase,
    # so to generate a key which has both uppercase and lowercase letters
    # we change some characters to uppercase ones randomly.
    # this will decrease the chance of collision. Although a collision is
    # very rare because of the mixture we created above when with_salt = True.
    return ''.join(
        choice((str.upper, str.lower))(char) for char in key  # noqa
    )


def save_shortened_url(key: str, url: str, request) -> str:
    """
    This function will save the url with the key to django's cache.
    If another url exists with that key, it will raise KeyCollisionError.
    otherwise an absolute url will be returned as a result.
    """

    # Either gets the current value in cache or sets a new one.
    result = cache.get_or_set(
        key,
        url,
        timeout=None
    )

    if result != url:
        # This will check if the url in cache is the url we want to shorten.
        # the non-equality of result and url means that a collision is happened.
        # if a key collision happens, an error will be raised to
        # tell the user to try again later.
        raise exceptions.KeyCollisionError()

    return reverse_lazy('decode-detail', args=[key], request=request)


def get_original_url(key: str) -> Union[str, None]:
    result = cache.get(key)
    if not result:
        raise exceptions.URLNotFound()
    return result
