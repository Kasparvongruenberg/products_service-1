import uuid

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from moto import mock_s3

from . import model_factories
from ..views import ProductViewSet
from ..models import Product
from .fixtures import user, products, product_with_file, TEST_TYPE, TEST_WF2


@pytest.mark.django_db()
class TestProductsList:

    def test_products_list_empty(self, api_rf, user):
        request = api_rf.get(reverse('product-list'))
        request.user = user
        response = ProductViewSet.as_view({'get': 'list'})(request)
        assert response.status_code == 200
        assert response.data == []

    def test_products_list(self, api_rf, user, products):
        request = api_rf.get(reverse('product-list'))
        request.user = user
        response = ProductViewSet.as_view({'get': 'list'})(request)
        assert response.status_code == 200
        assert len(response.data) == 3

        product_data = response.data[0]
        assert 'id' in product_data
        assert 'name' in product_data

    def test_products_list_with_name_filter(self, api_rf, user, products):
        request = api_rf.get('{}?type={}'.format(reverse('product-list'),
                                                 TEST_TYPE))
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
        request = api_rf.get('{}?workflowlevel2_uuid={}'.format(
            reverse('product-list'), TEST_WF2)
        )
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
        request = api_rf.get('{}?type={}'.format(reverse('product-list'),
                                                 'nonexistent'))
        request.user = user
        response = ProductViewSet.as_view({'get': 'list'})(request)
        assert response.status_code == 200
        assert len(response.data) == 0

        request = api_rf.get('{}?workflowlevel2_uuid={}'.format(
            reverse('product-list'), 'nonexistent')
        )
        request.user = user
        response = ProductViewSet.as_view({'get': 'list'})(request)
        assert response.status_code == 200
        assert len(response.data) == 0


@pytest.mark.django_db()
class TestProductsDetail:

    def test_product_detail(self, api_rf, user):
        product = model_factories.ProductFactory.create()

        request = api_rf.get(reverse('product-detail',
                                     args=(product.uuid,)))
        request.user = user
        response = ProductViewSet.as_view({'get': 'retrieve'})(request,  uuid=str(product.uuid))  # noqa
        assert response.status_code == 200
        assert response.data

        assert response.data['id'] == product.pk
        assert response.data['uuid'] == str(product.uuid)
        assert 'name' in response.data
        assert 'workflowlevel2_uuid' in response.data

    def test_nonexistent_product(self, api_rf, user):
        request = api_rf.get(reverse('product-detail', args=(222,)))
        request.user = user
        response = ProductViewSet.as_view({'get': 'retrieve'})(request, uuid='e70d4613-2055-4c95-9815-ea2f07210d55')  # noqa
        assert response.status_code == 404

    def test_product_with_file_detail(self, api_rf, user, product_with_file):
        request = api_rf.get(reverse('product-detail',
                                     args=(product_with_file.uuid,)))
        request.user = user
        response = ProductViewSet.as_view({'get': 'retrieve'})(
            request,  uuid=str(product_with_file.uuid)
        )
        assert response.status_code == 200
        assert response.data
        assert response.data['file'] == reverse('product-file',
                                                args=(product_with_file.uuid,))
        assert response.data['file_name'] == product_with_file.file_name


@mock_s3
@pytest.mark.django_db()
class TestProductsCreate:

    def test_create_product_with_file(self, api_rf, user, s3_conn):
        file_mock = SimpleUploadedFile('foo.pdf', b'some content',
                                       content_type='multipart/form-data')
        data = {
            'workflowlevel2_uuid': str(uuid.uuid4()),
            'name': 'Test name',
            'file': file_mock,
            'file_name': 'bar.pdf',
        }
        request = api_rf.post(reverse('product-list'), data)
        request.user = user
        response = ProductViewSet.as_view({'post': 'create'})(request)
        assert response.status_code == 201

        product = Product.objects.get(id=response.data['id'])
        assert product.file
        assert product.file_name == 'bar.pdf'
        assert response.data['file'] == reverse('product-file',
                                                args=(product.uuid,))

    def test_create_product_with_file_without_name(self, api_rf, user,
                                                   s3_conn):
        file_mock = SimpleUploadedFile('foo.pdf', b'some content',
                                       content_type='multipart/form-data')
        data = {
            'workflowlevel2_uuid': str(uuid.uuid4()),
            'name': 'Test name',
            'file': file_mock,
        }
        request = api_rf.post(reverse('product-list'), data)
        request.user = user
        response = ProductViewSet.as_view({'post': 'create'})(request)
        assert response.status_code == 201

        product = Product.objects.get(id=response.data['id'])
        assert product.file
        assert product.file_name == 'foo.pdf'


@mock_s3
@pytest.mark.django_db()
class TestProductsUpdate:

    def test_create_product_with_file(self, api_rf, user, s3_conn):
        file_mock = SimpleUploadedFile('foo.pdf', b'some content',
                                       content_type='multipart/form-data')
        data = {
            'workflowlevel2_uuid': str(uuid.uuid4()),
            'name': 'Test name',
            'file': file_mock,
            'file_name': 'bar.pdf',
        }
        request = api_rf.post(reverse('product-list'), data)
        request.user = user
        response = ProductViewSet.as_view({'post': 'create'})(request)
        assert response.status_code == 201

        product = Product.objects.get(id=response.data['id'])
        assert product.file
        assert product.file_name == 'bar.pdf'
        assert response.data['file'] == reverse('product-file',
                                                args=(product.uuid,))


@mock_s3
@pytest.mark.django_db()
class TestProductFile:

    def test_product_file(self, api_rf, user, product_with_file):
        request = api_rf.get(reverse('product-file',
                                     args=(product_with_file.uuid,)))
        request.user = user
        response = ProductViewSet.as_view({'get': 'file'})(
            request, uuid=product_with_file.uuid
        )
        assert response.status_code == 200
        assert response['Content-Disposition'] == 'attachment; filename={}'\
            .format(product_with_file.file_name)
