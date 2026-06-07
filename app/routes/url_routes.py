from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse

from app.models.schemas import ShortenURLRequest
from app.services.shortener_service import get_original_url, shorten_url


router = APIRouter()


@router.post("/shorten", status_code=status.HTTP_201_CREATED)
def create_short_url(request: ShortenURLRequest):
    return shorten_url(request)


@router.get("/{short_code}")
def redirect_to_original_url(short_code: str):
    original_url = get_original_url(short_code)
    return RedirectResponse(url=original_url)

