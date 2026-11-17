# FastAPI – Dynamic Routes and Path Parameters

## 1. Overview

This tutorial explains how to create dynamic routes in FastAPI and how to specify the data type of a path parameter.

A **dynamic route** allows an API endpoint to accept values directly from the URL.

## 2. Project Structure

```text
dynamic_routes/
├── main.py
└── README.md
```

## 3. Code Explanation

### A. Creating a FastAPI Application

```python
from fastapi import FastAPI

app = FastAPI()
```

- `FastAPI` is imported to create the application.
- `app = FastAPI()` creates the application instance used to define API routes.

### B. Dynamic Route with the Default Data Type

```python
@app.get("/users/{user_id}")
def users(user_id):
    return {
        "user_id_for_the_username": user_id
    }
```

- `/users/{user_id}` defines a dynamic path parameter.
- The value provided in the URL is passed to the `user_id` parameter.
- Without a type annotation, FastAPI treats the parameter as a string by default.

**Example request:**

```text
GET /users/101
```

**Response:**

```json
{
  "user_id_for_the_username": "101"
}
```

Notice that `"101"` is a string.

### C. Dynamic Route with a Specific Data Type

```python
@app.get("/users/{user_id}")
def users(user_id: int):
    return {
        "user_id_for_the_username": user_id
    }
```

- Adding `: int` specifies that `user_id` must be an integer.
- FastAPI validates the incoming value and converts valid integer strings into integers.
- If the supplied value cannot be converted to an integer, FastAPI returns a validation error.

**Example request:**

```text
GET /users/101
```

**Response:**

```json
{
  "user_id_for_the_username": 101
}
```

Notice that `101` is now a number, not a string.

**Invalid request:**

```text
GET /users/abc
```

FastAPI returns an HTTP `422 Unprocessable Entity` validation response because `abc` is not a valid integer.

## 4. How to Run the Application

Open a terminal in the parent project directory and execute:

```bash
python -m uvicorn dynamic_routes.main:app --reload
```

Alternatively, open the terminal inside the `dynamic_routes` folder and run:

```bash
python -m uvicorn main:app --reload
```

The `--reload` option automatically restarts the development server when code changes are detected.

## 5. Testing the API

After starting the server, open these URLs in your browser:

- **API endpoint:** http://127.0.0.1:8000/users/101
- **Interactive API documentation:** http://127.0.0.1:8000/docs

Try changing `101` to another number, then try a string such as `abc` when the parameter is declared as `int`.

## 6. Key Takeaways

- Dynamic routes use curly braces, such as `{user_id}`.
- Path parameters capture values from the URL.
- Without a type annotation, a path parameter defaults to a string.
- Using `user_id: int` enables integer validation and conversion.
- Invalid values produce a validation error.
- FastAPI generates interactive API documentation automatically.

