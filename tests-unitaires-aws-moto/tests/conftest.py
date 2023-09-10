import os
import pytest
from moto import mock_dynamodb
from mypy_boto3_dynamodb.service_resource import Table

from project.service import ProjectService


@pytest.fixture
def user_table_name() -> str:
    return "test-users"


@pytest.fixture
def user_table_fixture(user_table_name) -> Table:
    os.environ["PROJECT_USER_TABLE_NAME"] = user_table_name
    with mock_dynamodb():
        service = ProjectService()
        service.create_table()
        yield service.user_table

