# FastAPI – Middleware

## 1. Overview

Middleware is a mechanism in FastAPI that allows developers to execute code before and after an HTTP request is processed by an API endpoint.

It acts as an intermediate layer between the client and the application.

Middleware can be used for:

1. Logging incoming requests and outgoing responses.
2. Measuring API execution time.
3. Handling authentication and security-related operations.
4. Adding or modifying HTTP headers.
5. Monitoring application activity.
6. Performing common operations for every request.

In this tutorial, we explore basic middleware implementation and logging middleware using FastAPI.

## 2. Project Structure

```text
middleware/
├── main.py
└── README.md
```

## 3. What Is Middleware?

Middleware is a function that executes during the request-response cycle of an application.

Whenever a client sends an HTTP request, middleware gets an opportunity to execute code before the request reaches the actual API endpoint.

After the endpoint processes the request and generates a response, middleware can execute additional code before the response is sent back to the client.

In simple terms, middleware allows developers to perform common operations around API endpoint execution without writing the same logic inside every endpoint.

### Understanding the Request-Response Cycle

Consider a client sending a request to a FastAPI application.

The request passes through middleware before reaching the endpoint. After the endpoint generates a response, the response passes back through the middleware before reaching the client.

The general execution flow is:

1. Client sends an HTTP request.
2. Middleware receives the request.
3. Middleware executes its pre-processing logic.
4. Request reaches the API endpoint.
5. Endpoint executes its business logic.
6. Endpoint generates an HTTP response.
7. Middleware executes its post-processing logic.
8. Response is returned to the client.

### Simple Representation

```text
        CLIENT
           |
           | HTTP Request
           |
           v
    +--------------+
    |  MIDDLEWARE  |
    |              |
    | Before Logic |
    +--------------+
           |
           v
    +--------------+
    | API ENDPOINT |
    |              |
    | Business     |
    | Logic        |
    +--------------+
           |
           | HTTP Response
           |
           v
    +--------------+
    |  MIDDLEWARE  |
    |              |
    | After Logic  |
    +--------------+
           |
           v
         CLIENT
```

Middleware provides a centralized way to execute common functionality for multiple endpoints.

---

## 4. Simple Middleware

### Code Example

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def my_middleware(request: Request, call_next):
    print("request received")

    response = await call_next(request)

    print("response sent")

    return response
```

### Explanation

Let's understand every new term and function used in this code.

### A. Importing FastAPI and Request

```python
from fastapi import FastAPI, Request
```

**FastAPI**

- `FastAPI` is used to create the API application.
- It provides functionality for defining routes, handling requests, and generating responses.

**Request**

- `Request` is a class provided by Starlette and made available through FastAPI.
- It represents the incoming HTTP request.
- It provides access to request information such as URL, HTTP method, headers, query parameters, and other request details.

For example, if the client requests:

```text
GET /users/1
```

The `request` object allows middleware to access information about that request.

### B. Creating the FastAPI Application

```python
app = FastAPI()
```

This creates the FastAPI application instance.

The middleware will be registered with this application using the `app` object.

### C. Understanding the Middleware Decorator

```python
@app.middleware("http")
```

This is a decorator provided by FastAPI for registering HTTP middleware.

A decorator is a Python feature that modifies or extends the behavior of a function.

Here:

- `app.middleware()` registers middleware with the FastAPI application.
- `"http"` specifies that this middleware handles HTTP requests.
- The function immediately below this decorator becomes the middleware function.

The middleware will execute for incoming HTTP requests handled by this application.

### D. Understanding async

```python
async def my_middleware(request: Request, call_next):
```

Here, `async` is a Python keyword used to define an asynchronous function.

An asynchronous function allows Python to perform other work while waiting for certain operations to complete.

In web applications, operations such as database queries, network communication, and HTTP request processing may involve waiting.

Asynchronous programming helps handle such waiting operations efficiently.

**Difference between normal and asynchronous functions:**

Normal function:

```python
def my_function():
    return "Hello"
```

Asynchronous function:

```python
async def my_function():
    return "Hello"
