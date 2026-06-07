

from fastapi import FastAPI , status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import random
import string

url_database = {}

def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for _ in range(6))
    return short_code

class User(BaseModel):
    name : str

class ShortenURLRequest(BaseModel):
    url: HttpUrl

app = FastAPI(
    title="URL Shortener API",
    description="A production-style URL Shortener API built with FastAPI.",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message" :"welcome to url shortener"
    }

@app.get("/about")
def about():
    return {
        
       "project": "URL Shortener API",
       "developer": "Prashant",
       "status": "Learning FastAPI"

    }

@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return{
        "status" : "Healthy"
    }

@app.get("/hello/{name}")
def hello(name: str):
    return{
        "message" : f"hello {name}"
    }

@app.get("/square/{number}")
def square(number: int):
    result = number * number
    return{
        "number" : number,
        "square" : result
  }

@app.get("/greet")
def greet(name: str = "Guest"):
    return {
        "message": f"Hello, {name}!"
    }


@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    return {
        "message": f"User '{user.name}' created successfully"
    }

@app.post("/shorten", status_code=status.HTTP_201_CREATED)
def shorten_url(request: ShortenURLRequest):
    short_code = generate_short_code()
    url_database[short_code] = request.url
    return {
         "original_url": request.url,
         "short_url": f"http://localhost:8000/{short_code}"
    
    }

@app.get("/{short_code}")
def redirect_to_original_url(short_code: str):
    original_url = url_database.get(short_code)
    if original_url:
        return RedirectResponse(url=original_url)
    else:
        return {"error": "Short URL not found"}