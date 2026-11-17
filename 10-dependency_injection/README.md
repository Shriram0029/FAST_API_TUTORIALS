# FastAPI – Dependency Injection

## 1. Overview

Dependency Injection is a feature in FastAPI that allows developers to reuse common functionality across multiple API endpoints without repeatedly writing the same code.

FastAPI provides the `Depends()` function to declare and inject dependencies into endpoint functions.

Dependencies can be used for:

1. Reusing common logic across multiple endpoints.
2. Handling authentication and authorization.
3. Validating request information.
4. Sharing database connections.
5. Managing common operations such as logging and configuration.

This tutorial covers the basics of Dependency Injection, reusable logic, and a simple token-based authentication example.

## 2. Project Structure

```text
dependency_injection/
├── main.py
└── README.md
```

## 3. What Is Dependency Injection?

Dependency Injection is a programming technique in which a function or component receives the functionality it needs from an external source instead of creating or implementing that functionality itself.

In FastAPI, `Depends()` is used to declare a dependency.

FastAPI automatically executes the dependency function and provides its returned value to the endpoint.

### Basic Code Example

```python
from fastapi import FastAPI, Depends

app = FastAPI()

def common_logic():
    return {
        "message": "common logic executed"
    }

@app.get("/home")
def home(data=Depends(common_logic)):
    return data
```

### Explanation

**A. Creating a Dependency Function**

```python
def common_logic():
    return {
        "message": "common logic executed"
    }
```

- `common_logic()` is a normal Python function.
- It contains the common functionality that can be reused.
- It returns a dictionary containing a message.

**B. Injecting the Dependency**

```python
@app.get("/home")
def home(data=Depends(common_logic)):
    return data
```

The important part is:

```python
data=Depends(common_logic)
```

- `Depends()` tells FastAPI that `common_logic` is a dependency.
- FastAPI automatically calls the dependency function when processing the request.
- The returned value is assigned to the `data` parameter.
- The endpoint returns that data to the client.

The developer does not need to call `common_logic()` manually inside the endpoint.

### Example Request

```text
GET /home
```

### Example Response

```json
{
  "message": "common logic executed"
}
```

### Execution Flow

1. The client sends a request to `/home`.
2. FastAPI identifies the dependency declared using `Depends()`.
3. FastAPI executes `common_logic()`.
4. The dependency returns its dictionary.
5. The returned value is injected into the `data` parameter.
6. The endpoint returns the injected data.

## 4. Reusable Logic Using Dependency Injection

One of the major advantages of Dependency Injection is code reusability.

The same dependency function can be shared across multiple endpoints without duplicating its implementation.

### Code Example

```python
def get_current_user():
    return {
        "user": "Shriram"
    }

@app.get("/profile")
def profile(user=Depends(get_current_user)):
    return user

@app.get("/dashboard")
def dashboard(user=Depends(get_current_user)):
    return user
```

### Explanation

**A. Creating a Common Dependency**

```python
def get_current_user():
    return {
        "user": "Shriram"
    }
```

This function represents a common operation that provides the current user's information.

**B. Using the Dependency in the Profile Endpoint**

```python
@app.get("/profile")
def profile(user=Depends(get_current_user)):
    return user
```

- The `/profile` endpoint uses `get_current_user` as its dependency.
- FastAPI executes the dependency function.
- The returned user information is injected into the `user` parameter.
- The endpoint returns the user information.

**C. Reusing the Same Dependency in the Dashboard Endpoint**

```python
@app.get("/dashboard")
def dashboard(user=Depends(get_current_user)):
    return user
```

The same dependency is used again in another endpoint.

There is no need to rewrite the user retrieval logic.

### Example Requests

```text
GET /profile
GET /dashboard
```

### Example Response

Both endpoints return:

```json
{
  "user": "Shriram"
}
```

### Advantages of Reusable Dependencies

- Avoids code duplication.
- Makes application logic easier to maintain.
- Allows common functionality to be shared across endpoints.
- Makes testing and modifying common logic easier.
- Helps organize larger applications.

## 5. Token Handling Through Authentication

Dependency Injection is also useful for implementing authentication.

In this example, a dependency function verifies an incoming token before allowing access to a protected endpoint.

### Code Example

```python
from fastapi import FastAPI, Depends, Header, HTTPException

app = FastAPI()

def verify_token(token: str = Header(None)):
    if token != "mine":
        raise HTTPException(
            status_code=401,
            detail="UnAuthorized"
        )

    return {
        "user": "Authorized User"
    }

@app.get("/secure-data")
def secure_data(user=Depends(verify_token)):
    return {
        "message": "Secure Data accessed",
        "user": user
    }
```

### Explanation

**A. Header**

```python
token: str = Header(None)
```

- `Header()` tells FastAPI to extract the value from an HTTP request header.
- The parameter is named `token`, so FastAPI looks for the `token` header.
- `None` is the default value if the header is not provided.

For example:

```text
token: mine
```

