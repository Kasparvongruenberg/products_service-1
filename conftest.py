import pytest
from rest_framework.test import APIRequestFactory


@pytest.fixture(scope='session')
def api_rf():
    return APIRequestFactory()
