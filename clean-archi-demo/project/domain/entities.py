from uuid import UUID
from typing import TypeVar

from pydantic import BaseModel, ConfigDict

# IdentityType = TypeVar("IdentityType", str, int, UUID)


class ProjectBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)


class User(ProjectBaseModel):
    # id: IdentityType | None = None
    username: str
    email: str


class Post(ProjectBaseModel):
    # id: IdentityType | None = None
    user: User
    title: str
    body: str
