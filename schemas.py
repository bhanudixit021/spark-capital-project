from pydantic import BaseModel

class Item(BaseModel):
    task:str

    
class Users(BaseModel):
    name:str
    email:str