# Testing FastAPI APIs Using Pytest

## 1. Introduction

Testing is an important part of backend development. It helps verify whether an application behaves as expected and whether its API endpoints return the correct responses.

In this tutorial, we learn how to test FastAPI endpoints using **Pytest** and **FastAPI TestClient**.

We will test two endpoints:

1. Home API – Checks whether the API returns a welcome message.
2. Addition API – Checks whether the API correctly adds two numbers.

### Project Structure

```text
21-testing_pytest/
│
├── main.py
├── test_main.py
└── README.md
```

- `main.py` contains the FastAPI application and its endpoints.
- `test_main.py` contains the test cases.
- `README.md` contains the explanation and execution instructions.

---

## 2. Why Testing?

Testing is the process of checking whether a software application or a particular component works as expected.

In backend development, testing helps verify whether API endpoints return the correct status codes, response data, and expected results.

### Why is testing important?

**1. Finding bugs**

Testing helps identify errors in application logic before the application is deployed.

**2. Verifying API responses**

It checks whether an API returns the expected response for a given request.

**3. Preventing regressions**

When developers modify existing code, previously working functionality may accidentally break. Tests help identify these problems.

**4. Improving reliability**

Testing increases confidence that the application behaves correctly under the tested conditions.

**5. Saving development time**

Finding bugs during development is generally easier and less expensive than discovering them after deployment.

### What is API Testing?

API testing involves sending requests to API endpoints and checking their responses.

For example, consider an addition API:

```text
GET /add?a=3&b=4
```

Expected response:

```json
{
    "result": 7
}
```

An API test checks whether the endpoint actually returns this expected result.

---

## 3. Installing Pytest

### What is Pytest?

Pytest is a Python testing framework used to write and execute test cases.

It provides a simple way to test Python applications using ordinary Python functions and `assert` statements.

### Installation

Install Pytest using:

```bash
python -m pip install pytest
```

Verify the installation:

```bash
python -m pytest --version
```

Example output:

```text
pytest 9.2.0
```

### Why use Pytest?

- Simple test case creation.
- Uses Python's built-in `assert` statement.
- Automatically discovers test files.
- Provides detailed failure reports.
- Supports unit testing and integration testing.

### How does Pytest identify test files?

By default, Pytest discovers files following naming conventions such as:

```text
test_*.py
*_test.py
```

For example:

```text
test_main.py
```

Inside these files, functions beginning with `test_` are identified as test functions.

Example:

```python
def test_home():
    assert 2 + 2 == 4
```

Pytest automatically identifies and executes this function.

---

## 4. Understanding Pytest + FastAPI

FastAPI provides a testing utility called `TestClient`.

It allows us to send HTTP requests to our FastAPI application and inspect the responses without manually starting a Uvicorn server.

### What is TestClient?

`TestClient` is provided by:

```python
from fastapi.testclient import TestClient
```

It allows us to test API endpoints directly from Python code.

For example:

```python
client = TestClient(app)
```

Here, the `TestClient` is created using our FastAPI application instance.

We can now send requests using methods such as:

```python
client.get("/")
client.post("/users")
client.put("/users/1")
client.delete("/users/1")
```

These methods simulate HTTP requests to the application.

### Install the testing dependencies

Run:

```bash
python -m pip install pytest httpx
```

`pytest` executes the test cases, while `httpx` provides the HTTP client functionality required by FastAPI's TestClient in the standard setup.

---

## 5. Understanding main.py

The `main.py` file contains the FastAPI application that we want to test.

### Code

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "hello world"
    }

@app.get("/add")
def add(a: int, b: int):
    return {
        "result": a + b
    }
```

### Explanation

**1. Importing FastAPI**

```python
from fastapi import FastAPI
```

Imports the FastAPI class, which is used to create the backend application.

**2. Creating the application**

```python
app = FastAPI()
```

Creates the FastAPI application instance.

**3. Creating the Home API**

```python
@app.get("/")
def home():
    return {
        "message": "hello world"
    }
