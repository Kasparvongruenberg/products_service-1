import uuid

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from . import model_factories
from ..views import ProductViewSet, PropertyViewSet
from ..models import Product, Property


class ProductViewsBaseTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = model_factories.User()


class ProductListTest(ProductViewsBaseTest):

    def test_products_list_empty(self):
        request = self.factory.get('')
        request.user = self.user
        response = ProductViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_products_list(self):
        model_factories.ProductFactory.create_batch(3)

        request = self.factory.get('')
        request.user = self.user
        response = ProductViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

        product_data = response.data[0]
        self.assertTrue('id' in product_data)
        self.assertTrue('name' in product_data)

    def test_products_list_with_name_filter(self):
        test_type = 'test type'
        model_factories.ProductFactory.create(type=test_type)

        request = self.factory.get('?type={}'.format(test_type))
        request.user = self.user
        response = ProductViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        product_data = response.data[0]
        self.assertTrue('id' in product_data)
        self.assertTrue('name' in product_data)
        self.assertTrue('type' in product_data)
        self.assertEqual(product_data['type'], test_type)

    def test_products_list_with_wf2_filter(self):
        test_wf2 = str(uuid.uuid4())
        model_factories.ProductFactory.create(workflowlevel2_uuid=test_wf2)

        request = self.factory.get('?workflowlevel2_uuid={}'.format(test_wf2))
        request.user = self.user
        response = ProductViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        product_data = response.data[0]
        self.assertTrue('id' in product_data)
        self.assertTrue('name' in product_data)
        self.assertTrue('workflowlevel2_uuid' in product_data)
        self.assertEqual(product_data['workflowlevel2_uuid'], test_wf2)

    def test_products_empty_filter(self):
        request = self.factory.get('?type={}'.format('nonexistent'))
        request.user = self.user
        response = ProductViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        request = self.factory.get('?workflowlevel2_uuid={}'
                                   .format('nonexistent'))
        request.user = self.user
        response = ProductViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_property_list_empty(self):
        request = self.factory.get('')
        request.user = self.user
        view = PropertyViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])


class ProductDetailTest(ProductViewsBaseTest):

    def test_product_detail(self):
        product = model_factories.ProductFactory.create()

        request = self.factory.get('')
        request.user = self.user
        response = ProductViewSet.as_view({'get': 'retrieve'})(request,
                                                               pk=product.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)

        self.assertEqual(response.data['id'], product.pk)
        self.assertTrue('name' in response.data)
        self.assertTrue('workflowlevel2_uuid' in response.data)

    def test_nonexistent_product(self):
        request = self.factory.get('')
        request.user = self.user
        response = ProductViewSet.as_view({'get': 'retrieve'})(request,
                                                               pk=1001)
        self.assertEqual(response.status_code, 404)


class ProductCreateTest(ProductViewsBaseTest):

    def test_create_product(self):
        data = {
            'workflowlevel2_uuid': str(uuid.uuid4()),
            'name': 'Test name',
            'make': 'Test company',
            'type': 'Test type',
            'description': 'Foo bar foo bar',
            'status': 'in-stock',
        }
        request = self.factory.post('', data)
        request.user = self.user
        response = ProductViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)

        product = Product.objects.get(id=response.data['id'])
        self.assertEqual(product.workflowlevel2_uuid,
                         data['workflowlevel2_uuid'])
        self.assertEqual(product.name, data['name'])
        self.assertEqual(product.make, data['make'])
        self.assertEqual(product.type, data['type'])
        self.assertEqual(product.description, data['description'])
        self.assertEqual(product.status, data['status'])

    def test_create_product_fail(self):
        data = {
            'workflowlevel2_uuid': str(uuid.uuid4()),
            'name': '',
        }
        request = self.factory.post('', data)
        request.user = self.user
        response = ProductViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)


