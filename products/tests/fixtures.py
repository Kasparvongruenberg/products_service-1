import uuid

import pytest
import boto3
from moto import mock_s3
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from . import model_factories

TEST_TYPE = 'test type'
TEST_WF2 = str(uuid.uuid4())


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


@pytest.fixture
@mock_s3
def product_with_file():
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    return model_factories.ProductFactory.create(
        file=SimpleUploadedFile('foo.pdf', b'some content'),
        file_name='bar.pdf',
    )
