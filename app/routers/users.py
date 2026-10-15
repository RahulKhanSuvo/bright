from fastapi import APIRouter

from app import schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post("/", response_model=schemas.UserResponse)
def create_user(
user:
)