class ProductUpdateTest(ProductViewsBaseTest):

    def test_update_product(self):

        product = model_factories.ProductFactory.create()
        data = {
            'workflowlevel2_uuid': str(uuid.uuid4()),  # changing
            'name': 'New name',  # changing
            'make': product.make,
            'model': product.model,
            'type': product.type,
            'status': product.status,
        }
        request = self.factory.put('', data)
        request.user = self.user
        response = ProductViewSet.as_view({'put': 'update'})(request,
                                                             pk=product.pk)
        self.assertEqual(response.status_code, 200)

        product = Product.objects.get(id=response.data['id'])
        self.assertEqual(product.workflowlevel2_uuid,
                         data['workflowlevel2_uuid'])
        self.assertEqual(product.name, data['name'])

    def test_update_product_fail(self):
        product = model_factories.ProductFactory.create()
        data = {
            'name': '',
        }
        request = self.factory.put('', data)
        request.user = self.user
        response = ProductViewSet.as_view({'put': 'update'})(request,
                                                             pk=product.pk)
        self.assertEqual(response.status_code, 400)


class PropertyListTest(ProductViewsBaseTest):

    def test_property_list(self):
        products = model_factories.ProductFactory.create_batch(2)

        prop1 = model_factories.PropertyFactory.create()
        prop2 = model_factories.PropertyFactory.create(products=products[:1])
        prop3 = model_factories.PropertyFactory.create(products=products)

        request = self.factory.get('')
        request.user = self.user
        response = PropertyViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

        for prop_data in response.data:
            if prop_data['id'] == prop1.pk:
                self.assertEqual(prop_data['product'], [])
            elif prop_data['id'] == prop2.pk:
                self.assertEqual(len(prop_data['product']), 1)
            elif prop_data['id'] == prop3.pk:
                self.assertEqual(len(prop_data['product']), 2)


class PropertyDetailTest(ProductViewsBaseTest):

    def test_property_daetail(self):
        products = model_factories.ProductFactory.create_batch(2)
        prop = model_factories.PropertyFactory.create(products=products)

        request = self.factory.get('')
        request.user = self.user
        response = PropertyViewSet.as_view({'get': 'retrieve'})(request,
                                                                pk=prop.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)


class PropertyCreateTest(ProductViewsBaseTest):

    def test_create_property(self):
        products = model_factories.ProductFactory.create_batch(2)
        data = {
            'name': 'Test name',
            'type': 'Test type',
            'value': '55',
            'product': [item.pk for item in products]
        }
        request = self.factory.post('', data)
        request.user = self.user
        response = PropertyViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)

        prop = Property.objects.get(id=response.data['id'])
        self.assertEqual(prop.name, data['name'])
        self.assertEqual(prop.type, data['type'])
        self.assertEqual(prop.value, data['value'])
        self.assertEqual(list(prop.product.all()), products)

    def test_create_property_fail(self):
        data = {
            'name': '',  # 'name' is required
            'value': '',  # 'value' is required
        }
        request = self.factory.post('', data)
        request.user = self.user
        response = ProductViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)


class PropertyUpdateTest(ProductViewsBaseTest):

    def test_update_property(self):
        products = model_factories.ProductFactory.create_batch(2)
        prop = model_factories.PropertyFactory.create(products=products)
        data = {
            'name': prop.name,
            'type': prop.type,
            'value': 'New value',  # change "value" field
            'product': [products[0].pk]
        }
        request = self.factory.put('', data)
        request.user = self.user
        response = PropertyViewSet.as_view({'put': 'update'})(request,
                                                              pk=prop.pk)
        self.assertEqual(response.status_code, 200)

        prop_updated = Property.objects.get(id=response.data['id'])
        self.assertEqual(prop_updated.value, data['value'])
        self.assertEqual(prop_updated.name, prop.name)
        self.assertEqual(list(prop.product.all()), products[:1])

    def test_update_property_fail(self):
        prop = model_factories.PropertyFactory.create()
        data = {
            'name': '',  # "name" field is required
            'type': prop.type,
            'value': 'New value',
        }
        request = self.factory.put('', data)
        request.user = self.user
        response = PropertyViewSet.as_view({'put': 'update'})(request,
                                                              pk=prop.pk)
        self.assertEqual(response.status_code, 400)
