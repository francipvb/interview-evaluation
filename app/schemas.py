from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class BaseTodo(BaseModel):
    title: str = Field(..., description="A title for the task.")
    body: Optional[str] = Field(
        None,
        description="A detailed description of the task.",
    )


class TodoPayload(BaseTodo):
    """Data for the item being created."""


class TodoItem(BaseTodo):
    """A task to do."""

    id: int = Field(..., description="The item unique ID.")
    completed: bool = Field(
        ..., description="Indicates if this task has been completed."
    )
    username: Optional[str] = Field(
        ...,
        description="The user who created this item.",
    )


class BaseUser(BaseModel):
    name: str
    email: EmailStr
    username: str


class UserPayload(BaseUser):
    password: str


class User(BaseUser):
    pass


class StoredUser(BaseUser):
    password_hash: str
