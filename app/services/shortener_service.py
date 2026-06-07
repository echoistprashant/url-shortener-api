from fastapi import HTTPException, status

from app.database.storage import url_database
from app.models.schemas import ShortenURLRequest
from app.utils.generator import generate_short_code


def shorten_url(request: ShortenURLRequest):
    if request.custom_alias:
        if request.custom_alias in url_database:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Custom alias already exists",
            )

        short_code = request.custom_alias
    else:
        short_code = generate_short_code()

    url_database[short_code] = request.url

    return {
        "original_url": request.url,
        "short_url": f"http://localhost:8000/{short_code}",
    }


def get_original_url(short_code: str):
    original_url = url_database.get(short_code)
    if original_url:
        return original_url

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Short URL not found",
    )

