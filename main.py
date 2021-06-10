from typing import Optional
from fastapi import FastAPI,Query,Path
from pydantic import BaseModel



app = FastAPI()

# ? Base Item Structure
class Item(BaseModel):
    name:str
    description:str
    price:float
    tax : Optional[float] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}

# ? Query validations

@app.get("/items")
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
    
    

