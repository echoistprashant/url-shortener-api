
from fastapi import FastAPI

from app.routes import test_routes, url_routes

app = FastAPI(
    title="URL Shortener API",
    description="A production-style URL Shortener API built with FastAPI.",
    version="1.0.0",
)

app.include_router(test_routes.router)
app.include_router(url_routes.router)
