from pydantic import BaseModel, HttpUrl
from datetime import datetime


class User(BaseModel):
    name: str


class ShortenURLRequest(BaseModel):
    url: HttpUrl
    custom_alias: str | None = None
    expires_in_days: int | None = None


class ShortenURLResponse(BaseModel):
    original_url: str
    short_url: str


class URLStatsResponse(BaseModel):
    original_url: str
    short_code: str
    clicks: int
    expires_at: datetime | None = None
    is_expired: bool

class UserSignupRequest(BaseModel):
     username: str 
     email: str
     password: str

class UserResponse(BaseModel):
    id: int 
    username: str
    email: str

class UserLoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
   
class MyURLResponse(BaseModel):
    original_url: str
    short_code: str
    clicks: int
    expires_at: datetime | None = None
     
class MeResponse(BaseModel):
    id: int
    username: str
    email: str