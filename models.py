from sqlalchemy import Column,Integer,String,Float,Date
from database import Base
from typing import Union
import datetime



class Item(Base):
    __tablename__ = 'items' # table name
    id = Column(Integer,primary_key=True)
    task = Column(String(255))


class Users(Base):
    __tablename__ = 'users' # table name
    id = Column(Integer,primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))

class BseData(Base):
    __tablename__ = 'bse_data'
    id = Column(Integer,primary_key=True)
    deal_date =  Column(Date,default=datetime.date)
    security_code = Column(Integer)
    security_name = Column(String(255))
    client_name = Column(String(255))
    deal_type = Column(String(255))
    quantity = Column(Integer)
    price = Column(Float)