```

This endpoint handles GET requests sent to the root URL.

Endpoint:

```text
GET /
```

Expected response:

```json
{
    "message": "hello world"
}
```

**4. Creating the Addition API**

```python
@app.get("/add")
def add(a: int, b: int):
    return {
        "result": a + b
    }
```

This endpoint accepts two integer query parameters:

- `a`: First number.
- `b`: Second number.

It adds both numbers and returns the result.

Example request:

```text
GET /add?a=3&b=4
```

Expected response:

```json
{
    "result": 7
}
```

---

## 6. Understanding test_main.py

The `test_main.py` file contains the test cases for the FastAPI endpoints.

### Complete Code

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# test HOME API
def test_home():
    response = client.get("/")

    # status code check
    assert response.status_code == 200

    # response body check
    assert response.json() == {"message": "hello world"}


def test_add():
    response = client.get("/add?a=3&b=4")

    assert response.status_code == 200
    assert response.json() == {"result": 7}
```

### Explanation

**1. Importing TestClient**

```python
from fastapi.testclient import TestClient
```

Imports the TestClient utility provided by FastAPI.

It allows us to send requests to the application during testing without running a separate server.

**2. Importing the FastAPI application**

```python
from main import app
```

Imports the `app` object from `main.py`.

This is the application whose endpoints we want to test.

**3. Creating the TestClient**

```python
client = TestClient(app)
```

Creates a testing client connected to our FastAPI application.

We can use this client to send HTTP requests to the application's endpoints.

**4. Testing the Home API**

```python
def test_home():
    response = client.get("/")
```

The function name starts with `test_`, so Pytest identifies it as a test case.

`client.get("/")` sends a simulated GET request to the root endpoint.

The response is stored in the `response` variable.

**5. Checking the HTTP status code**

```python
assert response.status_code == 200
```

The `status_code` property contains the HTTP status code returned by the endpoint.

Here, we verify that the response status code is `200`.

HTTP 200 means the request was successful.

If the actual status code is different, the assertion fails and Pytest reports the test as failed.

**6. Checking the response body**

```python
assert response.json() == {"message": "hello world"}
```

The `response.json()` method converts the JSON response body into a Python object.

We compare the actual response with the expected dictionary.

Expected:

```python
{"message": "hello world"}
```

If both dictionaries match, the assertion passes.

**7. Testing the Addition API**

```python
def test_add():
    response = client.get("/add?a=3&b=4")
```

This sends a GET request to the addition endpoint with two query parameters.

- `a = 3`
- `b = 4`

The endpoint calculates:

```text
3 + 4 = 7
```

**8. Checking the status code**

```python
assert response.status_code == 200
```

Verifies that the addition API successfully processes the request.

**9. Checking the addition result**

```python
assert response.json() == {"result": 7}
```

Verifies that the API returns the correct addition result.

If the returned value is not `7`, the test fails.

---

## 7. Important Pytest Concepts

### 7.1 Test Function

A test function is a Python function that contains statements to verify application behavior.

Example:

```python
def test_add():
    assert 3 + 4 == 7
```

Pytest automatically discovers functions whose names begin with `test_`.

### 7.2 Assert Statement

The `assert` statement checks whether a condition is true.

Syntax:

```python
assert actual_value == expected_value
```

If the condition is true, the test passes.

If the condition is false, the test fails.

Example:

```python
assert 10 == 10
```

This passes.

```python
assert 10 == 20
```

This fails.

### 7.3 Response Object

When we send a request using TestClient, it returns a response object.

For example:

```python
response = client.get("/")
```

We can inspect different properties:

| Property | Purpose |
|---|---|
| `response.status_code` | Returns the HTTP status code |
| `response.json()` | Returns the parsed JSON response |
| `response.text` | Returns the response body as text |
| `response.headers` | Provides the response headers |

### 7.4 TestClient vs Uvicorn

| TestClient | Uvicorn |
|---|---|
| Used for testing APIs | Used to run the application server |
| Does not require a separate server process | Starts an ASGI server |
| Sends requests directly to the application | Accepts requests over a network |
| Commonly used in automated tests | Commonly used during development and deployment |

---

