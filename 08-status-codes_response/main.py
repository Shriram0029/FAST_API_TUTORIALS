from fastapi import FastAPI, status, HTTPException

app = FastAPI()

# HTTP Status code
@app.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user():
    return{
        "message" : "User Created"
    }

# Custom Responses
@app.get("/user")
def get_user():
    return{
        "status" : "success",
        "message": "User Fetched",
        "data": {
            "name" : "Shriram",
            "age" : 24,
        }
    }

# Basic Error Handling
@app.get("/users/{user_id}")
def get_users(user_id: int):
    if user_id != 1:
        raise HTTPException(
            status_code=404, 
            detail="User Not Found"
        )
    return{
        "data" : user_id,
        "name" : "Shriram"
    }




