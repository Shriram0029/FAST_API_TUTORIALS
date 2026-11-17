from fastapi import FastAPI

app = FastAPI()

#Home route
@app.get("/")
def home():
    return {"message":"WELCOME TO FASTAPI"}

# About route
@app.get("/about")
def about():
    return {"message":"This is about page"}

# users route
@app.get("/users")
def users():
    return {
        "users":["A","B","C","D"]
    }