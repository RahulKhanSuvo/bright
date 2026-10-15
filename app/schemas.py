from pydantic import BaseModel, ConfigDict


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
    email: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    # Including posts in the user response automatically serializes the relationship!
    posts: list[PostResponse] = []

    model_config = ConfigDict(from_attributes=True)
