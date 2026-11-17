
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import os
# from dotenv import load_dotenv
from config import settings

app = FastAPI()
# load_dotenv()

origins = settings.origins
# SECRET_KEY = os.getenv("SECRET_KEY")
# DB_URL = os.getenv("DB_URL")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # get, put, post, delete
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {
        "message": "CORS ENABLE API"
    }
