'''
import requests
# simple api call
response = requests.get(r"https://jsonplaceholder.typicode.com/posts")

data = response.json()
print(data)
print(data[:2])

# simple api call by id
response = requests.get(r"https://jsonplaceholder.typicode.com/posts/2")
data = response.json()
print(data)
'''

from fastapi import FastAPI
import requests
from fastapi import HTTPException


app = FastAPI()

# get all data
@app.get("/posts")
def get_posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    data = response.json()
    return data

# get data by id
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Post not found")
    data = response.json()
    return data 