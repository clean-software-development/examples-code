import os
import pytest
from moto import mock_dynamodb
from mypy_boto3_dynamodb.service_resource import Table

from project.service import ProjectService


# A laisser par sécurité pour ne pas risquer d'utiliser un profil ou des clés AWS existants.
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SECURITY_TOKEN"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


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

