from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserResponse(UserBase):
    id: UUID
    # Including posts in the user response automatically serializes the relationship!
    # posts: list[PostResponse] = []

    model_config = ConfigDict(from_attributes=True)
