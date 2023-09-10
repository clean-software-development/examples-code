
from pydantic import BaseModel, ConfigDict


class ProjectBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)


class User(ProjectBaseModel):
    user_id: str | None = None
    username: str


class Post(ProjectBaseModel):
    post_id: str
    user: User
    title: str
    body: str


