import pytest

from project.domain.entities import User
from project.domain.service import Service
from project.infra.memory.repository import RepositoryMemory
from project.domain.exceptions import ConflictError, NotFoundError


def test_service_add_user():
    repository = RepositoryMemory()
    service = Service(repository=repository)

    new_user = User(username="user1", email="user1@example.net")
    response = service.add_user(user=new_user)
    assert response is None
    assert "user1" in repository._users

    new_user = User(username="user2", email="user2@example.net")
    service.add_user(user=new_user)
    assert "user2" in repository._users

    assert len(repository._users) == 2

    with pytest.raises(ConflictError) as exc:
        service.add_user(user=User(username="user2", email="user2@example.net"))
    assert str(exc.value) == "this user [user2] already exists"


def test_service_get_user_by_username():
    user1 = User(username="user1", email="user1@example.net")
    users = {
        "user1": user1.model_dump(),
    }
    repository = RepositoryMemory(users=users)
    service = Service(repository=repository)

    search_user = service.get_user_by_username(username="user1")
    assert search_user == user1

    with pytest.raises(NotFoundError) as exc:
        service.get_user_by_username(username="not-existing-user")
    assert str(exc.value) == "user [not-existing-user] not found"


def test_service_get_users():
    user1 = User(username="user1", email="user1@example.net")
    users = {
        "user1": user1.model_dump(),
    }
    repository = RepositoryMemory(users=users)
    service = Service(repository=repository)

    users = service.get_users()
    assert len(users) == 1
    assert users[0] == user1
