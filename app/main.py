print("welcome to url shortener")

from fastapi import FastAPI

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

@app.get("/health")
def health():
    return {
        "status" : "Healthy"
    }