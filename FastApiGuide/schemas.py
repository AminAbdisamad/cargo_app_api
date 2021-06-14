
from pydantic import BaseModel

# Item Model
class BaseItem(BaseModel):
    title:str
    description:str

class CreateItem(BaseItem):
    pass

class Item(BaseItem):
    id:int
    owner_id:int

    class Config:
        orm_mode = True


# User Model

class UserBase(BaseModel):
    name:str
    email:str
    

class UserCreation(UserBase):
    password:str

class User(UserBase):
    id:int
    is_active:bool
    items: list[Item] = []
    # Config class is used to provide configurations to Pydantic
    class Config:
        # orm_mode = True allows us to get relationship data
        orm_mode = True

