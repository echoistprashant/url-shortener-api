print("welcome to url shortener")

from fastapi import FastAPI , status


app = FastAPI()

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
        "status " : "Healthy"
    }

@app.get("/hello/{name}")
def hello(name: str):
    return{
        "messsage" : f"hello {name}"
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
