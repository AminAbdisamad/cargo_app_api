from typing import Optional
from sqlalchemy.orm import Session
from .schemas import UserCreation,CreateItem
from .model import User,Item

def save(db:Session,user:UserCreation):
    db.add(user)
    db.commit()
    db.refresh(user)

def create_users(db:Session, user: UserCreation)->Optional[User]:
    #? This should be upgraded
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password,name=user.name)
    save(db,db_user)
    return db_user

def get_users(db:Session, skip:int= 0, limit:int=100)->Optional[User]:
        return db.query(User).offset(skip).limit(limit).all()


def get_user_by_email(db:Session, email:str)->Optional[User]:
    return db.query(User).filter(User.email == email).first()


def create_user_item(db:Session, item:CreateItem,owner_id:int)->Optional[Item]:
    db_item = Item(**item.dict(),owner_id=owner_id)
    save(db,db_item)
    return db_item