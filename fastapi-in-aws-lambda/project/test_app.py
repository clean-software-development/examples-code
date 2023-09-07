import pytest
from fastapi import status as http_status
from fastapi.testclient import TestClient


from app import app, ItemModel, ITEMS


@pytest.fixture
def fake_items() -> list[ItemModel]:
    return [ItemModel(pk=str(i), name=f"test-{i}", data={"key": f"value-{i}"}) for i in range(1, 10)]


@pytest.fixture
def test_app():
    client = TestClient(app)
    yield client


def test_add_item(test_app: TestClient):

    item = ItemModel(pk="1234", name="test", data={"key": "value"}).model_dump()
    response = test_app.post(
        f"/item",
        json=item
    )
    assert response.status_code == http_status.HTTP_200_OK    
    assert response.json() == {"message": "ok"}

    ITEMS.clear()


def test_get_items(test_app: TestClient, fake_items: list[ItemModel]):
    ITEMS.update(fake_items)

    response = test_app.get(
        f"/item"
    )

    assert response.status_code == http_status.HTTP_200_OK

    fake_items_dicts = [item.model_dump() for item in fake_items]
    assert sorted(response.json(), key=lambda x: x['pk']) == sorted(fake_items_dicts, key=lambda x: x['pk'])
