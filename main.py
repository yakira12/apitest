from fastapi import FastAPI

from pydantic import BaseModel

class Item(BaseModel):
    name :str
    price : float
    quantity: int


app = FastAPI()

items_database = []


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