## 8. Running the Test Cases

### Step 1: Open the project folder

Open the terminal inside:

```text
21-testing_pytest
```

### Step 2: Install dependencies

```bash
python -m pip install fastapi uvicorn pytest httpx
```

### Step 3: Run Pytest

Execute:

```bash
python -m pytest
```

Pytest automatically discovers the `test_main.py` file and executes the test functions.

### Expected Output

```text
============================= test session starts =============================
collected 2 items

test_main.py ..                                                           [100%]

============================== 2 passed ======================================
```

The two dots indicate that both test cases passed.

- `test_home()` passed.
- `test_add()` passed.

### Useful Pytest Commands

| Command | Purpose |
|---|---|
| `python -m pytest` | Runs all discovered tests |
| `python -m pytest -v` | Runs tests with detailed names and results |
| `python -m pytest -q` | Runs tests with shorter output |
| `python -m pytest test_main.py` | Runs tests from a specific file |
| `python -m pytest -k add` | Runs tests whose names match `add` |
| `python -m pytest -s` | Displays print output from test execution |

**Important:** We do not need to start the Uvicorn server separately when using FastAPI's TestClient for these tests.

---

## 9. Understanding the Testing Execution Flow

The execution takes place in the following order:

1. We execute `python -m pytest` in the terminal.
2. Pytest searches for files matching its test file naming conventions.
3. It identifies `test_main.py`.
4. Pytest imports the test file.
5. `test_main.py` imports the FastAPI `app` from `main.py`.
6. `TestClient(app)` creates a client for the application.
7. Pytest identifies the `test_home()` and `test_add()` functions.
8. `test_home()` sends a GET request to `/`.
9. The home endpoint returns its JSON response.
10. The test checks the status code and response body.
11. `test_add()` sends a GET request to `/add?a=3&b=4`.
12. The addition endpoint calculates the result and returns its JSON response.
13. The test checks the status code and result.
14. Pytest displays the final test results.

---

## 10. Interview Questions

**Q1. What is testing in software development?**

Testing is the process of verifying whether an application behaves as expected and identifying errors before deployment.

**Q2. What is Pytest?**

Pytest is a Python testing framework used to write, discover, and execute test cases.

**Q3. Why do we use Pytest with FastAPI?**

We use Pytest to automate testing of FastAPI endpoints and verify their status codes, response bodies, and expected behavior.

**Q4. What is TestClient in FastAPI?**

TestClient is a testing utility that allows us to send simulated HTTP requests to a FastAPI application without starting a separate server.

**Q5. What is the purpose of `assert`?**

The `assert` statement checks whether a condition is true. If it is false, the test fails.

**Q6. How does Pytest identify test functions?**

By default, Pytest identifies functions whose names begin with `test_` inside discovered test files.

**Q7. What is the difference between unit testing and integration testing?**

Unit testing checks individual components or functions independently. Integration testing checks whether multiple components work correctly together.

**Q8. What does HTTP status code 200 indicate?**

It indicates that the HTTP request was successfully processed.

**Q9. What is the purpose of `response.json()`?**

It parses the JSON response body and returns the corresponding Python object, such as a dictionary or list.

**Q10. Do we need to start Uvicorn to run TestClient tests?**

No. TestClient can communicate directly with the FastAPI application in the test process, so a separate Uvicorn server is not required.

**Q11. What happens when an assertion fails?**

Pytest marks the corresponding test as failed and displays information about the assertion and the actual and expected values.

**Q12. What is regression testing?**

Regression testing checks whether existing functionality continues to work correctly after code changes.

---

## 11. Conclusion

In this tutorial, we learned how to test FastAPI APIs using Pytest and TestClient.

We covered:

- Why testing is important.
- Installing and running Pytest.
- Creating test functions.
- Importing the FastAPI application into the test file.
- Creating a TestClient instance.
- Sending GET requests to API endpoints.
- Checking HTTP status codes.
- Validating JSON response bodies using assertions.
- Running tests automatically through the terminal.

Testing helps developers identify problems early and maintain the reliability of backend applications as they grow.