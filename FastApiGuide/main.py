from fastapi import Depends, FastAPI, HTTPException,status
from sqlalchemy.orm import Session

from model import Base,User as UserModel
from schemas import UserCreation,User as UserSchema, Item,CreateItem
from db import SessionLocal, engine
from services import get_users as get_all ,create_users,get_user_by_email,create_user_item



Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/",response_model=UserSchema)
def create_user(user:UserCreation, db:Session = Depends(get_db)):
    user_exist = get_user_by_email(db,user.email)
    if user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User already exist")
    return create_users(db,user)


@app.get("/users/",response_model=list[UserSchema])
def get_users(db:Session = Depends(get_db)):
   return get_all(db)



@app.post("/items/",response_model=Item)
def create_item(user_id:int, item:CreateItem, db:Session = Depends(get_db)):
   return create_user_item(db,item,user_id)