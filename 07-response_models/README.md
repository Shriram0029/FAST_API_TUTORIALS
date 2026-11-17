# FastAPI – Response Models

## 1. Overview

A **Response Model** in FastAPI defines the structure of the data that an API should return to the client.

FastAPI uses Pydantic models to validate, serialize, and filter the outgoing response data.

Response models are useful for:

1. **Response Validation** – Ensuring that the returned data follows the expected structure and data types.
2. **Hiding Sensitive Data** – Preventing confidential information, such as passwords, from being exposed in API responses.
3. **Output Formatting** – Controlling which fields are included in the final response.
4. **API Documentation** – Automatically generating response schemas in Swagger UI.

## 2. Project Structure

```text
response_models/
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
- `BaseModel` is imported from Pydantic to define data models.
- `app = FastAPI()` initializes the application.

### B. Define the User Model

```python
class User(BaseModel):
    name: str
    age: int
    password: str
```

The `User` model defines the complete user information.

| Field | Data Type | Description |
|---|---|---|
| `name` | `str` | User's name |
| `age` | `int` | User's age |
| `password` | `str` | User's password |

This model contains all three fields, including the sensitive password field.

### C. Define the UserResponse Model

```python
class UserResponse(BaseModel):
    name: str
    age: int
```

The `UserResponse` model defines the fields that should be included in the API response.

| Field | Data Type | Description |
|---|---|---|
| `name` | `str` | User's name |
| `age` | `int` | User's age |

Notice that the `password` field is not included in this model.

This is intentional because sensitive information should not be exposed to clients.

### D. Create the GET Endpoint with a Response Model

```python
@app.get("/user", response_model=UserResponse)
def get_user():
    return {
        "name": "Shriram",
        "age": 21,
        "password": "123#"
    }
```

The important part of this endpoint is:

```python
response_model=UserResponse
```

This tells FastAPI to use the `UserResponse` model to validate and filter the outgoing response.

The function returns three fields:

- `name`
- `age`
- `password`

However, the `UserResponse` model contains only two fields:

- `name`
- `age`

Therefore, FastAPI removes the extra `password` field before sending the response to the client.

## 4. Example Request

Send a GET request to:

```text
http://127.0.0.1:8000/user
```

No request body or query parameters are required.

## 5. Example Response

Although the Python function returns:

```json
{
  "name": "Shriram",
  "age": 21,
  "password": "123#"
}
```

The actual API response will be:

```json
{
  "name": "Shriram",
  "age": 21
}
```

The password is automatically excluded because it is not defined in the `UserResponse` model.

This demonstrates how response models help prevent sensitive fields from being exposed in API responses.

## 6. How Response Validation Works

FastAPI performs response validation using the specified response model.

The process is:

1. The endpoint function executes.
2. The function returns a Python dictionary.
3. FastAPI validates the returned data against `UserResponse`.
4. Fields not included in the response model are excluded.
5. The validated and filtered data is serialized into JSON.
6. The final response is sent to the client.

If the returned data does not satisfy the response model's requirements, FastAPI raises a response validation error.

## 7. Important Difference Between User and UserResponse

| User Model | UserResponse Model |
|---|---|
| Contains complete user information | Contains only public user information |
| Includes the password | Excludes the password |
| Represents the full data structure | Represents the API output structure |
| Used to define all user fields | Used to control the response |

Using separate models allows an application to maintain complete internal data while exposing only the required information to clients.

## 8. How to Run the Application

Open a terminal inside the `response_models` folder and execute:

```bash
python -m uvicorn main:app --reload
```

Alternatively, run from the parent project directory using the appropriate module path:

```bash
python -m uvicorn response_models.main:app --reload
```

## 9. Test Using Swagger UI

Open the interactive API documentation:

http://127.0.0.1:8000/docs

1. Find `GET /user`.
2. Click **Try it out**.
3. Click **Execute**.
4. Observe the response.
5. Notice that the password is not included in the response.

## 10. Key Takeaways

- A response model defines the structure of an API response.
- `response_model` is used to specify the expected response schema.
- FastAPI validates the outgoing response against the specified model.
- Extra fields are excluded by default when they are not present in the response model.
- Sensitive information can be hidden from API responses.
- Response models improve consistency and automatic API documentation.

## 11. Concepts Covered

- Pydantic response models
- Response validation
- `response_model` parameter
- Sensitive data filtering
- Output formatting
- Automatic response serialization
- Swagger UI response documentation

**Conclusion:** Response models provide control over the data returned by an API. They help ensure that clients receive only the required information in a properly structured format.