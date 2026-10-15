from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

DbSession = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: DbSession,
):
    db_user = (
        models.User(
            name=user.name,
            email=user.email,
            hashed_password=hash_password(user.password),
        ),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
