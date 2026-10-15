from pydantic import BaseModel, ConfigDict, EmailStr, Field


# --- Post Schemas ---
class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# --- User Schemas ---


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserResponse(UserBase):
    id: int
    # Including posts in the user response automatically serializes the relationship!
    posts: list[PostResponse] = []

    model_config = ConfigDict(from_attributes=True)
