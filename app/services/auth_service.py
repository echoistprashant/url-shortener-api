from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.schemas import UserSignupRequest
from app.models.url_model import User
from app.utils.security import hash_password
from app.models.schemas import (UserLoginRequest)

from app.utils.security import (
    verify_password,
    create_access_token
)


def signup_user(request: UserSignupRequest, db: Session):
    existing_user = db.query(User).filter(
        User.email == request.email
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail =  "User with this email already exists"
        
        )
    hashed_password = hash_password(request.password)

    new_user = User(
        username = request.username,
        email = request.email,
        hashed_password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }    



def login_user(
    request: UserLoginRequest,
    db: Session
):
    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    is_password_correct = verify_password(
        request.password,
        user.hashed_password
    )

    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "user_id": user.id
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }