# FastAPI – CRUD Operations

## 1. Overview

CRUD stands for **Create, Read, Update, and Delete**. These are the four fundamental operations used to manage data in an application.

In this tutorial, we build a simple Todo API using FastAPI and Pydantic. The API allows us to create todos, retrieve all todos, retrieve a specific todo, update an existing todo, and delete a todo.

### CRUD Operations

| Operation | HTTP Method | Purpose |
|---|---|---|
| Create | `POST` | Add a new todo |
| Read all | `GET` | Retrieve all todos |
| Read one | `GET` | Retrieve a todo by ID |
| Update | `PUT` | Replace an existing todo |
| Delete | `DELETE` | Remove a todo |

## 2. Project Structure

```text
crud_operations/
├── main.py
└── README.md
```

## 3. Code Explanation

### A. Import Modules and Initialize the Application

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

todos = []
```

- `FastAPI` creates the API application.
- `BaseModel` defines the structure and validation rules for todo data.
- `app = FastAPI()` initializes the application.
- `todos = []` creates an empty Python list to store todos temporarily.

**Important:** This list is in-memory storage. The data is lost when the application restarts, and it is not a substitute for a database.

### B. Define the Todo Model

```python
class Todo(BaseModel):
    id: int
    title: str
    completed: bool
```

The `Todo` model defines the structure of each todo.

| Field | Data Type | Description |
|---|---|---|
| `id` | `int` | Unique identifier for the todo |
| `title` | `str` | Description of the task |
| `completed` | `bool` | Indicates whether the task is completed |

All three fields are required because no default values are specified.

Example todo:

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "completed": false
}
```

## 4. Create API – POST

### Endpoint

`POST /todos`

### Code

```python
@app.post("/todos")
def create_todo(todo: Todo):
    todos.append(todo)
    return {
        "message": "Todo added",
        "data": todo
    }
```

### How it works

1. The client sends todo information in the request body.
2. FastAPI validates the data using the `Todo` model.
3. `todos.append(todo)` adds the todo to the list.
4. The API returns a confirmation message and the created todo.

### Example Request

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "completed": false
}
```

### Example Response

```json
{
  "message": "Todo added",
  "data": {
    "id": 1,
    "title": "Learn FastAPI",
    "completed": false
  }
}
```

## 5. Read All Todos – GET

### Endpoint

`GET /todos`

### Code

```python
@app.get("/todos")
def get_todo():
    return todos
```

### How it works

- Returns the entire `todos` list.
- If no todos have been created, it returns an empty list.
- No request body is required.

### Example Response

```json
[
  {
    "id": 1,
    "title": "Learn FastAPI",
    "completed": false
  },
  {
    "id": 2,
    "title": "Practice Python",
    "completed": true
  }
]
```

The example assumes that two todos have already been added.

## 6. Read a Specific Todo – GET by ID

### Endpoint

`GET /todos/{todo_id}`

### Code

```python
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo

    return {
        "Error": "Todo not found"
    }
```

### How it works

1. `todo_id` is extracted from the URL as a path parameter.
2. The loop checks each todo in the list.
3. If `todo.id == todo_id`, the matching todo is returned.
4. If no match exists, the function returns an error message.

### Example Request

`GET /todos/1`

### Example Response

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "completed": false
}
```

If the requested ID does not exist, the current code returns:

```json
{
  "Error": "Todo not found"
}
```

**Note:** This example returns a normal successful HTTP status even when the todo is missing. A more complete API should return HTTP `404 Not Found` in that case.

## 7. Update a Todo – PUT

### Endpoint

`PUT /todos/{todo_id}`

### Code

```python
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return {
                "message": "Todo updated",
                "data": updated_todo
            }

    return {
        "Error": "Todo not found"
    }
```

### How it works

- The target todo ID comes from the URL.
- `updated_todo` contains the new todo data in the request body.
- `enumerate(todos)` provides both the index and the todo object.
- When a matching ID is found, `todos[index] = updated_todo` replaces the existing item.
- If no match is found, the function returns an error message.

### Example Request

`PUT /todos/1`

Request body:

```json
{
  "id": 1,
  "title": "Complete FastAPI tutorial",
  "completed": true
}
```

### Example Response

```json
{
  "message": "Todo updated",
  "data": {
    "id": 1,
    "title": "Complete FastAPI tutorial",
    "completed": true
  }
}
```

**Important:** This implementation replaces the entire todo. The `id` in the request body should match the ID in the URL. The current code does not enforce that match, so additional validation would be needed for a robust API.

## 8. Delete a Todo – DELETE

### Endpoint

`DELETE /todos/{todo_id}`

### Code

```python
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {
                "Message": "Todo has been deleted"
            }

    return {
        "Error": "Todo not found"
    }
```

### How it works

1. The client provides the todo ID in the URL.
2. The loop searches for the matching todo.
3. `todos.pop(index)` removes the matching todo from the list.
4. The API returns a deletion confirmation.
5. If no todo matches the ID, an error message is returned.

### Example Request

`DELETE /todos/1`

### Example Response

```json
{
  "Message": "Todo has been deleted"
}
```

## 9. How to Run the Application

Open a terminal in the `crud_operations` folder and run:

```bash
python -m uvicorn main:app --reload
```

If running from the parent directory, use the folder's module path. For example:

```bash
python -m uvicorn crud_operations.main:app --reload
```

The `--reload` option restarts the development server when code changes are detected.

## 10. Test the API Using Swagger UI

Open the interactive documentation:

http://127.0.0.1:8000/docs

You can test all five endpoints directly from the browser.

Recommended testing order:

1. Use `POST /todos` to create a todo.
2. Use `GET /todos` to retrieve all todos.
3. Use `GET /todos/{todo_id}` to retrieve one todo.
4. Use `PUT /todos/{todo_id}` to update it.
5. Use `DELETE /todos/{todo_id}` to delete it.
6. Call `GET /todos` again to verify the deletion.

## 11. Important Concepts Learned

- **Pydantic models:** Define and validate todo data.
- **Request bodies:** Send data to create or update resources.
- **Path parameters:** Identify a specific todo using its ID.
- **HTTP methods:** Use POST, GET, PUT, and DELETE for different operations.
- **Python lists:** Store and manipulate todos in memory.
- **Loops:** Search for a todo by ID.
- **`enumerate()`:** Access both the list index and the todo object.
- **`append()`:** Add an item to the list.
- **`pop()`:** Remove an item from the list.
- **Automatic validation:** FastAPI validates request bodies and path parameter types.

## 12. Limitations of This Implementation

This is a beginner-level CRUD example, so it has a few limitations:

- Data is not persistent because it is stored in a Python list.
- Duplicate todo IDs are not prevented.
- Missing todos return error messages without an HTTP `404` status.
- The update operation replaces the entire todo rather than updating selected fields.
- There is no database, authentication, or authorization.

These can be improved later by adding proper error handling, ID validation, partial updates with PATCH, and database integration.

## Conclusion

This tutorial demonstrates how to build a basic CRUD API with FastAPI. It combines Pydantic models, HTTP methods, path parameters, request bodies, and Python list operations to manage todo items.

The same CRUD concepts are used in larger applications backed by databases such as SQLite, PostgreSQL, or MySQL.