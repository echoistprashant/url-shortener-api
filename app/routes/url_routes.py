from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse

from app.models.schemas import ShortenURLRequest, ShortenURLResponse, URLStatsResponse, MyURLResponse,MyURLsPaginatedResponse   
from app.services.shortener_service import get_original_url, shorten_url, get_url_stats, get_my_urls

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.utils.security import (
    get_current_user
)
from app.models.url_model import (
    User
)


router = APIRouter()


@router.post("/shorten",response_model=ShortenURLResponse, status_code=status.HTTP_201_CREATED)
def create_short_url(
    request: ShortenURLRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user)
):
    return shorten_url(request, db, current_user)

@router.get(
    "/stats/{short_code}",
    response_model=URLStatsResponse
)
def url_stats(
    short_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_url_stats(
        short_code,
        db,
        current_user
    )
@router.get(
    "/my-urls",
    response_model=MyURLsPaginatedResponse
)
def my_urls(
    page: int = 1,
    limit: int = 5,
    search: str | None = None,
    sort: str = "desc",
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_my_urls(
    current_user,
    db,
    page,
    limit,
    search,
    sort
)


@router.get("/{short_code}")
def redirect_to_original_url(
    short_code: str,
    db: Session = Depends(get_db)
):
    original_url = get_original_url(short_code, db)
    return RedirectResponse(url=original_url)

