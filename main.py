from fastapi import FastAPI

from pydantic import BaseModel

class Item(BaseModel):
    name :str
    price : float
    quantity: int


app = FastAPI()

items_database = [{"name": "Nike", "price": 1.99, "quantity": 2 }]


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}



@app.get("/items/")
async def get_items():
    print("---------------In get items -----------")
    return {"items": items_database}

