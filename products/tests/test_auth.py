from django.test import TestCase
from rest_framework.test import APIRequestFactory

from ..views import ProductViewSet


class AnonymousRequestTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_unauthorized_request(self):
        request = self.factory.get('')
        response = ProductViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 403)

    def test_options_request(self):
        request = self.factory.options('')
        response = ProductViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
