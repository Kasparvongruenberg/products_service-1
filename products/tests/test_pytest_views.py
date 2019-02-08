"""pytest unit tests, to run:
DJANGO_SETTINGS_MODULE=products_service.settings.base pytest -v --cov
"""
import pytest

from . import model_factories
from ..views import ProductViewSet

from .fixtures import user, products, TEST_TYPE, TEST_WF2


@pytest.mark.django_db()
class TestProductsList:

    def test_products_list_empty(self, api_rf, user):
        request = api_rf.get('')
        request.user = user
        response = ProductViewSet.as_view({'get': 'list'})(request)
        assert response.status_code == 200
        assert response.data == []

    def test_products_list(self, api_rf, user, products):
        request = api_rf.get('')
        request.user = user
        response = ProductViewSet.as_view({'get': 'list'})(request)
        assert response.status_code == 200
        assert len(response.data) == 3

        product_data = response.data[0]
        assert 'id' in product_data
        assert 'name' in product_data

    def test_products_list_with_name_filter(self, api_rf, user, products):
        request = api_rf.get('?type={}'.format(TEST_TYPE))
        request.user = user
        response = ProductViewSet.as_view({'get': 'list'})(request)
        assert response.status_code == 200
        assert len(response.data) == 1

        product_data = response.data[0]
        assert 'id' in product_data
        assert 'name' in product_data
        assert 'type' in product_data
        assert product_data['type'] == TEST_TYPE

    def test_products_list_with_wf2_filter(self, api_rf, user, products):
        request = api_rf.get('?workflowlevel2_uuid={}'.format(TEST_WF2))
        request.user = user
        response = ProductViewSet.as_view({'get': 'list'})(request)
        assert response.status_code == 200
        assert len(response.data) == 1

        product_data = response.data[0]
        assert 'id' in product_data
        assert 'name' in product_data
        assert 'workflowlevel2_uuid' in product_data
        assert product_data['workflowlevel2_uuid'] == TEST_WF2

    def test_products_empty_filter(self, api_rf, user, products):
        request = api_rf.get('?type={}'.format('nonexistent'))
        request.user = user
        response = ProductViewSet.as_view({'get': 'list'})(request)
        assert response.status_code == 200
        assert len(response.data) == 0

        request = api_rf.get('?workflowlevel2_uuid={}'.format('nonexistent'))
        request.user = user
        response = ProductViewSet.as_view({'get': 'list'})(request)
        assert response.status_code == 200
        assert len(response.data) == 0


@pytest.mark.django_db()
class TestProductsDetail:

    def test_product_detail(self, api_rf, user):
        product = model_factories.ProductFactory.create()

        request = api_rf.get('')
        request.user = user
        response = ProductViewSet.as_view({'get': 'retrieve'})(request,  uuid=str(product.uuid))  # noqa
        assert response.status_code == 200
        assert response.data

        assert response.data['id'] == product.pk
        assert response.data['uuid'] == str(product.uuid)
        assert 'name' in response.data
        assert 'workflowlevel2_uuid' in response.data

    def test_nonexistent_product(self, api_rf, user):
        request = api_rf.get('')
        request.user = user
        response = ProductViewSet.as_view({'get': 'retrieve'})(request, uuid='e70d4613-2055-4c95-9815-ea2f07210d55')  # noqa
        assert response.status_code == 404