```

The `async` keyword defines a coroutine function, which can use `await` to wait for asynchronous operations.

In FastAPI middleware, the asynchronous form is commonly used because the middleware needs to wait for the next request-processing stage.

### E. Understanding the Parameters

```python
async def my_middleware(request: Request, call_next):
```

This function accepts two important parameters.

**1. request**

- Contains information about the incoming HTTP request.
- Allows middleware to inspect the request.
- Can be used to access the URL, path, headers, and HTTP method.

**2. call_next**

- Represents the next stage in the middleware request-processing chain.
- Calling it passes the request forward through the remaining middleware and eventually to the API endpoint.
- It returns the response generated by the application.

In simple terms, `call_next()` allows middleware to pass control to the next processing stage.

### F. Executing Logic Before the Endpoint

```python
print("request received")
```

This statement executes before the request reaches the endpoint.

Whenever a request arrives, the message is printed in the terminal.

This is an example of pre-processing logic.

### G. Understanding await

```python
response = await call_next(request)
```

This is one of the most important statements in middleware.

Let's break it down.

**call_next(request)**

- Passes the incoming request to the next processing stage.
- Allows the API endpoint to execute.
- Eventually produces an HTTP response.

**await**

- Waits for the asynchronous operation to complete.
- Allows the middleware to receive the response generated by the application.

**response**

- Stores the response returned by the next processing stage.
- Contains the HTTP response that will be sent to the client.

Without waiting for `call_next(request)` to complete, the middleware cannot perform its post-response logic using the resulting response.

### H. Executing Logic After the Endpoint

```python
print("response sent")
```

This statement executes after the endpoint has processed the request and the response has been obtained.

It represents post-processing logic.

### I. Returning the Response

```python
return response
```

This returns the response to the client through the middleware stack.

Returning the response is important because middleware should pass the generated response back rather than discard it.

### Example Terminal Output

When a client sends a request, the terminal displays:

```text
request received
response sent
```

This demonstrates that middleware executes before and after the endpoint processing.

---

## 5. Logging Middleware

### What Is Logging?

Logging is the process of recording information about an application's execution.

It helps developers understand what is happening inside an application and makes debugging and monitoring easier.

For example, logging can record:

- Which API endpoint was requested.
- When a request was received.
- How much time an API request took.
- Whether an operation was successful.
- Errors that occurred during execution.

In FastAPI, logging middleware can be used to record information about incoming requests and their processing time.

### Code Example

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def my_middleware_logging(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    print(f"Path : {request.url.path} | Time: {process_time}")

    return response
```

This is the active implementation in the tutorial.

### Explanation

**A. Importing the Time Module**

```python
import time
```

`time` is a built-in Python module that provides functions related to time.

It contains several functions for obtaining the current time, measuring elapsed time, and performing time-related operations.

In this example, we use `time.time()` to calculate how long a request takes.

**B. Recording the Starting Time**

```python
start_time = time.time()
```

`time.time()` returns the current time as a floating-point number representing seconds since the Unix epoch.

The Unix epoch is the reference point of January 1, 1970, at 00:00:00 UTC.

Here, the current timestamp is stored in the variable `start_time`.

This records when the middleware begins processing the request.

**C. Processing the Request**

```python
response = await call_next(request)
```

This statement passes the request to the next processing stage.

The API endpoint executes, processes the request, and generates a response.

The middleware waits until the response is available.

**D. Calculating Processing Time**

```python
process_time = time.time() - start_time
```

This calculates the total elapsed time between the start of request processing and the completion of the next processing stage.

The calculation is:

\[
\text{Processing Time} =
\text{End Time} - \text{Start Time}
\]

For example:

| Operation | Time |
|---|---:|
| Start time | 100.00 seconds |
| End time | 100.25 seconds |
| Processing time | 0.25 seconds |

Therefore, the request took approximately 0.25 seconds.

**Important:** The actual values returned by `time.time()` are timestamps. Subtracting the starting timestamp from the ending timestamp gives the elapsed duration in seconds.

**E. Accessing the Request Path**

```python
request.url.path
```

The `request` object contains information about the incoming HTTP request.

`request.url.path` retrieves the path portion of the requested URL.

For example:

| Requested URL | `request.url.path` |
|---|---|
| `http://127.0.0.1:8000/` | `/` |
| `http://127.0.0.1:8000/users` | `/users` |
| `http://127.0.0.1:8000/profile` | `/profile` |
| `http://127.0.0.1:8000/items/10` | `/items/10` |

It does not include the domain, port, or query string.

**F. Printing the Log Information**

```python
print(f"Path : {request.url.path} | Time: {process_time}")
```

This uses a Python f-string to insert variable values into a string.

It prints:

- The requested API path.
- The time taken to process the request.

Example terminal output:

```text
Path : /users | Time: 0.0021
Path : /profile | Time: 0.0018
Path : /items/10 | Time: 0.0034
```

The numbers above are illustrative; actual processing times depend on the application and system.

**G. Returning the Response**

```python
return response
```

After recording the processing information, the middleware returns the original response to the client.

---

## 6. Understanding the Complete Logging Middleware Flow

Consider a client requesting:

```text
GET /users
```

The following operations take place:

**Step 1 – Request Arrives**

The client sends an HTTP request to the FastAPI application.

**Step 2 – Middleware Starts**

The middleware function executes before the API endpoint.

**Step 3 – Start Time Is Recorded**

```python
start_time = time.time()
```

The current timestamp is stored.

**Step 4 – Request Is Passed Forward**

```python
response = await call_next(request)
```

The request continues through the remaining middleware and reaches the API endpoint.

**Step 5 – Endpoint Executes**

The endpoint performs its business logic and generates the response.

**Step 6 – Processing Time Is Calculated**

```python
process_time = time.time() - start_time
```

The elapsed time is calculated.

**Step 7 – Request Information Is Logged**

```python
print(f"Path : {request.url.path} | Time: {process_time}")
```

The requested path and processing duration are printed.

**Step 8 – Response Is Returned**

```python
return response
```

The response is passed back to the client.

### Execution Flow

```text
          CLIENT
             |
             | HTTP Request
             v
    +---------------------+
    |  LOGGING MIDDLEWARE |
    +---------------------+
             |
             v
    Record Start Time
             |
             v
    await call_next(request)
             |
             v
       API ENDPOINT
             |
             v
    Execute Business Logic
             |
             v
      Generate Response
             |
             v
    +---------------------+
    |  LOGGING MIDDLEWARE |
    +---------------------+
             |
             v
    Calculate Processing Time
             |
             v
       Print Log Details
             |
             v
       Return Response
             |
             v
           CLIENT
```

---

## 7. Important Python Concepts Used in Middleware

The following concepts are particularly important for understanding middleware.

### A. Decorators

A decorator is a Python feature that allows additional functionality to be applied to a function without directly modifying its implementation.

Example:

```python
@app.middleware("http")
async def my_middleware(request: Request, call_next):
    pass
```

The decorator registers the function as HTTP middleware.

### B. Asynchronous Programming

Asynchronous programming allows a program to handle operations that involve waiting without blocking the entire execution flow.

Python uses the `async` and `await` keywords to support asynchronous programming.

Example:

```python
async def my_function():
    result = await some_async_operation()
```

- `async` defines an asynchronous function.
- `await` waits for an asynchronous operation to complete.

### C. Request Object

The `Request` object provides access to information about an incoming HTTP request.

Some commonly used properties include:

| Property | Purpose |
|---|---|
| `request.url` | Retrieves the complete request URL |
| `request.url.path` | Retrieves the URL path |
| `request.method` | Retrieves the HTTP method |
| `request.headers` | Accesses request headers |
| `request.query_params` | Accesses query parameters |

### D. Response Object

The response object represents the HTTP response generated by the application.

It can contain:

- Response body.
- HTTP status code.
- Response headers.

In this tutorial, the response is received through:

```python
response = await call_next(request)
```

It is then returned using:

```python
return response
```

### E. Time Measurement

The `time` module is used to calculate elapsed time.

```python
start_time = time.time()

# Some operation

process_time = time.time() - start_time
```

This technique can be used to measure the duration of operations in Python applications.

For more precise duration measurement, Python also provides `time.perf_counter()`, which is generally preferred for measuring elapsed time.

---

## 8. Difference Between Simple Middleware and Logging Middleware

| Simple Middleware | Logging Middleware |
|---|---|
| Demonstrates basic middleware execution | Records request information and processing time |
| Prints request received | Records the starting timestamp |
| Passes request using `call_next()` | Passes request using `call_next()` |
| Prints response sent | Calculates elapsed time |
| Returns the response | Logs path and processing time, then returns the response |

Both examples use the same middleware mechanism. The difference is the additional functionality implemented inside the middleware function.

---

## 9. How to Run the Application

Open the terminal inside the `middleware` folder and execute:

```bash
python -m uvicorn main:app --reload
```

The `--reload` option automatically restarts the development server when code changes are detected.

Open the following URL:

http://127.0.0.1:8000/docs

Use the Swagger UI to test the API endpoints.

You can also open the root URL:

http://127.0.0.1:8000/

The middleware executes for HTTP requests even if no explicit root endpoint has been defined. In that case, FastAPI returns a `404 Not Found` response, but the middleware can still record the request.

---

## 10. Important Points to Remember

1. Middleware is executed around the request-response cycle.
2. Middleware can perform operations before and after endpoint execution.
3. `@app.middleware("http")` registers HTTP middleware.
4. `Request` provides information about incoming requests.
5. `call_next(request)` passes the request to the next processing stage.
6. `await` waits for the asynchronous operation to complete.
7. The returned response can be inspected or modified before being returned.
8. `time.time()` provides the current timestamp.
9. Subtracting timestamps calculates elapsed processing time.
10. `request.url.path` retrieves the requested URL path.
11. Middleware can be used for logging, monitoring, authentication, and other common operations.

## 11. Important Practical Notes

- Middleware is generally executed for every HTTP request handled by the application.
- If multiple middleware functions are registered, they form a processing chain.
- Middleware should return a response so that the request-response cycle can complete.
- The processing time in this example measures the time spent waiting for the downstream application to produce a response. It does not include all subsequent response transmission time to the client.
- The current implementation uses `print()` for demonstration. Real applications generally use Python's `logging` module for structured and configurable logs.
- If an unhandled exception occurs inside the downstream application, `call_next()` may raise an exception instead of returning a normal response. The current example does not include separate exception logging.

## 12. Concepts Covered

- Middleware
- Request-response lifecycle
- HTTP middleware
- Middleware decorator
- Asynchronous functions
- `async` and `await`
- Request object
- Response object
- `call_next()`
- Logging middleware
- Python time module
- Request processing time
- URL path extraction
- Pre-processing and post-processing

**Conclusion:** Middleware is an important part of FastAPI that allows developers to execute common operations around API request processing. Logging middleware makes it possible to monitor incoming requests and measure how long the application takes to generate responses, helping developers understand and maintain API performance.