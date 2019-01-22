"""pytest unit tests, to run:
DJANGO_SETTINGS_MODULE=products_service.settings.base py.test -v --cov
"""

import uuid

import pytest
from rest_framework.test import APIRequestFactory

from . import model_factories
from ..views import ProductViewSet


TEST_TYPE = 'test type'
TEST_WF2 = str(uuid.uuid4())


@pytest.fixture
def api_rf():
    return APIRequestFactory()


@pytest.fixture
def user():
    return model_factories.User()


@pytest.fixture
def products():
    return [
        model_factories.ProductFactory.create(),
        model_factories.ProductFactory.create(type=TEST_TYPE),
        model_factories.ProductFactory.create(workflowlevel2_uuid=TEST_WF2),
    ]


@pytest.mark.django_db()
def test_products_list_empty(api_rf, user):
    request = api_rf.get('')
    request.user = user
    response = ProductViewSet.as_view({'get': 'list'})(request)
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db()
def test_products_list(api_rf, user, products):
    request = api_rf.get('')
    request.user = user
    response = ProductViewSet.as_view({'get': 'list'})(request)
    assert response.status_code == 200
    assert len(response.data) == 3

    product_data = response.data[0]
    assert 'id' in product_data
    assert 'name' in product_data


@pytest.mark.django_db()
def test_products_list_with_name_filter(api_rf, user, products):
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


@pytest.mark.django_db()
def test_products_list_with_wf2_filter(api_rf, user, products):
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


@pytest.mark.django_db()
def test_products_empty_filter(api_rf, user, products):
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
