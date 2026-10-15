from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import CurrentUser
from app.models import User
from app.schemas import LoginRequest, UserCreate, UserResponse
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])
DbSession = Annotated[Session, Depends(get_db)]
FormData = Annotated[OAuth2PasswordRequestForm, Depends()]


# 1. SIGNUP / REGISTER
@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def signup(user_data: UserCreate, db: DbSession):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new user with hashed password
    db_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# 2. LOGIN (Sets HttpOnly Cookie)
@router.post("/login")
def login(form_data: LoginRequest, response: Response, db: DbSession):
    user = db.query(User).filter(User.email == form_data.email).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    # Set secure HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,  # Blocks JavaScript from reading the cookie (protects against XSS)
        secure=False,  # Change to True in production once you have HTTPS enabled
        samesite="lax",  # Protects against CSRF attacks
        max_age=1800,  # Cookie expires in 30 minutes
    )
    return {"message": "Login successful"}


@router.get("/me", response_model=UserResponse)
def get_logged_in_user(current_user: CurrentUser):
    # If the request doesn't have a valid cookie, get_current_user blocks it automatically 401
    return current_user


@router.post("/logout")
def logout(response: Response):
    # Instructs the browser to delete the cookie immediately
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,  # Match whatever settings you used in login
        samesite="lax",
    )
    return {"message": "Logged out successfully"}
