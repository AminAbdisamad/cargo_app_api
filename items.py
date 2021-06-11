from enum import Enum
from datetime import datetime, timedelta
from typing import Optional,Set,Union
from fastapi import FastAPI,Query,Path,Body,Header,Cookie,status,Form
from pydantic import BaseModel,Field,HttpUrl,EmailStr


app = FastAPI()

class Workshop(BaseModel):
    name:str
    start_date:Optional[datetime] = None
    end_date:Optional[datetime] = None
    process_after: Optional[timedelta] = None
    repeat_at: Optional[datetime] = None


class Image(BaseModel):
    name:str
    url:HttpUrl

# ? Base Item Structure
class Item(BaseModel):
    name:str
    description:Optional[str] = Field(
        None, title="Description of the item",max_length=100,example="A very nice Item"
    )
    price:float = Field(gt=0,description="Price should be greater than zero",example="34.8")
    tax: Optional[float] = None
    # unique tags
    tags: Set[str] = set()
    image:Optional[list[Image]] = None

class Offer(BaseModel):
    name:str
    description:Optional[str] = None
    price:Optional[float] = None
    items:Item

class BaseItem(BaseModel):
    description:str
    type:str

class CarItem(BaseItem):
    type="car"

class PlaneItem(BaseItem):
    type="plain"
    size:int

itemz = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

# i = Union[int, str, float]
@app.get("/items/{item_id}")
def read_root(user_agent:Optional[str] = Header(None),cookie:Optional[str] = Cookie(None)):
    return {"Hello": "World","user_agent":user_agent,"cookie":cookie}

@app.post("/workshop/",status_code=status.HTTP_201_CREATED)
def workshop(workshop_id:int,workshop:Workshop):
    data = {"workshop_id":workshop_id,"workshop":workshop}
    return data

@app.post("/offer/")
def offer(offer:Offer):
    return offer

# ? Query validations
@app.get("/items",status_code=status.HTTP_200_OK)
async def items(q:Optional[str] = Query(None,min_length=2, max_length=20,regex="^fixedquery$",title="Query string",
        description="Query string for the items to search in the database that have a good match",deprecated=True)):
    # Even though q is optional if you try 
    # use it max length should be 10 
    items = {"item_id":"bar"}
    if q:
        items.update({"q":q})
    return items


@app.get("/items/{item_id}")
def read_item(item_id:int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


fake_items:list[dict] = [{"item_name":"foo"},{"item_name":"bar"},{"item_name":"baz"}]

@app.get("/get/items")
def get_items(skip:int =0, limit:int=10):
    return fake_items[skip:skip+limit]

# ? Query parameter list / multiple values
@app.get("/it/")
async def read_items(q: Optional[list[str]] = Query(None)):
    query_items = {"q": q}
    return query_items

# ? Query parameter list / multiple values with defaults
@app.get("/it/")
async def read_it(q: list[str] = Query(["foo", "bar"])):
    query_items = {"q": q}
    return query_items


#? Post Method
@app.post("/item")
def save_items(item:Item):
    items = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        items.update({"total_price":price_with_tax})
    return items

# ? Put Method 
@app.put("/items/{item_id}")
def update_item(item_id:int = Path(...,title="ID of the item",ge=0,le=100), item:Optional[Item]=None, q:Optional[str] = None):
    result:dict = {"item_id":item_id}
    if q:
        result.update({"q":q})
    if item:
        result.update({"item":item})
    return result

class CustomerAddress(BaseModel):
    country:str
    city:str
    street:str
    zipcode:int
class Customer(BaseModel):
    name:str
    email:str
    address:CustomerAddress

class CargoType(Enum):
    SEA = "cargo"
    LAND = "land"
    
class Cargo(BaseModel):
    size:float
    cargo_type:CargoType


@app.put("/customers/")
async def update_customer(customer_id:int, customer:Customer,cargo:Cargo,important:int = Body(...)):
    return {"customer_id":customer_id, "customer":customer,"cargo":cargo,"important":important}

@app.put("/customers/here")
def customer_updating(customer_id:int,customer:Customer = Body(...,embed=False)):
    results = {"customer_id": customer_id, "customer": customer}
    return results 
    

# ? Login 
@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}