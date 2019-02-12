import uuid

import pytest

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
