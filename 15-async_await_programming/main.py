from fastapi import FastAPI
import time
import asyncio

# synchronous programming example
'''
def task():
    time.sleep(3)
    return "Done"
'''

# asynchronous programming
'''
async def task():
    await asyncio.sleep(3)
    return "Done"
'''

app = FastAPI()

@app.get("/")
async def home():
    await asyncio.sleep(3)
    return{
        "message": "Async API"
    }
