import uuid

from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Product, Property


class ProductTest(TestCase):

    def test_product_with_required_fields_save(self):
        product = Product(
            workflowlevel2_uuid=uuid.uuid4,
            name='Product 1',
        )
        product.full_clean()
        product.save()

        product_saved = Product.objects.get(pk=product.pk)
        self.assertEqual(product, product_saved)
        self.assertEqual(str(product), str(product_saved))

    def test_product_with_all_fields_save(self):
        product = Product(
            workflowlevel2_uuid=uuid.uuid4,
            name='Product 1',
            make='Producer 1',
            model='Model 1',
            style='Blue',
            description='Foo bar foo bar',
            type='type',
            status='in-stock',
            reference_id='UYT1'
        )
        product.full_clean()
        product.save()

        product_saved = Product.objects.get(pk=product.pk)
        self.assertEqual(product, product_saved)
        self.assertEqual(str(product), str(product_saved))

    def test_product_validation_failed(self):
        product = Product(
            workflowlevel2_uuid=uuid.uuid4
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_product_properties_creation(self):
        product = Product(
            workflowlevel2_uuid=uuid.uuid4,
            name='Product 1',
        )
        product.save()
        property1 = Property.objects.create(name='Color', value='blue')
        property2 = Property.objects.create(name='Size', value='L')
        product.property_set.add(property1, property2)

        property_saved = Property.objects.get(pk=product.pk)
        self.assertEqual(property1, property_saved)
        self.assertEqual(str(property1), str(property_saved))

        properties = Product.objects.get(pk=product.pk).property_set.all()
        self.assertIn(property1, properties)
        self.assertIn(property2, properties)
