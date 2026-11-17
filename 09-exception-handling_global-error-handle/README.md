# FastAPI – Exception Handling

## 1. Overview

Exception handling is the process of identifying, managing, and responding to errors that occur during API execution.

FastAPI provides different mechanisms for handling errors and returning meaningful responses to clients.

This tutorial covers three important approaches:

1. **HTTPException** – Used to raise standard HTTP errors with a specific status code and error message.
2. **Custom Exceptions** – Used to define application-specific exceptions based on business requirements.
3. **Global Exception Handler** – Used to handle custom exceptions centrally and return a consistent error response.

## 2. Project Structure

```text
exception_handling/
├── main.py
└── README.md
```

## 3. HTTPException

### What is HTTPException?

`HTTPException` is a built-in FastAPI exception used to terminate request processing and return an HTTP error response.

It allows developers to specify:

- HTTP status code
- Error message through the `detail` parameter
- Optional response headers

### Code Example

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    return {
        "data": 1,
        "name": "Shriram"
    }
```

### Explanation

- `@app.get("/users/{user_id}")` defines a GET endpoint with a path parameter.
- `user_id: int` specifies that the user ID must be an integer.
- The condition checks whether the requested ID is different from `1`.
- If the condition is true, `HTTPException` is raised.
- `status_code=400` specifies the HTTP error status.
- `detail` contains the error message.
- If the user ID is `1`, the function returns the user information.

### Example 1 – Successful Request

Request:

```text
GET /users/1
```

Response:

```json
{
  "data": 1,
  "name": "Shriram"
}
```

HTTP Status Code: `200 OK`

### Example 2 – Error Response

Request:

```text
GET /users/2
```

Response:

```json
{
  "detail": "User not found"
}
```

HTTP Status Code: `400 Bad Request`

**Important:** HTTP `404 Not Found` would generally be more appropriate when the requested user does not exist. Your example uses `400` to demonstrate HTTPException.

---

## 4. Custom Exceptions

### What Are Custom Exceptions?

Custom exceptions are user-defined exceptions created to handle specific application errors.

Instead of relying only on predefined HTTP exceptions, developers can define their own exception classes based on application requirements.

For example, an application may define exceptions such as:

- `UserNotFoundException`
- `ProductNotFoundException`
- `InvalidOrderException`
- `InsufficientBalanceException`

### Code Example

```python
class UserNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.get("/user/{name}")
def get_user(name: str):
    if name != "Shriram":
        raise UserNotFoundException(name)

    return {
        "name": name
    }
```

### Explanation

**A. Creating a Custom Exception Class**

```python
class UserNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name
```

- `UserNotFoundException` is a user-defined exception class.
- It inherits from Python's built-in `Exception` class.
- The constructor accepts a username.
- `self.name = name` stores the username associated with the exception.

Inheriting from `Exception` makes the class a valid Python exception that can be raised using the `raise` keyword.

**B. Raising the Custom Exception**

```python
@app.get("/user/{name}")
def get_user(name: str):
    if name != "Shriram":
        raise UserNotFoundException(name)

    return {
        "name": name
    }
```

- The endpoint accepts a username through the path parameter.
- The condition checks whether the name is different from `"Shriram"`.
- If the condition is true, the custom exception is raised.
- Otherwise, the function returns the username.

### Example Requests

**Valid request:**

```text
GET /user/Shriram
```

Response:

```json
{
  "name": "Shriram"
}
```

**Invalid request:**

```text
GET /user/Ram
```

The custom exception `UserNotFoundException` is raised.

Without a registered exception handler, an unhandled custom exception results in an internal server error.

This leads to the next concept: Global Exception Handling.

---

## 5. Global Exception Handler

### What Is a Global Exception Handler?

A global exception handler is used to handle specific exceptions centrally across an application.

Instead of writing the same error-handling logic inside every endpoint, developers can register a single handler for a particular exception class.

FastAPI provides the `@app.exception_handler()` decorator for this purpose.

### Code Example

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


class UserNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.get("/user/{name}")
def get_user(name: str):
    if name != "Shriram":
        raise UserNotFoundException(name)

    return {
        "name": name
    }


@app.exception_handler(UserNotFoundException)
def user_not_found_handler(
    request: Request,
    exc: UserNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": f"User {exc.name} not found"
        }
    )
```

### Explanation

**A. Import Required Modules**

