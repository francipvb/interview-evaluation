from typing import List

from fastapi import APIRouter, Response

from .schemas import TodoItem, TodoPayload, User, UserPayload

router = APIRouter()


@router.get("/items/", response_model=List[TodoItem])
def get_items():
    """Retrieve a persistent list of items."""
    # TODO: Implement this
    pass


@router.get("/items/{id}", response_model=TodoItem)
def get_item(id: int):
    """Retrieve a particular item from the store."""
    # TODO: Implement this.
    pass


@router.post(
    path="/items/",
    response_model=TodoItem,
    status_code=201,
    response_description="The item has been created successfully.",
)
def create_item(
    payload: TodoPayload,
):
    """Add an item to the store."""

    # TODO: Implement this.
    # Requirements:
    # * Ensure an user is authenticated with basic credentials.
    # * Add the username to the item.
    pass


@router.put("/items/{id}", response_model=TodoItem)
def update_item(
    id: int,
    payload: TodoPayload,
):
    # TODO: Implement this.
    # * Ensure the user is authenticated. If not, either return a 401 response
    #   or raise an `HttpException` with a 401 code.
    # * Ensure that the item is stored already in the datastore. If not, raise
    #   an `HttpException` with a 404 code or return a 404 response.
    # * Check the username matches the item's username. If not, return a 403
    #   response or raise a `HttpException` with a 403 code.
    # * Apply the update and save it to the database.
    pass


@router.delete("/items/{id}", response_class=Response, status_code=204)
def remove_item(
    id: int,
):
    # TODO: Implement this
    # 1. Check that the item exists in the datastore.
    # 2. Ensure the user is authenticated.
    # 3. Check if the currently logged username matches.
    # 4. Remove the item from the store.
    pass


@router.post("/users/")
def create_user(payload: UserPayload):
    # TODO: Implement this.
    # 1. Validate the username has no uppercase letter, @ sign, nor
    #   punctuations.
    # 2. Hash the password and store the user in the data store.
    pass


# TODO: Document this endpoint
@router.get("/users/me")
def get_current_user():
    # TODO: Implement this.
    # 1. Get the credentials from the request.
    # 2. Retrieve the user by it's username from the store.
    # 3. Validate the password.
    # 4. Return the user without the password hash.
    pass
