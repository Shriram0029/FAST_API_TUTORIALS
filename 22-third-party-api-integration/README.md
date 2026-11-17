# Third-Party API Integration Using FastAPI

## 1. Introduction

In backend development, applications often need information from external services. Instead of building and maintaining every functionality ourselves, we can communicate with existing APIs provided by third-party services.

This process is called **Third-Party API Integration**.

In this tutorial, we learn how to:
- Understand external APIs.
- Install and use the Python Requests library.
- Make basic API calls.
- Fetch all records from an external API.
- Fetch a specific record using its ID.
- Integrate external APIs with FastAPI.
- Handle errors while communicating with external APIs.

We use **JSONPlaceholder**, a free fake REST API, to understand these concepts.

### Project Structure

```text
22-third-party-api-integration/
│
├── main.py
└── README.md
```

---

## 2. What is an External API?

### What is an API?

API stands for **Application Programming Interface**.

An API allows two software applications to communicate with each other.

For example, consider an application that displays weather information.

The application itself may not collect weather information. Instead, it communicates with an external weather service through an API and retrieves the required information.

Similarly, applications can use external APIs to access:
- Weather information.
- Payment services.
- Maps and location information.
- User information.
- Product details.
- News and other external data.

### What is an External API?

An external API is an API provided by another application or service that our application can communicate with.

For example:

Consider an e-commerce application that needs payment functionality.

Instead of building an entire payment processing system, the application can integrate with an external payment provider through its API.

The external service processes the payment request and sends the response back to our application.

### Understanding the Communication

The general communication process is:

1. Our application sends an HTTP request to an external API.
2. The external API receives and processes the request.
3. The external service retrieves or processes the required information.
4. It sends an HTTP response back.
5. Our application reads and uses the returned data.

### What is JSONPlaceholder?

JSONPlaceholder is a free fake REST API used for testing and learning API integration.

Website:

https://jsonplaceholder.typicode.com/

It provides sample resources such as:
- Posts
- Comments
- Albums
- Photos
- Todos
- Users

For this tutorial, we use the Posts resource.

All posts:

```text
https://jsonplaceholder.typicode.com/posts
```

A specific post:

```text
https://jsonplaceholder.typicode.com/posts/2
```

Example response:

```json
{
    "userId": 1,
    "id": 2,
    "title": "Example post title",
    "body": "Example post body"
}
```

The API returns data in JSON format.

---

## 3. Installing Requests

### What is the Requests Library?

Requests is a Python library used to send HTTP requests to external servers and APIs.

It provides simple methods to communicate with APIs using HTTP methods such as:

- GET – Retrieve information.
- POST – Send information.
- PUT – Update information.
- PATCH – Partially update information.
- DELETE – Delete information.

For this tutorial, we mainly use the GET method to retrieve data.

### Installation

Install Requests using:

```bash
python -m pip install requests
```

Verify the installation:

```bash
python -m pip show requests
```

Import the library:

```python
import requests
```

Now we can use Requests to communicate with external APIs.

---

## 4. Basic API Call

Before integrating an external API with FastAPI, we first understand how to call an external API directly using Python.

### Code

```python
import requests

# Simple API call
response = requests.get(
    "https://jsonplaceholder.typicode.com/posts"
)

data = response.json()

print(data)
print(data[:2])

# Simple API call by ID
response = requests.get(
    "https://jsonplaceholder.typicode.com/posts/2"
)

data = response.json()

print(data)
```

### Explanation

**1. Importing Requests**

```python
import requests
```

Imports the Requests library, which allows Python to communicate with external APIs.

**2. Sending a GET request**

```python
response = requests.get(
    "https://jsonplaceholder.typicode.com/posts"
)
```

The `requests.get()` method sends an HTTP GET request to the specified URL.

Here, we are requesting all posts available from JSONPlaceholder.

The returned HTTP response is stored in the `response` variable.

**3. Converting the response into JSON**

```python
data = response.json()
```

The external API returns data in JSON format.

The `.json()` method parses the JSON response and converts it into corresponding Python objects.

For example:

- JSON object becomes a Python dictionary.
- JSON array becomes a Python list.
- JSON string becomes a Python string.
- JSON number becomes a Python number.

In this example, the API returns a list of posts, so `data` contains a Python list of dictionaries.

**4. Printing all the data**

```python
print(data)
```

Displays all the posts received from the external API.

**5. Printing the first two records**

```python
print(data[:2])
```

This uses Python list slicing.

`data[:2]` retrieves the first two elements from the list.

It is useful when we want to inspect only a small portion of a large API response.

---

## 5. Single Data Fetch

Sometimes, we do not need all the records from an external API.

Instead, we may need only one particular record.

For example, if we want to retrieve the post whose ID is 2, we can directly request that resource.

### Code

```python
response = requests.get(
    "https://jsonplaceholder.typicode.com/posts/2"
)

data = response.json()

print(data)
```

### Explanation

**1. Sending a request using the ID**

```python
requests.get(
    "https://jsonplaceholder.typicode.com/posts/2"
)
```

