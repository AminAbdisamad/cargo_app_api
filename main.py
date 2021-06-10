from typing import Optional
from fastapi import FastAPI,Query
from pydantic import BaseModel



app = FastAPI()


class Item(BaseModel):
    name:str
    description:str
    price:float
    tax : Optional[float] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items")
async def items(q:Optional[str] = Query(None,min_length=2, max_length=20,regex="^fixedquery$")):
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


@app.post("/item")
def save_items(item:Item):
    items = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        items.update({"total_price":price_with_tax})
    return items

@app.put("/items/{item_id}")
def update_item(item_id:int, item:Item):
    return {"item_id":item_id,**item.dict()}
