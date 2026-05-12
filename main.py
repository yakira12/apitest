from fastapi import FastAPI

from pydantic import BaseModel

class Item(BaseModel):
    id: int | None
    name :str
    price : float
    quantity: int


app = FastAPI()

items_database = [{"id": 1 , "name": "Nike", "price": 1.99, "quantity": 2 }]


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

@app.post("/items/add/")
async def add_item(item: Item):
    print("---------------In add item ------------")
    if item is not None:
        print(f"-----------the item id is {item.id}---------- ")
        print(f"the item name is {item.name}")
        print(f"the item price is {item.price}")
        print(f"the item quantity is {item.quantity}")
        print("----------adding the item to the database-------------")
        items_database.append(item.model_dump())
    return {"items": items_database}

@app.put("/items/update/{id}/")
async def update_item(id: int, item: Item):
    print("---------------In update item ------------")
    if item is not None:
        print(f"The item id is {item.id}")
        print(f"the item name is {item.name}")
        print(f"the item price is {item.price}")
        print(f"the item quantity is {item.quantity}")
        for product in items_database:
            if product["id"] == item.id:
                print("-----------the item was found------------")
                product["price"] = item.price
                product["quantity"] = item.quantity
                product["name"] = item.name
                print("the item was updated")
    return {"items": items_database}


@app.delete("/items/delete/{id}/")
async def delete_item(item: Item, id: int):
    print("---------------In delete item ------------")
    if item is not None:
        print(f"the item id is {item.id}")
        print(f"the item name is {item.name}")
        print(f"the item price is {item.price}")
        print(f"the item quantity is {item.quantity}")
        for product in items_database:
            if product["id"] == item.id:
                print("-----------the item was found------------")
                items_database.remove(product)
                print("the item was deleted")
    return {"items": items_database}



