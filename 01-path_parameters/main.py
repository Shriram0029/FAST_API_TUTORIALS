from fastapi import FastAPI

app = FastAPI()

'''
# users route - (default string)
@app.get("/users/{user_id}")
def users(user_id):
    return{
        "user_id_for_the_username":user_id
    }
'''

# users route - (with specific data type)
@app.get("/users/{user_id}")
def users(user_id:int):
    return{
        "user_id_for_the_username":user_id
    }