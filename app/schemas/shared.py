from pydantic import BaseModel


# --- Post Schemas ---
class PostBase(BaseModel):
    title: str
    content: str
