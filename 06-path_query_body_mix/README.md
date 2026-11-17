# FastAPI – Path Parameters, Query Parameters, and Request Body

## 1. Overview

This tutorial demonstrates how FastAPI handles three important types of input:

1. **Path Parameters** – Identify a specific resource through the URL.
2. **Query Parameters** – Pass optional or additional information through the URL.
3. **Request Body** – Send structured data, usually in JSON format, to the API.

In this example, we build a simple User API that supports creating users, updating users, and retrieving all users.

## 2. Project Structure

```text
path_query_body/
├── main.py
└── README.md
```

## 3. Understanding the User Model

```python
class User(BaseModel):
    name: str
    age: int
```

The `User` model defines the structure of user data.

| Field | Data type | Purpose |
|---|---|---|
| `name` | `str` | User's name |
| `age` | `int` | User's age |

Both fields are required because no default values are specified.

The `users = []` list stores created users temporarily in memory.

## 4. Create a User – POST

### Endpoint

`POST /users`

```python
@app.post("/users")
def create_user(user: User):
    users.append(user)
    return {
        "message": "user created",
        "data": user
    }
```

### Concepts used

- **Request body:** `user: User` tells FastAPI to expect JSON matching the `User` model.
- **Pydantic validation:** FastAPI validates the incoming data.
- **List operation:** `users.append(user)` adds the new user to the list.

### Example request body

```json
{
  "name": "Shriram",
  "age": 21
}
```

### Example response

```json
{
  "message": "user created",
  "data": {
    "name": "Shriram",
    "age": 21
  }
}
```

No path or query parameters are required for this endpoint.

## 5. Update a User – PUT

### Endpoint

`PUT /users/{user_id}?notify=true`

```python
@app.put("/users/{user_id}")
def updated_user(user_id: int, user: User, notify: bool = False):
    if user_id < len(users):
        users[user_id] = user

        return {
            "message": "user updated",
            "notify": notify,
            "data": user
        }

    return {
        "Error": "USER NOT FOUND"
    }
```

This endpoint combines all three input types.

### A. Path Parameter – `user_id`

The path parameter identifies the user entry to update.

For example:

`PUT /users/0`

Here, `user_id` is `0`.

The type annotation `user_id: int` tells FastAPI to validate and convert the path value to an integer.

**Important:** In this implementation, `user_id` is used as a zero-based list index, not as a separately stored user ID. Therefore, `0` refers to the first user, `1` to the second, and so on.

### B. Query Parameter – `notify`

The parameter is declared as:

```python
notify: bool = False
```

- `notify` is a query parameter because it is a simple type and has a default value.
- Its default is `False`.
- You can override it by adding `?notify=true` to the URL.

Examples:

```text
PUT /users/0
PUT /users/0?notify=true
PUT /users/0?notify=false
```

If omitted, the response contains `"notify": false`.

If supplied as `true`, the response contains `"notify": true`.

**Note:** Your code only returns the `notify` value. It does not actually send a notification.

### C. Request Body – `user: User`

The request body provides the replacement user data.

Example:

```json
{
  "name": "Shriram Updated",
  "age": 22
}
```

FastAPI validates this JSON against the `User` model.

### Complete update example

Request:

```text
PUT /users/0?notify=true
```

Request body:

```json
{
  "name": "Shriram Updated",
  "age": 22
}
```

Example response:

```json
{
  "message": "user updated",
  "notify": true,
  "data": {
    "name": "Shriram Updated",
    "age": 22
  }
}
```

This assumes at least one user has already been created.

If the index does not exist, the current code returns:

```json
{
  "Error": "USER NOT FOUND"
}
```

## 6. Retrieve All Users – GET

### Endpoint

`GET /users`

```python
@app.get("/users")
def get_users():
    return users
```

This endpoint returns all users currently stored in the list.

- It does not require a request body.
- It does not require a path parameter.
- It does not require a query parameter.

### Example response

```json
[
  {
    "name": "Shriram Updated",
    "age": 22
  },
  {
    "name": "Priya",
    "age": 21
  }
]
```

The response depends on the users created during the current server session. If no users exist, it returns an empty list:

```json
[]
```

## 7. Summary of the Three Input Types

| Input type | Example in this code | Location |
|---|---|---|
| Path parameter | `user_id: int` | `/users/0` |
| Query parameter | `notify: bool = False` | `?notify=true` |
| Request body | `user: User` | JSON body |

### Complete URL example

```text
http://127.0.0.1:8000/users/0?notify=true
```

Breakdown:

- `/users/0` identifies the list index using a path parameter.
- `notify=true` passes a query parameter.
- The JSON request body supplies the new user's name and age.

All three can be used in the same endpoint.

## 8. How to Run the Application

Open a terminal inside the folder containing `main.py` and run:

```bash
python -m uvicorn main:app --reload
```

If running from the parent directory, use the appropriate module path for your tutorial folder.

## 9. Test Using Swagger UI

Open:

http://127.0.0.1:8000/docs

Recommended testing sequence:

1. Use `POST /users` to create the first user.
2. Create another user if you want to test a second list index.
3. Use `GET /users` to retrieve all users.
4. Use `PUT /users/{user_id}` with `user_id = 0` and a JSON request body.
5. Try `notify = true` and `notify = false` in the query parameter.
6. Use `GET /users` again to verify the updated data.

## 10. Important Limitations

- The users are stored in memory and disappear when the application restarts.
- The update endpoint uses a zero-based list index instead of a dedicated user ID.
- Negative `user_id` values can unintentionally update entries because Python supports negative list indices.
- Missing users return a JSON error message with a successful HTTP status instead of `404 Not Found`.
- The `notify` parameter is returned in the response but does not trigger a notification.

These limitations are useful learning points for improving the API later.

## 11. Key Takeaways

- Path parameters identify resources.
- Query parameters provide additional URL-based options.
- Request bodies carry structured data.
- FastAPI determines parameter roles from their declarations and types.
- Pydantic models validate request body data.
- A single endpoint can combine path parameters, query parameters, and a request body.

**Concepts covered:** CRUD fundamentals, Pydantic models, path parameters, query parameters, request bodies, and FastAPI endpoint handling.