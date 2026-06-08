from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.schemas import ShortenURLRequest
from app.models.url_model import URL
from app.utils.generator import generate_short_code
from datetime import datetime, timedelta


def shorten_url(
    request: ShortenURLRequest,
    db: Session
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
        expires_at=expires_at
    )

    db.add(new_url)
    db.commit()

    return {
        "original_url": request.url,
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
    db: Session
):
    url_entry = db.query(URL).filter(
        URL.short_code == short_code
    ).first()

    if url_entry:
        return {
            "original_url": url_entry.original_url,
            "short_code": url_entry.short_code,
            "clicks": url_entry.clicks
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Short URL not found",
    )