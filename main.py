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
    product : list[Product] = session.exec(select(Product).offset(offset).limit(limit)).all()
    return product

@app.post("/products/add/")
async def add_product(product :Product, session : SessionDep) -> Product:
    print("_____________In add product ------------------")
    if product is not None:
        print(f"The product name is {product.name}")
        print(f"the poduct price is {product.price}")
        print (f"The product quantity is {product.quantity}")
        session.add(product)
        session.commit()
        #session.refresh(Product)
        return {"product": product.model_dump()}

@app.get("/products/get/{id}/")
async def get_product_by_id(session: SessionDep, id : int ) -> Product:
    print("--------------In get product by Id-----------")
    product : Product = session.get(Product, id)
    #product : Product = session.exec(select(Product).where(Product.id == id)).one()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/name/{name}/")
async def get_product_by_name(session: SessionDep, name : str) -> Product:
    print("-------------In get product by name ----------")
    product: Product = session.exec(select(Product).where(Product.name == name)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/update/")
async def update_product(product : Product, session : SessionDep) -> Product:
    print("-------------In update product------------------")
    if product is not None:
        print(f"The product name is {product.name}")
        print (f"the product price is {product.price}")
        print(f"the product quantity is {product.quantity}")
        cur_product = session.exec(select(Product).where(Product.name == product.name)).first()
        #if the product is not found then insert the new product
        if not cur_product:
            print("----------The product was found. adding it to the database-------------")
            session.add(product)
            session.commit()
            return {"product": product.model_dump()}
        #otherwise update the existing product
        print("----------The product was found. updating it -----------------------------")
        cur_product.name = product.name
        cur_product.price = product.price
        cur_product.quantity = product.quantity
        session.add(cur_product)
        session.commit()
        return {"product": product.model_dump()}

@app.delete("/products/delete/{id}/")
async def delete_product_by_id(id: int, session : SessionDep) -> Product:
    print("-------------In delete product by id --------------")
    product : Product = session.exec(select(Product).where(Product.id == id)).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()

    return {"product": product.model_dump()}















