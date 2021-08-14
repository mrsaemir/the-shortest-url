from urllib import parse

from django.conf import settings
from django.core.cache import cache
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class URLShortenerTest(APITestCase):
    def setUp(self) -> None:
        # clear cache to avoid throttle tests affect other tests.
        cache.clear()

    def test_encodes_decodes_valid_url(self):
        """
        Testing if the encoder can successfully shorten a url
        """

        # check encode
        url = reverse('encode-list')
        payload = {'url': 'https://www.finn.auto/'}
        response_encode = self.client.post(url, payload)
        self.assertEqual(response_encode.status_code, status.HTTP_201_CREATED)
        # check if a url is returned in response
        self.assertIn('url', response_encode.data)
        self.assertIsNotNone(response_encode.data['url'])

        # check decode
        # extract the key of the returned shortened url
        shortened_path = parse.urlparse(response_encode.data['url']).path
        response_decode = self.client.get(shortened_path)
        self.assertEqual(response_decode.status_code, status.HTTP_200_OK)
        # check if the returned url is equal to our original url
        self.assertEqual(response_decode.data, payload)

    def test_encode_fails_with_invalid_url(self):
        """
        Testing if the encoder returns error when receiving invalid url
        """

        url = reverse('encode-list')
        data = {'url': 'This-is-an-invalid-url'}
        response = self.client.post(url, data)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_decode_fails_with_invalid_url(self):
        """
        Testing if a 404 is returned when we try to decode a url that does not exits.
        """
        url = reverse('decode-detail', args=['InVaLiD'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_encode_returns_different_shortened_urls(self):
        """
        Check that two different urls end up being shortened to two different results
        """
        url = reverse('encode-list')
        response_1 = self.client.post(url, data={'url': 'http://finn.auto/1'})
        response_2 = self.client.post(url, data={'url': 'http://finn.auto/2'})

        self.assertNotEqual(response_1.data, response_2.data)

    def test_encode_throttle(self):
        """
        Check that requests from suspicious users are being throttled
        """

        url = reverse('encode-list')
        for i in range(settings.ENCODER_THROTTLE_RATE):
            response = self.client.post(url, data={'url': f'http://finn.auto/{i}'})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, data={'url': f'http://finn.auto/throttle-it'})
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_decode_throttle(self):
        """
        Check that requests from suspicious users are being throttled
        """

        for i in range(settings.DECODER_THROTTLE_RATE):
            response = self.client.get(reverse('decode-detail', args=[i]))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(reverse('decode-detail', args=['invalid']))
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
