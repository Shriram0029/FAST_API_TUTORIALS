# FastAPI – Query Parameters

## 1. Overview

Query parameters are values passed to an API endpoint through the URL, after a `?` symbol.

They are commonly used to filter, search, sort, or limit the data returned by an API.

**Example URL:**

```text
http://127.0.0.1:8000/items?name=laptop&price=50000
```

Here:
- `name=laptop` is the first query parameter.
- `price=50000` is the second query parameter.
- `&` separates multiple query parameters.

## 2. Project Structure

```text
query_parameters/
├── main.py
└── README.md
```

## 3. Code Explanation

### A. Query Parameter Without a Default Value

```python
@app.get("/users")
def get_users(name):
    return {
        "name": name
    }
```

- `name` is treated as a required query parameter because no default value is provided.
- The client must supply `name` in the URL.

**Example request:**

```text
GET /users?name=Shriram
```

**Response:**

```json
{
  "name": "Shriram"
}
```

If `name` is omitted, FastAPI returns a validation error because the parameter is required.

### B. Optional Query Parameter

```python
@app.get("/users")
def get_users(name: str = None):
    return {
        "name": name
    }
```

- `name: str` indicates that the parameter is expected to be a string.
- `= None` gives the parameter a default value of `None`, making it optional.
- If the client does not provide `name`, the response contains `null`.

**Example request:**

```text
GET /users
```

**Response:**

```json
{
  "name": null
}
```

**Example request with a value:**

```text
GET /users?name=Shriram
```

**Response:**

```json
{
  "name": "Shriram"
}
```

### C. Query Parameter with a Default Value

```python
@app.get("/products")
def get_products(limit: int = 10):
    return {
        "limit": limit
    }
```

- `limit: int` specifies that the value must be an integer.
- `= 10` sets the default value to `10`.
- If the client does not provide `limit`, FastAPI uses `10`.

**Example request:**

```text
GET /products
```

**Response:**

```json
{
  "limit": 10
}
```

**Example request with a custom value:**

```text
GET /products?limit=5
```

**Response:**

```json
{
  "limit": 5
}
```

### D. Multiple Query Parameters

The active example in `main.py` is:

```python
@app.get("/items")
def get_items(name: str = None, price: int = 0):
    return {
        "name": name,
        "price": price
    }
```

This endpoint accepts two query parameters: `name` and `price`.

- `name: str = None` makes `name` optional, with a default value of `None`.
- `price: int = 0` makes `price` optional, with a default value of `0`.
- FastAPI converts valid integer query values into Python integers and validates invalid values.

**Example 1 — Provide both parameters**

Request:

```text
GET /items?name=laptop&price=50000
```

Response:

```json
{
  "name": "laptop",
  "price": 50000
}
```

**Example 2 — Provide only the name**

Request:

```text
GET /items?name=keyboard
```

Response:

```json
{
  "name": "keyboard",
  "price": 0
}
```

**Example 3 — Provide no parameters**

Request:

```text
GET /items
```

Response:

```json
{
  "name": null,
  "price": 0
}
```

**Example 4 — Invalid integer**

Request:

```text
GET /items?name=laptop&price=abc
```

FastAPI returns an HTTP `422 Unprocessable Entity` validation response because `abc` cannot be converted to an integer.

## 4. How to Run the Application

Open the terminal in the parent project directory and run:

```bash
python -m uvicorn query_parameters.main:app --reload
```

Alternatively, open the terminal inside the `query_parameters` folder and run:

```bash
python -m uvicorn main:app --reload
```

## 5. Testing the API

Once the server is running, open:

- **API endpoint:** http://127.0.0.1:8000/items
- **Interactive API documentation:** http://127.0.0.1:8000/docs

Try adding query parameters directly to the URL:

```text
http://127.0.0.1:8000/items?name=laptop&price=50000
```

You can also test the endpoint through the interactive Swagger UI at `/docs`.

## 6. Key Takeaways

- Query parameters appear after `?` in a URL.
- Use `&` to separate multiple query parameters.
- Parameters without default values are required.
- Parameters with default values are optional.
- `None` is returned as JSON `null`.
- Type annotations such as `int` allow FastAPI to validate and convert incoming values.
- Query parameters are useful for filtering, searching, pagination, and controlling API responses.

**Next topic:** Learn about required and optional query parameters in more detail, including validation rules and constraints.