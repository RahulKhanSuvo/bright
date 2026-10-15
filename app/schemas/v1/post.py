from pydantic import ConfigDict

from app.schemas.shared import PostBase


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
