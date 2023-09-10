from mypy_boto3_dynamodb.service_resource import Table
import pytest

from project.models import User
from project.service import ProjectService


def test_service_add_user_success(user_table_fixture: Table):
    service = ProjectService()
    new_user = User(user_id="test", username="testing")

    user_id = service.add_user(user=new_user)
    assert user_id == new_user.user_id

    new_user_without_id = User(username="new-testing")
    user_id = service.add_user(user=new_user_without_id)
    assert user_id is not None

    response = user_table_fixture.scan()
    users = response["Items"]
    assert len(users) == 2


def test_service_get_user_by_id_success(user_table_fixture: Table):
    service = ProjectService()
    
    user_table_fixture.put_item(Item={
        "user_id": "test",
        "username": "testing"
    })

    user = service.get_user_by_id(user_id="test")
    assert user.username == "testing"

    with pytest.raises(Exception) as exc:
        service.get_user_by_id(user_id="ABC")
    assert str(exc.value) == f"User not found for id: ABC"