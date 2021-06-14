from typing import Optional
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

#? Function Dependencies

async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons

# ? Class Dependencies
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
class CommonQueries:
    def __init__(self,q:Optional[str]=None,skip:int = 0, limit:int = 10):
        self.q = q
        self.skip = skip 
        self.limit = limit

@app.get("/get/items")    
async def get_items(commons:CommonQueries = Depends(CommonQueries)):
    data:dict = {}
    if commons.q:
        data.update({"q":commons.q})
    items = fake_items_db[commons.skip:commons.skip + commons.limit]
    data.update({"items":items})
    return data

@app.get("get/itemz/")
async def get_itemz(commons: CommonQueries = Depends()):
    response:dict = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key



@app.get("/auth/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def auth():
    return [{"item": "Foo"}, {"item": "Bar"}]
