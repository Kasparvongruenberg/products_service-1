import uuid

from django.test import TestCase
from django.apps import apps
from products.apps import ProdcutsConfig

from .. import gunicorn_conf


class TestGunicornConf(TestCase):
    def setUp(self):
        self.user = uuid.uuid4()

    def test_config_values(self):
        self.assertEqual(gunicorn_conf.bind, '0.0.0.0:8080')
        self.assertEqual(gunicorn_conf.limit_request_field_size, 0)
        self.assertEqual(gunicorn_conf.limit_request_line, 0)


class CrmConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(ProdcutsConfig.name, 'products')
        self.assertEqual(apps.get_app_config('products').name, 'products')
