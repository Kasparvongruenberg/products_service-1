import uuid

import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import boto3
from moto import mock_s3

from ..models import Product, Property


@mock_s3
@pytest.mark.django_db()
class TestProductModule:

    def test_product_with_required_fields_save(self):
        product = Product(
            workflowlevel2_uuid=uuid.uuid4,
            name='Product 1',
        )
        product.full_clean()
        product.save()

        product_saved = Product.objects.get(pk=product.pk)
        assert product == product_saved
        assert str(product) == str(product_saved)

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
        assert product == product_saved
        assert str(product) == str(product_saved)

    def test_product_with_file_save(self):
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        file_mock = SimpleUploadedFile('test1.pdf', b'some content')
        product = Product(
            workflowlevel2_uuid=uuid.uuid4,
            name='Product 1',
            file=file_mock,
            file_name='foo.pdf',
        )
        product.full_clean()
        product.save()

        product_saved = Product.objects.get(pk=product.pk)
        assert product == product_saved
        assert str(product) == str(product_saved)
        assert product.file
        assert product.file_name == 'foo.pdf'

    def test_product_validation_failed(self):
        product = Product(
            workflowlevel2_uuid=uuid.uuid4
        )
        with pytest.raises(ValidationError):
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

        property_saved = Property.objects.get(pk=property1.pk)
        assert property1 == property_saved
        assert str(property1) == str(property_saved)

        properties = Product.objects.get(pk=product.pk).property_set.all()
        assert property1 in properties
        assert property2 in properties
