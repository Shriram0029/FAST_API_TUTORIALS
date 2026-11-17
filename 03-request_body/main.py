'''
--------------------------------------------------------------
from fastapi import FastAPI

app = FastAPI()

@app.post("/create-user")

# def create_user(name: str, age: int):
#     return{
#         "name": name,
#         "age": age
#     }

def create_user(user: dict):
    return{
        "message":"user created",
        "data":user
    }
-------------------------------------------------------------
'''


from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int
    clg_name: str
    qualification: str
    graduation_year: int

@app.post("/create-user")
def create_user(user: User):
    return{
        "message":"user created",
        "data":user
    }
