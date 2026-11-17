# FastAPI – Pydantic Basics and Nested Models

## 1. Overview

This tutorial covers two concepts in FastAPI:

1. **Pydantic Basics** – Defining request body structures using Pydantic models and validating incoming data.
2. **Nested Models** – Using one Pydantic model as a field inside another model to represent structured data.

Pydantic models help FastAPI validate incoming JSON data and convert it into the expected Python types.

## 2. Project Structure

```text
pydantic_basics/
├── main.py
└── README.md
```

## 3. Pydantic Basics

### Code Example

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int
    email: str

@app.post("/create-user")
def create_user(user: User):
    return {
        "message": "CREATED USER",
        "data": user
    }
```

### Explanation

- `BaseModel` is imported from Pydantic to define the data model.
- `User` inherits from `BaseModel`.
- `name`, `age`, and `email` define the expected fields and their data types.
- `user: User` tells FastAPI to expect a request body matching the `User` model.
- FastAPI validates the incoming data before executing the endpoint function.

All three fields are required because no default values are specified.

### Example Request

**Endpoint:** `POST /create-user`

```json
{
  "name": "Shriram",
  "age": 21,
  "email": "shriram@example.com"
}
```

### Example Response

```json
{
  "message": "CREATED USER",
  "data": {
    "name": "Shriram",
    "age": 21,
    "email": "shriram@example.com"
  }
}
```

### Validation

If a required field is missing or a value cannot be converted to the expected type, FastAPI returns a request validation error, normally with HTTP status code `422`.

---

## 4. Nested Models

### What Is a Nested Model?

A nested model is a Pydantic model used as a field inside another Pydantic model.

It is useful when data contains multiple levels of structure. For example, a user has personal information and an address containing a city and pincode.

### Code Example

```python
from fastapi import FastAPI
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    pincode: int

class User(BaseModel):
    name: str
    age: int
    address: Address

app = FastAPI()

@app.post("/create-user")
def create_user(user: User):
    return {
        "message": "CREATED USER",
        "data": user
    }
```

### Explanation

**Address model**

```python
class Address(BaseModel):
    city: str
    pincode: int
```

Defines the structure of an address with two required fields.

**User model**

```python
class User(BaseModel):
    name: str
    age: int
    address: Address
```

Defines the user information. The important field is `address: Address`, which means the address must follow the structure defined by the `Address` model.

FastAPI and Pydantic validate both the user fields and the nested address fields.

### Example Request

**Endpoint:** `POST /create-user`

```json
{
  "name": "Shriram",
  "age": 21,
  "address": {
    "city": "Chennai",
    "pincode": 600001
  }
}
```

Notice that `address` is itself a JSON object containing `city` and `pincode`.

### Example Response

```json
{
  "message": "CREATED USER",
  "data": {
    "name": "Shriram",
    "age": 21,
    "address": {
      "city": "Chennai",
      "pincode": 600001
    }
  }
}
```

### Nested Model Validation

If the `pincode` field is missing or contains a value that cannot be converted to an integer, FastAPI returns a validation error.

This demonstrates that validation applies to nested fields as well as top-level fields.

---

## 5. How to Run the Application

Open the terminal inside the folder containing `main.py` and run:

```bash
python -m uvicorn main:app --reload
```

If running from the parent directory, use the appropriate module path for your folder. For example:

```bash
python -m uvicorn pydantic_basics.main:app --reload
```

## 6. Testing the API

Open the interactive API documentation:

http://127.0.0.1:8000/docs

1. Find `POST /create-user`.
2. Click **Try it out**.
3. Enter the appropriate JSON body.
4. Click **Execute**.
5. Check the response and status code.

Use the request body corresponding to the active `User` model in `main.py`.

## 7. Key Takeaways

- Pydantic's `BaseModel` defines the structure of request data.
- Type annotations specify the expected data types.
- FastAPI automatically parses and validates request bodies.
- Fields without default values are required.
- Nested models represent complex, hierarchical JSON structures.
- Validation applies recursively to nested model fields.
- Well-structured models make APIs easier to maintain and understand.

## 8. Concepts Covered

- Pydantic `BaseModel`
- Request body validation
- Required fields and type annotations
- POST endpoints
- Nested Pydantic models
- Nested JSON objects
- Automatic validation errors

**Next topic:** Explore optional fields, default values, and advanced Pydantic field validation.