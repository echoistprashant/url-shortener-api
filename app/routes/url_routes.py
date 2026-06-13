from fastapi import (
    APIRouter,
    status,
    Depends,
    Request,
    Query
)

from fastapi.responses import (
    RedirectResponse
)

from sqlalchemy.orm import Session

from app.utils.rate_limiter import (
    limiter
)

from app.models.schemas import (
    ShortenURLRequest,
    ShortenURLResponse,
    URLStatsResponse,
    MyURLResponse,
    MyURLsPaginatedResponse
)

from app.services.shortener_service import (
    get_original_url,
    shorten_url,
    get_url_stats,
    get_my_urls
)

from app.database.db import (
    get_db
)

from app.utils.security import (
    get_current_user
)

from app.models.url_model import (
    User
)

router = APIRouter()


@router.post(
    "/shorten",
    response_model=ShortenURLResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create short URL",
    description="Create a shortened URL for the authenticated user."
)
@limiter.limit("10/minute")
def create_short_url(
    request: Request,
    shorten_request: ShortenURLRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return shorten_url(
        shorten_request,
        db,
        current_user
    )


@router.get(
    "/stats/{short_code}",
    response_model=URLStatsResponse,
    summary="Get URL statistics",
    description="Get analytics and click statistics for a short URL."
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
    response_model=MyURLsPaginatedResponse,
    summary="Get user URLs",
    description="Get paginated, searchable and sortable URLs of authenticated user."
)
def my_urls(
    page: int = Query(
        1,
        ge=1,
        description="Page number (minimum 1)"
    ),

    limit: int = Query(
        5,
        ge=1,
        le=100,
        description="Number of URLs per page (1-100)"
    ),

    search: str | None = Query(
        None,
        description="Search URLs by keyword"
    ),

    sort: str = Query(
        "desc",
        description="Sort order: asc or desc"
    ),

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


@router.get(
    "/{short_code}",
    summary="Redirect short URL",
    description="Redirect user to the original URL using short code."
)
def redirect_to_original_url(
    short_code: str,
    db: Session = Depends(get_db)
):
    original_url = get_original_url(
        short_code,
        db
    )

    return RedirectResponse(
        url=original_url
    )