from fastapi import FastAPI

from slowapi.middleware import (
    SlowAPIMiddleware
)

from app.utils.rate_limiter import (
    limiter
)

from app.routes import (
    test_routes,
    url_routes,
    auth_routes
)

from app.database.db import (
    Base,
    engine
)

from app.models.url_model import (
    URL,
    User
)

app = FastAPI(
    title="URL Shortener API",
    description="A production-style URL Shortener API built with FastAPI.",
    version="1.0.0",
)

app.state.limiter = limiter

app.add_middleware(
    SlowAPIMiddleware
)

app.include_router(
    test_routes.router
)

app.include_router(
    auth_routes.router
)

app.include_router(
    url_routes.router
)

Base.metadata.create_all(
    bind=engine
)