Here, `/2` represents the ID of the post we want to retrieve.

Instead of fetching all posts, the external API returns only the record with ID 2.

**2. Converting the response**

```python
data = response.json()
```

Converts the JSON response into a Python dictionary.

**3. Displaying the result**

```python
print(data)
```

Displays the individual post.

### Difference Between Fetching All Data and Single Data

| Fetching all data | Single data fetch |
|---|---|
| `/posts` | `/posts/2` |
| Retrieves all posts | Retrieves one specific post |
| Returns a list of dictionaries | Returns a dictionary |
| Useful when multiple records are required | Useful when one particular record is required |

---

## 6. FastAPI Integration

Now that we understand how to communicate with an external API using Requests, we can integrate the same functionality into our FastAPI application.

Instead of directly printing the external API response in Python, we expose our own FastAPI endpoints that retrieve and return the external data.

### Complete main.py Code

```python
from fastapi import FastAPI
import requests
from fastapi import HTTPException

app = FastAPI()

# Get all data
@app.get("/posts")
def get_posts():
    url = "https://jsonplaceholder.typicode.com/posts"

    response = requests.get(url)

    data = response.json()

    return data


# Get data by ID
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"

    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    data = response.json()

    return data
```

### 6.1 Importing Required Libraries

```python
from fastapi import FastAPI
import requests
from fastapi import HTTPException
```

- `FastAPI`: Creates the backend application.
- `requests`: Communicates with the external API.
- `HTTPException`: Raises HTTP errors when a request cannot be handled as expected.

### 6.2 Creating the FastAPI Application

```python
app = FastAPI()
```

Creates the FastAPI application instance.

We use this instance to define our API endpoints.

### 6.3 Get All Posts

```python
@app.get("/posts")
def get_posts():
    url = "https://jsonplaceholder.typicode.com/posts"

    response = requests.get(url)

    data = response.json()

    return data
```

This endpoint retrieves all posts from JSONPlaceholder.

**Understanding the execution:**

1. A client sends a GET request to our FastAPI endpoint.
2. FastAPI executes the `get_posts()` function.
3. The external API URL is stored in the `url` variable.
4. `requests.get(url)` sends a GET request to JSONPlaceholder.
5. The external API returns its response.
6. `response.json()` converts the response into Python data.
7. FastAPI returns the retrieved data to the client as JSON.

Our endpoint:

```text
GET http://127.0.0.1:8000/posts
```

The endpoint acts as an intermediary between the client and the external API.

### 6.4 Get a Specific Post by ID

```python
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"

    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    data = response.json()

    return data
```

This endpoint retrieves a specific post using its ID.

**1. Understanding the path parameter**

```python
@app.get("/posts/{post_id}")
```

`post_id` is a path parameter.

The client provides the post ID as part of the URL.

For example:

```text
/posts/2
```

Here, `2` is the post ID.

**2. Receiving the post ID**

```python
def get_post(post_id: int):
```

FastAPI extracts the ID from the URL and passes it to the function.

The type hint `int` indicates that the ID should be an integer.

**3. Creating the external API URL**

```python
url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
```

An f-string is used to dynamically insert the requested ID into the external API URL.

For example, if `post_id = 2`, the resulting URL becomes:

```text
https://jsonplaceholder.typicode.com/posts/2
```

**4. Sending the external API request**

```python
response = requests.get(url)
```

Sends a GET request to JSONPlaceholder to retrieve the requested post.

**5. Checking the status code**

```python
if response.status_code != 200:
```

The `status_code` property contains the HTTP status code returned by the external API.

Here, we check whether the external API returned status code 200.

- 200 – Request successful.
- 404 – Requested resource not found.
- Other status codes may indicate other errors.

**6. Raising an HTTPException**

```python
raise HTTPException(
    status_code=404,
    detail="Post not found"
)
```

If the external API does not return status code 200, our FastAPI endpoint raises an HTTP 404 error.

The client receives a response similar to:

```json
{
    "detail": "Post not found"
}
```

**7. Returning the requested data**

```python
data = response.json()

return data
```

If the external API returns status code 200, the response is converted into Python data and returned to the client.

---

## 7. Testing the FastAPI Endpoints

### Step 1: Install the dependencies

```bash
python -m pip install fastapi uvicorn requests
```

### Step 2: Start the FastAPI server

```bash
python -m uvicorn main:app --reload
```

The application runs at:

```text
http://127.0.0.1:8000
```

### Step 3: Open Swagger UI

Navigate to:

```text
http://127.0.0.1:8000/docs
```

FastAPI provides an interactive Swagger UI where we can test our endpoints.

### Step 4: Test Get All Posts

Select:

```text
GET /posts
```

Click **Try it out**, followed by **Execute**.

Expected result:

The endpoint returns a list of posts retrieved from JSONPlaceholder.

### Step 5: Test Get Post by ID

Select:

```text
GET /posts/{post_id}
```

Enter:

```text
2
```

Click **Execute**.

Expected response:

