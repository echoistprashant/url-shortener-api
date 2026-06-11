from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.schemas import ShortenURLRequest
from app.models.url_model import URL, User
from app.utils.generator import generate_short_code
from datetime import datetime, timedelta


def shorten_url(
    request: ShortenURLRequest,
    db: Session,
    current_user: User
):
    if request.custom_alias:

        existing_alias = db.query(URL).filter(
            URL.short_code == request.custom_alias
        ).first()

        if existing_alias:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Custom alias already exists",
            )

        short_code = request.custom_alias

    else:
        short_code = generate_short_code()
    
    expires_at = None

    if request.expires_in_days:
         expires_at = datetime.now() + timedelta(
            days=request.expires_in_days

         )
    
    new_url = URL(
        original_url=str(request.url),
        short_code=short_code,
        expires_at=expires_at,
        user_id=current_user.id
    )

    db.add(new_url)
    db.commit()

    return {
        "original_url": str(request.url),
        "short_url": f"http://localhost:8000/{short_code}",
        
    }


def get_original_url(
    short_code: str,
    db: Session
):
    url_entry = db.query(URL).filter(
        URL.short_code == short_code
    ).first()

    if not url_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found",
        )

    if (
        url_entry.expires_at
        and url_entry.expires_at < datetime.now()
    ):
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Short URL has expired",
        )

    url_entry.clicks += 1
    db.commit()

    return url_entry.original_url

def get_url_stats(
    short_code: str,
    db: Session,
    current_user: User

):
    url_entry = db.query(URL).filter(
        URL.short_code == short_code
    ).first()

    if url_entry.user_id != current_user.id:
        raise HTTPException(
           status_code=status.HTTP_403_FORBIDDEN,
           detail="Not authorized"
    )

    is_expired = False

    if (
        url_entry.expires_at
        and url_entry.expires_at < datetime.now()
    ):
        is_expired = True

    return {
        "original_url": url_entry.original_url,
        "short_code": url_entry.short_code,
        "clicks": url_entry.clicks,
        "expires_at": url_entry.expires_at,
        "is_expired": is_expired
    }


def get_my_urls(
    current_user: User,
    db: Session
):
    urls = db.query(URL).filter(
        URL.user_id == current_user.id
    ).all()

    return urls