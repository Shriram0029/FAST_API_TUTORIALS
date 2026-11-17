# FastAPI – Request Body and Pydantic Models

## 1. Overview

A **request body** is data sent by a client to an API, usually in JSON format.

In FastAPI, Pydantic models are used to define the structure of the request body, validate incoming data, and convert it into the expected Python types.

This tutorial demonstrates how to create a user using a POST request.

## 2. Project Structure

```text
request_body/
├── main.py
└── README.md
```

## 3. Code Explanation

### A. Import Required Modules

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
```

- `FastAPI` is used to create the API application.
- `BaseModel` is imported from Pydantic to define the structure of the request data.
- `app = FastAPI()` creates the application instance.

### B. Define the User Model

```python
class User(BaseModel):
    name: str
    age: int
    clg_name: str
    qualification: str
    graduation_year: int
```

The `User` class defines the expected structure of the incoming JSON data.

| Field | Data type | Purpose |
|---|---|---|
| `name` | `str` | User's name |
| `age` | `int` | User's age |
| `clg_name` | `str` | College name |
| `qualification` | `str` | Educational qualification |
| `graduation_year` | `int` | Year of graduation |

Since no default values are provided, all five fields are required.

Pydantic validates the incoming data against the model. For example, it can convert a valid integer string into an integer and rejects values that cannot be converted.

### C. Create the POST Endpoint

```python
@app.post("/create-user")
def create_user(user: User):
    return {
        "message": "user created",
        "data": user
    }
```

- `@app.post("/create-user")` defines an endpoint that accepts POST requests.
- `user: User` tells FastAPI to expect a request body matching the `User` model.
- FastAPI validates the request body before calling the function.
- The response contains a success message and the submitted user data.

## 4. Example Request

Send a POST request to:

```text
http://127.0.0.1:8000/create-user
```

Request body:

```json
{
  "name": "Shriram",
  "age": 21,
  "clg_name": "ABC Engineering College",
  "qualification": "B.Tech",
  "graduation_year": 2027
}
```

## 5. Example Response

```json
{
  "message": "user created",
  "data": {
    "name": "Shriram",
    "age": 21,
    "clg_name": "ABC Engineering College",
    "qualification": "B.Tech",
    "graduation_year": 2027
  }
}
```

## 6. What Happens If Data Is Missing or Invalid?

### Missing required field

If `graduation_year` is omitted, FastAPI returns a validation error because the field is required.

### Invalid data type

If `age` is provided as `"twenty-one"`, Pydantic cannot convert it into an integer and returns a validation error.

By default, FastAPI responds with HTTP `422 Unprocessable Entity` when request validation fails.

## 7. How to Run the Application

From the parent project directory, run:

```bash
python -m uvicorn request_body.main:app --reload
```

Alternatively, open the terminal inside the `request_body` folder and run:

```bash
python -m uvicorn main:app --reload
```

## 8. How to Test the Endpoint

Open the automatically generated interactive API documentation:

http://127.0.0.1:8000/docs

1. Find `POST /create-user`.
2. Click **Try it out**.
3. Enter the JSON request body.
4. Click **Execute**.
5. Inspect the response and status code.

## 9. Key Takeaways

- A request body carries data from a client to an API.
- POST requests are commonly used to create resources.
- Pydantic's `BaseModel` defines the expected data structure.
- FastAPI automatically parses and validates request bodies.
- Fields without default values are required.
- Default values can make fields optional in incoming requests.
- Invalid request data produces a validation error.

**Next topic:** Explore default values, optional fields, and Pydantic field validation.