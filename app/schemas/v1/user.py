from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AllUserResponse(BaseModel):
    id: UUID
    email: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class PaginatedUserResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: list[AllUserResponse]

    model_config = ConfigDict(from_attributes=True)
