from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.schemas import (
    UserSignupRequest,
    UserResponse,
    UserLoginRequest,
    MeResponse
)
from app.services.auth_service import (
    signup_user,
    login_user
)
from app.utils.security import (
    get_current_user
)
from app.models.url_model import (
    User
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

@router.get(
    "/me",
    response_model=MeResponse
)
def get_me(
    current_user: User = Depends(
        get_current_user
    )
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }