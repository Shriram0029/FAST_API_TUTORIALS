# FastAPI – Status Codes, Custom Responses, and Error Handling

## 1. Overview

This tutorial covers three important concepts in FastAPI:

1. **HTTP Status Codes** – Indicate the result of an API request.
2. **Custom Responses** – Return structured JSON responses containing status messages and data.
3. **Error Handling** – Handle errors and return appropriate HTTP error responses using `HTTPException`.

These concepts help build APIs that communicate clearly with clients and handle successful requests as well as failures.

## 2. Project Structure

```text
status-codes_response/
├── main.py
└── README.md
```

## 3. HTTP Status Codes

### What Are HTTP Status Codes?

HTTP status codes are three-digit numbers returned by a server to indicate the result of a client's request.

They help the client understand whether a request was successful, whether additional action is required, or whether an error occurred.

### Common HTTP Status Code Categories

| Category | Range | Description |
|---|---|---|
| Informational | 100–199 | Request processing information |
| Success | 200–299 | Request completed successfully |
| Redirection | 300–399 | Further action or redirection required |
| Client Errors | 400–499 | Problem with the client request |
| Server Errors | 500–599 | Server encountered an error |

### Commonly Used Status Codes

| Status Code | Meaning | Description |
|---|---|---|
| 200 | OK | Request completed successfully |
| 201 | Created | A new resource was successfully created |
| 204 | No Content | Request succeeded without returning a response body |
| 400 | Bad Request | Invalid request from the client |
| 401 | Unauthorized | Authentication is required or invalid |
| 403 | Forbidden | Client does not have permission |
| 404 | Not Found | Requested resource does not exist |
| 422 | Unprocessable Entity | Request data failed validation |
| 500 | Internal Server Error | Unexpected server-side error |

### Code Example

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user():
    return {
        "message": "User Created"
    }
```

### Explanation

- `status` is imported from FastAPI to access predefined HTTP status codes.
- `@app.post("/create_user")` defines a POST endpoint.
- `status_code=status.HTTP_201_CREATED` specifies that the endpoint should return HTTP status code `201`.
- The function returns a JSON response containing a success message.

### Example Request

```text
POST /create_user
```

### Example Response

```json
{
  "message": "User Created"
}
```

**Response Status Code:**

```text
201 Created
```

By default, a successful POST request generally returns `200 OK`. By specifying `status_code=status.HTTP_201_CREATED`, the response explicitly indicates that a resource has been created.

## 4. Custom Responses

### What Are Custom Responses?

Custom responses allow developers to structure the data returned by an API according to application requirements.

Instead of returning only a single value, an API can return multiple fields such as:

- Status
- Message
- Data

This makes API responses more organized and easier for clients to understand.

### Code Example

```python
@app.get("/user")
def get_user():
    return {
        "status": "success",
        "message": "User Fetched",
        "data": {
            "name": "Shriram",
            "age": 24
        }
    }
```

### Explanation

- `@app.get("/user")` defines a GET endpoint.
- The function returns a dictionary containing three main fields.
- `status` indicates whether the operation was successful.
- `message` provides information about the operation.
- `data` contains the actual user information.

FastAPI automatically converts the returned Python dictionary into a JSON response.

### Example Request

```text
GET /user
```

### Example Response

```json
{
  "status": "success",
  "message": "User Fetched",
  "data": {
    "name": "Shriram",
    "age": 24
  }
}
```

This is an example of a structured custom JSON response.

**Important:** The `status` field in this example is simply a JSON field containing the string `"success"`. It is different from the actual HTTP status code, which is `200 OK` by default.

## 5. Basic Error Handling

### What Is Error Handling?

Error handling is the process of identifying and managing errors that occur while processing API requests.

In FastAPI, `HTTPException` is used to stop normal request processing and return an appropriate HTTP error response.

It allows developers to specify:

- HTTP status code
- Error details
- Optional response headers

### Code Example

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
def get_users(user_id: int):
    if user_id != 1:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )

    return {
        "data": user_id,
        "name": "Shriram"
    }
```

### Explanation

**A. Path Parameter**

```python
@app.get("/users/{user_id}")
def get_users(user_id: int):
```

- `{user_id}` is a path parameter.
- `user_id: int` specifies that the parameter must be an integer.
- The value is extracted directly from the URL.

**B. Conditional Check**

```python
if user_id != 1:
```

The condition checks whether the requested user ID is different from `1`.

In this example, only user ID `1` is considered valid.

**C. Raising HTTPException**

```python
raise HTTPException(
    status_code=404,
    detail="User Not Found"
)
```

- `HTTPException` is imported from FastAPI.
- `status_code=404` specifies the HTTP status code.
- `detail` provides the error message.
- `raise` immediately stops the normal execution of the endpoint and returns the error response.

**D. Successful Response**

```python
return {
    "data": user_id,
    "name": "Shriram"
}
```

If the requested user ID is `1`, the condition is false, and the function returns the user information.

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

HTTP Status Code:

```text
200 OK
```

### Example 2 – User Not Found

Request:

```text
GET /users/2
```

Response:

```json
{
  "detail": "User Not Found"
}
```

HTTP Status Code:

```text
404 Not Found
```

The error response is automatically generated by FastAPI when `HTTPException` is raised.

## 6. How to Run the Application

Open the terminal inside the `status-codes_response` folder and execute:

```bash
python -m uvicorn main:app --reload
```

Alternatively, run it from the parent project directory using:

```bash
python -m uvicorn status-codes_response.main:app --reload
```

For the second command, if the folder name contains a hyphen, Python module imports may not work as expected. In that case, use the first command from inside the folder.

## 7. Testing Using Swagger UI

Open the automatically generated API documentation:

http://127.0.0.1:8000/docs

Test the following endpoints:

| Method | Endpoint | Expected Result |
|---|---|---|
| POST | `/create_user` | 201 Created |
| GET | `/user` | 200 OK with custom JSON response |
| GET | `/users/1` | 200 OK with user data |
| GET | `/users/2` | 404 Not Found |

Try different user IDs to observe how the error handling works.

## 8. Important Differences

| Concept | Purpose | FastAPI Feature |
|---|---|---|
| HTTP Status Codes | Indicate request outcome | `status` |
| Custom Responses | Structure returned JSON data | Python dictionaries |
| Error Handling | Handle unsuccessful requests | `HTTPException` |

### Difference Between HTTP Status and JSON Status

Consider this response:

```json
{
  "status": "success",
  "message": "User Fetched"
}
```

Here, `"status": "success"` is part of the JSON response body.

The actual HTTP status code is separately communicated by the server, such as `200 OK`.

Both serve different purposes.

## 9. Key Takeaways

- HTTP status codes communicate the result of an API request.
- The `status` module provides predefined HTTP status code constants.
- The `status_code` parameter specifies the HTTP status code returned by an endpoint.
- Custom responses help organize API output using fields such as status, message, and data.
- FastAPI automatically converts returned dictionaries into JSON responses.
- `HTTPException` is used to raise HTTP errors.
- The `detail` parameter specifies the error message.
- Raising an exception immediately stops normal endpoint execution.

## 10. Concepts Covered

- HTTP status codes and categories
- Successful response codes
- `status` module
- Custom JSON responses
- `HTTPException`
- Basic error handling
- Path parameters in error handling
- Swagger UI testing

**Conclusion:** HTTP status codes, custom responses, and error handling are essential for building reliable APIs. They help communicate successful operations clearly and handle errors in a consistent manner.