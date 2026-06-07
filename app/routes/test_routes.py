from fastapi import APIRouter, status

from app.models.schemas import User


router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "welcome to url shortener",
    }


@router.get("/about")
def about():
    return {
        "project": "URL Shortener API",
        "developer": "Prashant",
        "status": "Learning FastAPI",
    }


@router.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {
        "status": "Healthy",
    }


@router.get("/hello/{name}")
def hello(name: str):
    return {
        "message": f"hello {name}",
    }


@router.get("/square/{number}")
def square(number: int):
    result = number * number
    return {
        "number": number,
        "square": result,
    }


@router.get("/greet")
def greet(name: str = "Guest"):
    return {
        "message": f"Hello, {name}!",
    }


@router.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    return {
        "message": f"User '{user.name}' created successfully",
    }

