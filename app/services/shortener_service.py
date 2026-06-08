from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.schemas import ShortenURLRequest
from app.models.url_model import URL
from app.utils.generator import generate_short_code


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

    new_url = URL(
        original_url=str(request.url),
        short_code=short_code
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

    if url_entry:
        return url_entry.original_url

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Short URL not found",
    )