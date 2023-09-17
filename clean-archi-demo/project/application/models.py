from pydantic import BaseModel

from project.domain.entities import IdentityType


class AddUserResponse(BaseModel):
    id: IdentityType