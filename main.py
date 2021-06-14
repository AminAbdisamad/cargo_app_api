from fastapi import FastAPI,APIRouter, Depends, HTTPException

from cargo_item import  cargo

app = FastAPI()

app.include_router(cargo)

@app.get("/")
def index():
    return "welcome to fastapi"