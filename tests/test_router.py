import pydantic
import pytest
from app.schemas import TodoItem, User, UserPayload
from fastapi import FastAPI
from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

from . import factories


@pytest.fixture()
def fastapi_app():
    from app.router import router

    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture()
def client(fastapi_app: FastAPI):
    with TestClient(fastapi_app) as client:
        return client


@pytest.fixture()
def valid_credentials(client: TestClient):
    payload: UserPayload = factories.UserFactory()
    response = client.post(
        url="/users/",
        json=payload.dict(
            by_alias=True,
            exclude_unset=True,
        ),
    )
    assert response.status_code == 201
    return HTTPBasicAuth(payload.username, payload.password)


@pytest.fixture()
def invalid_credentials():
    payload = factories.UserFactory()
    return HTTPBasicAuth(payload.username, payload.password)


def existing_item(client: TestClient, valid_credentials: HTTPBasicAuth):
    response = client.post(
        url="/items/",
        json=factories.ItemFactory().dict(by_alias=True, exclude_unset=True),
    )
    return pydantic.parse_obj_as(TodoItem, response.json())


class TestAuthentication:
    def test_creates_user(self, client: TestClient):
        payload: UserPayload = factories.UserFactory()
        response = client.post(
            url="/users/",
            json=payload.dict(
                by_alias=True,
                exclude_unset=True,
            ),
        )
        assert response.status_code == 201
        user = pydantic.parse_obj_as(User, response.json())
        assert user.username == payload.username

    def test_returns_valid_user(
        self,
        client: TestClient,
        valid_credentials: HTTPBasicAuth,
    ):
        response = client.get("/users/me", auth=valid_credentials)
        assert response.status_code == 200
        user = pydantic.parse_obj_as(User, response.json())
        assert user.username == valid_credentials.username

    def test_returns_401_without_credentials(self, client: TestClient):
        response = client.get("/users/me")
        assert response.status_code == 401

    def test_returns_401_with_invalid_credentials(
        self, client: TestClient, invalid_credentials: HTTPBasicAuth
    ):
        response = client.get("/users/me", auth=invalid_credentials)
        assert response.status_code == 401


class TestItemCrud:
    def test_returns_401(self, client: TestClient):
        response = client.post(
            url="/items/",
            json=factories.ItemFactory().dict(
                by_alias=True,
                exclude_unset=True,
            ),
        )
        assert response.status_code == 401

    def test_returns_newly_created_item(
        self,
        client: TestClient,
        valid_credentials: HTTPBasicAuth,
    ):
        payload = factories.ItemFactory()
        response = client.post(
            url="/items/",
            json=payload.dict(
                by_alias=True,
                exclude_unset=True,
            ),
            auth=valid_credentials,
        )
        assert response.status_code == 201
        todo = pydantic.parse_obj_as(TodoItem, response.json())
        assert todo.id is not None
        assert not todo.completed
        assert todo.username == valid_credentials.username

    def test_returns_the_item(
        self, client: TestClient, existing_item: TodoItem
    ):
        response = client.get(f"/items/{existing_item.id}")
        assert response.status_code == 200
        response_item = pydantic.parse_obj_as(TodoItem, response.json())
        assert response_item == existing_item

    # TODO: Add missing tests
