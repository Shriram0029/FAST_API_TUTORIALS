from fastapi import FastAPI, Request
import time
app = FastAPI()

# simple middleware
'''
@app.middleware("http")
async def my_middleware(request:Request,call_next):
    print("request recieved")

    response = await call_next(request)

    print("response sent")

    return response
'''

# logging middleware
@app.middleware("http")
async def my_middleware_logging(request:Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    print(f"Path : {request.url.path}  |  Time:{process_time}")

    return response