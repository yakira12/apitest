from fastapi import FastAPI,Depends, HTTPException, Query

from pydantic import BaseModel

from sqlmodel import Field, Session, SQLModel, create_engine, select

from typing import Annotated

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)






class Item(BaseModel):
    id: int | None
    name :str
    price : float
    quantity: int

class Product(SQLModel, table = True):
    id: int = Field(primary_key=True)
    name: str
    price: float
    quantity: int


#create the tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#will use the session to communicate to the engine
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

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
            if product["id"] == id:
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
            if product["id"] == id:
                print("-----------the item was found------------")
                items_database.remove(product)
                print("the item was deleted")
    return {"items": items_database}


@app.get("/products/")
async def get_product(session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,) -> list[Product]:
    print("---------------In get product ------------")
    produxt = session.exec(select(Product).offset(offset).limit(limit)).all()









