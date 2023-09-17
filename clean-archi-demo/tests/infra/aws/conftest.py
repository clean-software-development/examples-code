import os
import pytest
from moto import mock_dynamodb
from mypy_boto3_dynamodb.service_resource import Table

from project.infra.aws.repository import RepositoryDynamoDB

os.environ["PROJECT_IS_CREATE_TABLE"] = "false"


@pytest.fixture
def user_table_name() -> str:
    return "test-users"


@pytest.fixture
def repository(user_table_name) -> RepositoryDynamoDB:    
    os.environ["PROJECT_AWS_USER_TABLE_NAME"] = user_table_name
    
    with mock_dynamodb():
        repository = RepositoryDynamoDB()
        assert repository._user_table_name == user_table_name
        repository._create_table()
        yield repository

