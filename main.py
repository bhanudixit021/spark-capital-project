from fastapi import FastAPI,Body,Depends
import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from data_extract import DataExtract
from datetime import datetime
import re


Base.metadata.create_all(engine)

extract_session = DataExtract()

def get_session(): # to allow us to access the database session
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


app = FastAPI()


# @app.get("/items")
# def getItems(session:Session=Depends(get_session)):
#     items = session.query(models.Item).all()
#     return items


@app.get('/users')
def allusers(session:Session=Depends(get_session)):
    usersObject = session.query(models.Users).all()
    return usersObject


# @app.get("/items{id}")
# def getItem(id:int,session:Session=Depends(get_session)):
#     item = session.query(models.Item).get(id)
#     return item


@app.get('/users/{int}')
def getuser(id:int,session:Session=Depends(get_session)):
    usersObject = session.query(models.Users).get(id)
    return usersObject


# @app.get(('/data'))
# async def getData(session:Session=Depends(get_session)):
#     dataItem = session.query(models.BseData).all()
#     return dataItem



@app.get('/ed/{str}')
async def extract_data(base_url:str,session:Session=Depends(get_session)):
    context = extract_session._collect_data(base_url=base_url)
    message = 'data is not updated'
    if context['flag']:
        message = 'DataBase updated with new values'
        complete_data = context['base_data_collection']
        for data in complete_data:
            dataObject = models.BseData(
                deal_date = datetime.strptime(data['date'],'%m/%d/%Y'),
                security_code = data['security_code'],
                security_name = data['security_name'],
                client_name = data['client_name'],
                deal_type = data['deal_type'],
                quantity = data['quantity'],
                price = float(re.sub(',','',data['price']))
            )
            session.add(dataObject)
            session.commit()
            session.refresh(dataObject)
        
        return message


# @app.post("/items")
# def addItem(item:schemas.Item,session:Session=Depends(get_session)):
#     item = models.Item(task = item.task)
#     session.add(item)
#     session.commit()
#     session.refresh(item)
#     return item


@app.post('/users')
def addusers(user:schemas.Users,session:Session=Depends(get_session)):
    usersObject = models.Users(name =user.name,email = user.email )
    session.add(usersObject)
    session.commit()
    session.refresh(usersObject)
    return usersObject


# @app.put("/items/{id}")
# def updateItem(id:int,item:schemas.Item,session:Session=Depends(get_session)):
#     itemObject = session.query(models.Item).get(id)
#     itemObject.task = item.task
#     session.commit()
#     return itemObject


@app.put('/users/{int}')
def updateusers(id:int,user:schemas.Users,session:Session=Depends(get_session)):
    usersObject = session.query(models.Users).get(id)
    usersObject.name = user.name
    usersObject.email = user.email
    session.commit()
    return usersObject


# @app.delete("/items/{int}")
# def deleteItem(id:int,item:schemas.Item,session:Session=Depends(get_session)):
#     item = session.query(models.Item).get(id)
#     session.delete(item)
#     session.commit()
#     session.close()
#     return "Item as deleted"


@app.delete('/users/{int}')
def deleteusers(id:int,session:Session=Depends(get_session)):
    usersObject = session.query(models.Users).get(id)
    session.delete(usersObject)
    session.commit()
    session.close()
    return "User was deleted"

