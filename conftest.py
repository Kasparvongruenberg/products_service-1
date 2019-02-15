import pytest
from rest_framework.test import APIRequestFactory
from django.conf import settings
import boto3
from moto import mock_s3


@pytest.fixture(scope='session')
def api_rf():
    return APIRequestFactory()


@pytest.fixture(scope='session')
@mock_s3
def s3_conn():
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
