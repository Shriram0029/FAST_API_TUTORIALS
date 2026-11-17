
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allowed Frontend Origins
origins = [
    "http://localhost:5500"
]

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
