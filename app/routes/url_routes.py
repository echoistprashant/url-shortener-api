from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse

from app.models.schemas import ShortenURLRequest
from app.services.shortener_service import get_original_url, shorten_url, get_url_stats

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.db import get_db


router = APIRouter()


@router.post("/shorten", status_code=status.HTTP_201_CREATED)
def create_short_url(
    request: ShortenURLRequest,
    db: Session = Depends(get_db)
):
    return shorten_url(request, db)

@router.get("/stats/{short_code}")
def url_stats(
    short_code: str,
    db: Session = Depends(get_db)
):
    return get_url_stats(short_code, db)


@router.get("/{short_code}")
def redirect_to_original_url(
    short_code: str,
    db: Session = Depends(get_db)
):
    original_url = get_original_url(short_code, db)
    return RedirectResponse(url=original_url)

