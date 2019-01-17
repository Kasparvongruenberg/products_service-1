from django.test import TestCase


class DocsViewTest(TestCase):

    def test_docs_success(self):
        response = self.client.get('/docs/')
        self.assertEqual(response.status_code, 200)

    def test_swagger_json_success(self):
        response = self.client.get('/docs/swagger.json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.info.title, 'Products Service API')
