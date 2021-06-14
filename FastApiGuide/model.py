from sqlalchemy import Column,ForeignKey,Boolean,Integer,String
from sqlalchemy.orm import relationship,Session
from db import Base
from schemas import UserCreation

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String, index=True)
    email = Column(String,unique=True,index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    items = relationship("Item", back_populates="owner")

    def get_user(self, db:Session, user_id:int) :
        return db.query(self).filter(self.id == user_id).first()

  
   


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")

    