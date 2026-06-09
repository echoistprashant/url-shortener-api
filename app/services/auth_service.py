from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.schemas import UserSignupRequest
from app.models.url_model import User
from app.utils.security import hash_password


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
