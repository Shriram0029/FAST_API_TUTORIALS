from fastapi import FastAPI, Depends, Header, HTTPException

app = FastAPI()

# dependency injection
'''
def common_logic():
    return{
        "message":"common logic executed"
    }

@app.get("/home")
def home(data = Depends(common_logic)):
    return data
'''

# real life example (reusable logic)
'''
def get_current_user():
    return{
        "user" : "Shriram"
    }

@app.get("/profile")
def profile(user = Depends(get_current_user)):
    return user

@app.get("/dashboard")
def profile(user = Depends(get_current_user)):
    return user
'''

# Token Handling through Auth(real example)
def verify_token(token:str = Header(None)):
    if token != "mine":
        raise HTTPException(
            status_code=401,
            detail = "UnAuthorized"
        )
    return{
        "user" : "Authorized User"
    }

@app.get("/secure-data")
def secure_data(user = Depends(verify_token)):
    return{
        "message":"Secure Data accessed",
        "user":user
    }