```json
{
    "userId": 1,
    "id": 2,
    "title": "Example post title",
    "body": "Example post body"
}
```

The actual title and body are supplied by JSONPlaceholder.

### Step 6: Test an Invalid ID

Enter a post ID such as:

```text
9999
```

JSONPlaceholder returns a 404 response for a post that does not exist.

Our FastAPI application then raises:

```json
{
    "detail": "Post not found"
}
```

---

## 8. Important Concepts to Remember

| Concept | Purpose |
|---|---|
| External API | API provided by another application or service |
| Requests | Python library for sending HTTP requests |
| `requests.get()` | Sends an HTTP GET request |
| `response` | Stores the HTTP response object |
| `response.json()` | Converts JSON response data into Python objects |
| JSONPlaceholder | Free fake REST API for learning and testing |
| `data[:2]` | Retrieves the first two elements of a list |
| Path parameter | Passes a value through the URL path |
| f-string | Dynamically inserts values into a string |
| `status_code` | Provides the HTTP response status code |
| `HTTPException` | Raises an HTTP error from a FastAPI endpoint |

---

## 9. Important Improvements for Real Applications

The tutorial demonstrates the basic integration flow. In real applications, we should also consider the following improvements.

### 1. Add a timeout

```python
response = requests.get(url, timeout=15)
```

A timeout prevents the application from waiting indefinitely if the external API does not respond.

### 2. Handle external API errors

The current `/posts` endpoint directly calls `response.json()` without checking the external response status.

A more robust implementation should use:

```python
response.raise_for_status()
```

This raises an exception when the external API returns an unsuccessful HTTP status.

We can catch `requests.RequestException` and return an appropriate error response to the client.

### 3. Understand the difference between external and internal errors

In the current `/posts/{post_id}` endpoint, every external response other than 200 is converted into a 404 error.

However, an external server error (such as 500) does not mean that the requested post was not found.

In a production application, we should distinguish between:
- External resource not found (404).
- External server errors (5xx).
- Connection failures.
- Timeout errors.

An external API failure is often represented to our client using HTTP 502 or 504, depending on the failure.

### 4. Understand synchronous Requests

The Requests library is synchronous.

This means `requests.get()` blocks the current function while waiting for the external API response.

Our current FastAPI endpoints are regular synchronous functions (`def`), so FastAPI executes them in its thread pool.

For applications requiring asynchronous HTTP communication, libraries such as `httpx` can be used with `async def` and `await`.

---

## 10. Interview Questions

**Q1. What is a third-party API?**

A third-party API is an API provided by an external service that allows another application to access its functionality or data.

**Q2. What is the Requests library in Python?**

Requests is a Python library used to send HTTP requests and communicate with external APIs.

**Q3. How do you install Requests?**

We can install it using:

```bash
python -m pip install requests
```

**Q4. What is the purpose of `requests.get()`?**

It sends an HTTP GET request to a specified URL and retrieves the response from the server.

**Q5. What is the purpose of `response.json()`?**

It parses the JSON response body and converts it into corresponding Python objects.

**Q6. What is JSONPlaceholder?**

JSONPlaceholder is a free fake REST API used for testing and learning API integration.

**Q7. What is the difference between `/posts` and `/posts/2`?**

`/posts` retrieves all posts, whereas `/posts/2` retrieves only the post whose ID is 2.

**Q8. How do you integrate an external API with FastAPI?**

We can use a Python HTTP client library such as Requests inside a FastAPI endpoint to send requests to the external API, process its response, and return the retrieved data to the client.

**Q9. What is a path parameter in FastAPI?**

A path parameter is a variable value included directly in the URL path. For example, `{post_id}` in `/posts/{post_id}`.

**Q10. What is HTTPException?**

`HTTPException` is used in FastAPI to terminate request processing and return an HTTP error response with a specified status code and detail message.

**Q11. What is the purpose of `response.status_code`?**

It provides the HTTP status code returned by the external server.

**Q12. What is the difference between Requests and TestClient?**

Requests is used to communicate with external HTTP services, whereas FastAPI TestClient is used to test our own FastAPI application.

**Q13. What happens if an external API is unavailable?**

The request may fail due to a connection error, timeout, or unsuccessful HTTP response. The application should handle these failures and return an appropriate error to its client.

**Q14. Is Requests synchronous or asynchronous?**

Requests is a synchronous HTTP client. It blocks the current function while waiting for the response.

---

## 11. Conclusion

In this tutorial, we learned how to integrate third-party APIs with Python and FastAPI.

We covered:

- Understanding external APIs.
- Installing and importing the Requests library.
- Sending basic GET requests.
- Fetching all records from an external API.
- Fetching an individual record using its ID.
- Converting JSON responses into Python objects.
- Integrating external API calls into FastAPI endpoints.
- Using path parameters to fetch specific records.
- Handling unsuccessful external API responses using HTTPException.
- Testing integrated endpoints using Swagger UI.

Third-party API integration allows backend applications to reuse services and data provided by external systems instead of implementing every functionality independently.