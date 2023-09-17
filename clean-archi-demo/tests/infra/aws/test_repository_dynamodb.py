from project.infra.aws.repository import RepositoryDynamoDB


def test_repository_dynamodb_add_user(repository: RepositoryDynamoDB):

    repository.add_user(username="user1", email="user1@example.net")

    response = repository._user_table.get_item(Key={"username": "user1"})
    assert response.get("Item") == {
        "username": "user1",
        "email": "user1@example.net"
    }

    # update/replace
    repository.add_user(username="user1", email="user1@test.net")

    response = repository._user_table.get_item(Key={"username": "user1"})
    assert response.get("Item") == {
        "username": "user1",
        "email": "user1@test.net"
    }
