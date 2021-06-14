from typing import Optional
from sqlalchemy import Column,String,Boolean,Integer,ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from database import Base


# **********************
# * SQLAlchemy Models  *
# **********************

class CargoSenderModel(Base):
    __tablename__ = "cargo_sender"
    id =  Column(Integer, primary_key=True,index=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    phone = Column(String, index=True, unique=True)
    Country = Column(String, index=True)
    city = Column(String, index=True)
    address = Column(String, index=True)
    sent_cargos = relationship("Cargo", back_populates="cargo_sender")

class CargoReceiverModel(Base):
    __tablename__ = "cargo_receiver"
    id =  Column(Integer, primary_key=True,index=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    phone = Column(String, index=True, unique=True)
    Country = Column(String, index=True)
    city = Column(String, index=True)
    address = Column(String, index=True)
    received_cargos = relationship("Cargo", back_populates="cargo_receiver")


class CargoModel(Base):
    __tablename__ = "cargo"
    id = Column(Integer, primary_key=True,index=True)
    description = Column(String, index=True)
    orgin_country = Column(String, index=True)
    destination_country = Column(String,index=True)
    unit = Column(String,index=True)
    cargo_sender_id = Column(Integer, ForeignKey("cargo_sender.id"))
    cargo_sender = relationship("CargoSender", back_populates="sent_cargos")
    cargo_receiver_id = Column(Integer, ForeignKey("cargo_receiver.id"))
    cargo_receiver = relationship("CargoReceiver", back_populates="received_cargos")



# ********************
# * Pydantic Schemas *
# ********************

# ** Cargo Schema

class BaseCargoSchema(BaseModel):
    description: Optional[str] = None
    origin_country:str
    destination_country:str
    unit:str
    cargo_sender_id:int
    cargo_receiver_id:int

class CreateCargoSchema(BaseCargoSchema):
    pass

class CargoSchema(BaseCargoSchema):
    id:int
    class Config:
        # orm_mode = True allows us to get relationship data
        orm_mode = True



# ** Cargo Receiver Schema
class BaseCargoReceiverSchema(BaseModel): 
    name:str
    email:str 
    phone:str 
    Country:str
    city:str
    address:str
   
class CreateCargoReceiverSchema(BaseCargoReceiverSchema):
    pass

class CargoReceiverSchema(BaseCargoReceiverSchema):
    id:int
    received_cargos:list[CargoSchema] = []
    class Config:
        orm_mode = True


# ** Cargo Sender Schema

class BaseCargoSenderSchema(BaseModel): 
    name:str
    email:str 
    phone:str 
    Country:str
    city:str
    address:str
   
class CreateCargoSenderSchema(BaseCargoSenderSchema):
    pass

class CargoSenderSchema(BaseCargoSenderSchema):
    id:int
    send_cargos:list[CargoSchema] = []
    class Config:
        orm_mode = True
