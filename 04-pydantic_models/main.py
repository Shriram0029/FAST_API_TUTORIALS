from fastapi import FastAPI
from pydantic import BaseModel

'''
---------------------------------------------
app = FastAPI()

class User(BaseModel):
    name: str
    age: int
    email: str

@app.post("/create-user")
def create_user(user: User):
    return{
        "message" : "CREATED USER",
        "data" : user
    }
------------------------------------------------------------
'''

# NESTED MODELS
class Address(BaseModel):
    city: str
    pincode: int

class User(BaseModel):
    name: str
    age: int
    address: Address

app = FastAPI()

@app.post("/create-user")
def create_user(user: User):
    return{
        "message" : "CREATED USER",
        "data" : user
    }