**B. Creating the Token Verification Dependency**

```python
def verify_token(token: str = Header(None)):
```

This function checks whether the client provides the expected token.

**C. Validating the Token**

```python
if token != "mine":
    raise HTTPException(
        status_code=401,
        detail="UnAuthorized"
    )
```

- The condition checks whether the received token matches `"mine"`.
- If the token does not match, an `HTTPException` is raised.
- `status_code=401` indicates that the request is unauthorized.
- `detail` provides the error message.

**D. Returning Authorized User Information**

```python
return {
    "user": "Authorized User"
}
```

If the token matches, the dependency returns the authorized user's information.

**E. Injecting the Authentication Dependency**

```python
@app.get("/secure-data")
def secure_data(user=Depends(verify_token)):
```

- The `/secure-data` endpoint uses `verify_token` as a dependency.
- FastAPI automatically executes the token verification function.
- If verification fails, the request is stopped and an error response is returned.
- If verification succeeds, the returned user information is injected into the `user` parameter.

The endpoint then returns:

```python
return {
    "message": "Secure Data accessed",
    "user": user
}
```

## 6. Testing Token Authentication

### Endpoint

```text
GET /secure-data
```

This endpoint expects a token in the request header.

### Case 1 – Valid Token

Request header:

```text
token: mine
```

Example response:

```json
{
  "message": "Secure Data accessed",
  "user": {
    "user": "Authorized User"
  }
}
```

HTTP Status Code: `200 OK`

### Case 2 – Invalid Token

Request header:

```text
token: wrong
```

Example response:

```json
{
  "detail": "UnAuthorized"
}
```

HTTP Status Code: `401 Unauthorized`

### Case 3 – Missing Token

If the client does not provide the token header, FastAPI uses the default value `None`.

Since `None` does not match `"mine"`, the dependency raises the same HTTP exception.

Example response:

```json
{
  "detail": "UnAuthorized"
}
```

HTTP Status Code: `401 Unauthorized`

## 7. Understanding the Execution Flow

For the `/secure-data` endpoint, the execution takes place in the following order:

1. The client sends a request to `/secure-data`.
2. The request includes a token in the HTTP header.
3. FastAPI identifies `verify_token` as a dependency.
4. FastAPI executes `verify_token`.
5. The dependency checks whether the token is valid.
6. If invalid, an HTTP 401 error is raised.
7. If valid, the dependency returns the authorized user information.
8. FastAPI injects the returned value into the `user` parameter.
9. The endpoint returns the secure data.

## 8. How to Run the Application

Open the terminal inside the `dependency_injection` folder and execute:

```bash
python -m uvicorn main:app --reload
```

Alternatively, run the appropriate module path from the parent directory.

## 9. Testing Using Swagger UI

Open the automatically generated API documentation:

http://127.0.0.1:8000/docs

### Test the Basic Dependency

1. Find `GET /home`.
2. Click **Try it out**.
3. Click **Execute**.
4. Observe the common logic response.

### Test Reusable Dependencies

1. Test `GET /profile`.
2. Test `GET /dashboard`.
3. Observe that both endpoints return the same user information.

### Test Token Authentication

1. Find `GET /secure-data`.
2. Click **Try it out**.
3. Open the header parameter named `token`.
4. Enter `mine`.
5. Click **Execute**.
6. Observe the successful response.
7. Try `wrong` and execute again.
8. Observe the `401 Unauthorized` response.

## 10. Difference Between Normal Function Calls and Dependency Injection

| Normal Function Call | Dependency Injection |
|---|---|
| Function is called manually | FastAPI manages dependency execution |
| Developer handles the returned value | FastAPI injects the returned value |
| Reuse requires explicit function calls | Dependencies can be declared across multiple endpoints |
| Dependency management is manual | Dependency management is handled by FastAPI |

For example:

Normal function call:

```python
data = common_logic()
```

Dependency Injection:

```python
def home(data=Depends(common_logic)):
    return data
```

## 11. Key Takeaways

- Dependency Injection allows common functionality to be reused across endpoints.
- `Depends()` is the main function used to declare dependencies in FastAPI.
- FastAPI automatically executes the dependency function.
- The returned value of a dependency is injected into the endpoint parameter.
- A single dependency can be shared by multiple endpoints.
- Dependencies can be used for authentication and token verification.
- `Header()` extracts information from HTTP request headers.
- `HTTPException` can be raised inside a dependency to stop unauthorized requests.
- Dependency Injection helps reduce code duplication and improve maintainability.

## 12. Concepts Covered

- Dependency Injection
- `Depends()`
- Common dependency functions
- Reusable application logic
- Dependency execution
- HTTP headers
- Token verification
- Authentication basics
- HTTP 401 Unauthorized
- Dependency injection in multiple endpoints

**Conclusion:** Dependency Injection is an important FastAPI feature that helps developers organize and reuse application logic. It is particularly useful for common operations such as authentication, authorization, database connections, and request validation.