from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.schemas import (
    UserSignupRequest,
    UserResponse,
    UserLoginRequest
)
from app.services.auth_service import (
    signup_user,
    login_user
)

router = APIRouter()


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def signup(
    request: UserSignupRequest,
    db: Session = Depends(get_db)
):
    return signup_user(
        request,
        db
    )
@router.post("/login")
def login(
    request: UserLoginRequest,
    db: Session = Depends(get_db)
):
    return login_user(
        request,
        db
    )