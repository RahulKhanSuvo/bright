import uuid
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import User

DbSession = Annotated[Session, Depends(get_db)]


# 1. Strict dependency for Private Routes (throws 401 if not logged in)
def get_current_user(request: Request, db: DbSession) -> User:
    token_cookie = request.cookies.get("access_token")
    if not token_cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    try:
        scheme, token = token_cookie.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")

        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_id_str: str = str(user_id)
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    user = db.query(User).filter(User.id == uuid.UUID(user_id_str)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
