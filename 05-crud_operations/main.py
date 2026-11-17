from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

todos = []

class Todo(BaseModel):
    id: int
    title: str
    completed: bool

# create API
@app.post("/todos")
def create_todo(todo: Todo):
    todos.append(todo)
    return{
        "message": "Todo added",
        "data": todo
    }

# read api
@app.get("/todos")
def get_todo():
    return todos

# read specific data
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return{
        "Error": "Todo not found"
    }

# update api
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return{
                "message": "Todo updated",
                "data": updated_todo
            }
    return{
        "Error": "Todo not found"
    }

# delete api
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return{
                "Message": "Todo has been deleted"
            }
    return{
        "Error": "Todo not found"
    }