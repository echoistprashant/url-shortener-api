from pydantic import BaseModel, HttpUrl


class User(BaseModel):
    name: str


class ShortenURLRequest(BaseModel):
    url: HttpUrl
    custom_alias: str | None = None