```python
from fastapi import Request
from fastapi.responses import JSONResponse
```

- `Request` provides access to information about the incoming HTTP request.
- `JSONResponse` is used to return a JSON response with a custom status code and response body.

**B. Register the Global Exception Handler**

```python
@app.exception_handler(UserNotFoundException)
```

This decorator registers a handler for the `UserNotFoundException` class.

Whenever this exception is raised during request processing, FastAPI invokes the registered handler.

**C. Handler Function**

```python
def user_not_found_handler(
    request: Request,
    exc: UserNotFoundException
):
```

The handler accepts two parameters:

- `request`: Represents the incoming HTTP request.
- `exc`: Contains the exception instance that was raised.

Since the exception object stores the username in `self.name`, the handler can access it using `exc.name`.

**D. Return a Custom JSON Response**

```python
return JSONResponse(
    status_code=404,
    content={
        "status": "error",
        "message": f"User {exc.name} not found"
    }
)
```

- `JSONResponse` creates a JSON-formatted HTTP response.
- `status_code=404` specifies the HTTP response status.
- `content` defines the response body.
- The username is dynamically included in the error message.

This allows the application to return a consistent error response whenever a user is not found.

### Example 1 – Successful Request

Request:

```text
GET /user/Shriram
```

Response:

```json
{
  "name": "Shriram"
}
```

HTTP Status Code: `200 OK`

### Example 2 – Custom Error Response

Request:

```text
GET /user/Ram
```

Response:

```json
{
  "status": "error",
  "message": "User Ram not found"
}
```

HTTP Status Code: `404 Not Found`

Unlike the previous custom exception example, the exception is now handled by the registered global exception handler.

---

## 6. Difference Between the Three Approaches

| Feature | HTTPException | Custom Exception | Global Exception Handler |
|---|---|---|---|
| Purpose | Raise standard HTTP errors | Define application-specific errors | Handle registered exceptions centrally |
| Definition | Provided by FastAPI | Created by developer | Registered using a decorator |
| Usage | `raise HTTPException()` | `raise UserNotFoundException()` | `@app.exception_handler()` |
| Response | Standard HTTP error response | No automatic custom response by itself | Custom response defined by the handler |
| Example | 400 Bad Request | User not found exception | 404 JSON error response |

## 7. Execution Flow of Global Exception Handling

Consider the request:

```text
GET /user/Ram
```

The following steps take place:

1. The client sends a request to `/user/Ram`.
2. FastAPI executes the `get_user()` endpoint.
3. The condition checks whether the username is `"Shriram"`.
4. Since the name is `"Ram"`, `UserNotFoundException` is raised.
5. FastAPI identifies the registered exception handler.
6. The `user_not_found_handler()` function is executed.
7. The handler generates a custom JSON response.
8. The client receives the response with HTTP status code `404`.

## 8. How to Run the Application

Open the terminal inside the `exception_handling` folder and execute:

```bash
python -m uvicorn main:app --reload
```

## 9. Testing Using Swagger UI

Open the interactive API documentation:

http://127.0.0.1:8000/docs

Test the following requests:

| Endpoint | Expected Result |
|---|---|
| `/user/Shriram` | 200 OK |
| `/user/Ram` | 404 Not Found |
| `/user/John` | 404 Not Found |

The active code in this tutorial uses the global exception handler. The earlier HTTPException and custom-exception-only examples are retained as commented learning examples.

## 10. Key Takeaways

- `HTTPException` is used to raise standard HTTP errors.
- Custom exceptions allow developers to define application-specific error conditions.
- Custom exception classes should inherit from Python's `Exception` class.
- The `raise` keyword is used to trigger an exception.
- `@app.exception_handler()` registers a centralized handler for a particular exception.
- `Request` provides information about the incoming request.
- `JSONResponse` allows developers to customize the HTTP status code and JSON response body.
- Global exception handlers help maintain consistent error responses across an application.

## 11. Concepts Covered

- HTTPException
- Custom exception classes
- Python exception inheritance
- Raising exceptions
- Global exception handling
- `@app.exception_handler()`
- Request objects
- JSONResponse
- Custom error messages
- HTTP 404 error handling

**Conclusion:** Exception handling helps FastAPI applications manage errors in a structured and predictable way. HTTPException handles standard HTTP errors, custom exceptions represent application-specific failures, and global exception handlers provide centralized control over how those failures are returned to clients.