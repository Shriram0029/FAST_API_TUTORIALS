# Async Programming in FastAPI

## 1. Introduction to Asynchronous Programming

Asynchronous programming is a programming approach that allows an application to perform other tasks while waiting for a time-consuming operation to complete.

In normal synchronous programming, tasks are generally executed one after another. When one task takes time to complete, the execution waits until that task finishes before moving to the next statement.

In asynchronous programming, the application can pause a task while it is waiting for an operation and allow other tasks to execute during that waiting period.

This is particularly useful in web applications where multiple users may send requests to the server simultaneously.

FastAPI supports asynchronous programming using Python's `async` and `await` keywords.

### What is Synchronous Programming?

Synchronous programming is an execution model in which operations are performed sequentially.

A task must finish before the next statement in the same execution flow can proceed.

For example:

```python
import time

def task():
    time.sleep(3)
    return "Done"
```

**Understanding the code:**

- `def task()` defines a normal Python function.
- `time.sleep(3)` pauses the current thread for three seconds.
- `return "Done"` returns the result after the waiting period.

**What happens during execution?**

1. The function starts executing.
2. `time.sleep(3)` pauses the current thread.
3. The thread remains blocked for three seconds.
4. After three seconds, execution continues.
5. The function returns `"Done"`.

The important point is that `time.sleep()` blocks the thread during the waiting period.

If a thread is responsible for handling other work, that work cannot execute on that thread while it is blocked.

### What is Asynchronous Programming?

Asynchronous programming allows a task to pause while waiting for an operation without blocking the event loop.

Python provides the `asyncio` module to support asynchronous programming.

Example:

```python
import asyncio

async def task():
    await asyncio.sleep(3)
    return "Done"
```

**Understanding the code:**

- `async def task()` defines an asynchronous function.
- `await` pauses the current coroutine until the awaited operation completes.
- `asyncio.sleep(3)` waits for three seconds without blocking the event loop.
- `return "Done"` returns the result after the waiting period.

**What happens during execution?**

1. The asynchronous function starts executing.
2. `await asyncio.sleep(3)` begins an asynchronous waiting operation.
3. The current coroutine pauses.
4. The event loop can execute other ready tasks during this waiting period.
5. After three seconds, the coroutine resumes.
6. The function returns `"Done"`.

The important point is that `asyncio.sleep()` does not block the event loop while waiting.

---

## 2. Understanding async and await

Python provides two important keywords for asynchronous programming:

- `async`
- `await`

Both work together to define and execute asynchronous operations.

### 2.1 What is async?

The `async` keyword is used to define an asynchronous function, also called a coroutine function.

Syntax:

```python
async def function_name():
    # asynchronous operations
    pass
```

Example:

```python
async def task():
    return "Done"
```

**Important points:**

1. `async def` declares an asynchronous function.
2. Calling an asynchronous function normally creates a coroutine object.
3. The coroutine must be awaited or scheduled on an event loop to execute its asynchronous work.
4. Asynchronous functions are useful when an operation involves waiting, such as network requests or database operations supported by asynchronous libraries.

### 2.2 What is await?

The `await` keyword is used inside an asynchronous function to wait for an awaitable operation to complete.

An awaitable is an object that can be used with `await`, such as a coroutine or an asyncio Task.

Example:

```python
await asyncio.sleep(3)
```

**Understanding the statement:**

- `asyncio.sleep(3)` creates an asynchronous waiting operation.
- `await` pauses the current coroutine until that operation completes.
- During this waiting period, the event loop can execute other ready coroutines.

Unlike `time.sleep()`, `asyncio.sleep()` does not block the event loop.

### 2.3 Difference Between async and await

| async | await |
|---|---|
| Used to define an asynchronous function | Used to wait for an awaitable operation |
| Written before `def` | Written before an awaitable expression |
| Creates a coroutine function | Suspends the current coroutine until the awaited operation completes |
| Example: `async def task()` | Example: `await asyncio.sleep(3)` |

### 2.4 Understanding the asyncio Module

The `asyncio` module is Python's built-in library for writing asynchronous code.

It provides functionality to create, manage, and execute asynchronous tasks.

Some important asyncio functions include:

**1. asyncio.sleep()**

```python
await asyncio.sleep(3)
```

Pauses the current coroutine for the specified duration without blocking the event loop.

**2. asyncio.run()**

```python
asyncio.run(task())
```

Runs an asynchronous coroutine by creating and managing an event loop, and returns its result when the coroutine finishes.

It is commonly used as the entry point for standalone asynchronous Python programs. In FastAPI endpoints, the framework manages the event loop, so `asyncio.run()` should not be called inside an endpoint.

**3. asyncio.gather()**

```python
await asyncio.gather(task1(), task2())
```

Runs multiple awaitable operations concurrently and waits for all of them to complete.

It is useful when independent asynchronous operations can run at the same time.

---

## 3. Why Does Asynchronous Programming Matter?

Asynchronous programming is important because web applications often need to handle multiple requests and perform operations that involve waiting.

Consider a FastAPI application that receives requests from several users.

A request may need to:

- Fetch information from an external API.
- Communicate with a database.
- Read data from a file.
- Wait for a network response.
- Perform other input/output operations.

These operations may take time because the application must wait for another system or resource.

### 3.1 Problem with Synchronous Execution

Consider a server receiving three requests.

Each request requires three seconds of waiting.

With a simple single-threaded synchronous execution model:

```text
Request 1: 0s -------- 3s
Request 2:                  3s -------- 6s
Request 3:                                       6s -------- 9s

Total waiting time: Approximately 9 seconds
```

The requests are handled one after another in this simplified example.

While the first request is waiting, the same execution thread cannot process the second request.

### 3.2 How Asynchronous Execution Helps

In asynchronous execution, the server can switch to other ready tasks while one request is waiting for an asynchronous operation.

Consider three requests, each waiting for three seconds:

```text
Request 1: 0s -------- 3s
Request 2: 0s -------- 3s
Request 3: 0s -------- 3s

Total waiting time: Approximately 3 seconds
```

This is an illustrative example assuming all three operations can wait concurrently and there is no significant additional overhead.

The actual execution time depends on the number of requests, server configuration, available resources, and the operations being performed.

### 3.3 What is an Event Loop?

An event loop is a central component of asynchronous programming.

It manages asynchronous tasks and decides which task should execute when another task is waiting.

For example:

1. Request 1 starts an asynchronous operation.
2. Request 1 reaches an `await` statement and pauses.
3. The event loop checks for other tasks that are ready to execute.
4. Request 2 gets an opportunity to execute.
5. Request 2 also reaches an asynchronous waiting operation.
6. The event loop can execute Request 3.
7. When the waiting operations complete, the corresponding requests resume.

The event loop allows multiple asynchronous tasks to make progress without requiring a separate thread for every waiting operation.

### 3.4 What is a Coroutine?

A coroutine is a special function that can pause its execution and resume later.

In Python, an asynchronous function defined using `async def` is a coroutine function.

Example:

```python
async def task():
    await asyncio.sleep(3)
    return "Done"
```

When this function is called, it produces a coroutine object.

The event loop executes the coroutine, and the `await` statement allows it to suspend while waiting for an operation.

**Difference between a normal function and a coroutine:**

| Normal Function | Coroutine Function |
|---|---|
| Defined using `def` | Defined using `async def` |
| Executes when called | Calling it creates a coroutine object |
| Returns its result directly when executed | Must be awaited or scheduled to execute |
| Cannot use `await` directly | Can use `await` inside its body |

---

## 4. Asynchronous Programming in FastAPI

FastAPI supports both synchronous and asynchronous endpoint functions.

### 4.1 Synchronous Endpoint

```python
from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/")
def home():
    time.sleep(3)
    return {
        "message": "Sync API"
    }
```

Here, `def home()` defines a synchronous endpoint.

The `time.sleep(3)` statement blocks the thread executing the function for three seconds.

FastAPI normally runs synchronous endpoint functions in an external thread pool, rather than directly blocking the event loop.

However, the worker thread remains occupied during the blocking operation.

### 4.2 Asynchronous Endpoint

The current implementation uses:

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/")
async def home():
    await asyncio.sleep(3)
    return {
        "message": "Async API"
    }
```

**Understanding the code:**

**1. Importing FastAPI**

```python
from fastapi import FastAPI
```

Imports the FastAPI class required to create the application.

**2. Importing asyncio**

```python
import asyncio
```

Imports Python's built-in asynchronous programming library.

It provides functions such as `asyncio.sleep()`.

**3. Creating the Application**

```python
app = FastAPI()
```

Creates the FastAPI application instance.

**4. Defining the Endpoint**

```python
@app.get("/")
```

Defines a GET endpoint at the root URL.

**5. Defining an Asynchronous Function**

```python
async def home():
```

The `async` keyword makes `home()` an asynchronous function.

FastAPI can execute this endpoint as a coroutine on its event loop.

**6. Waiting Asynchronously**

```python
await asyncio.sleep(3)
```

This statement introduces an asynchronous delay of three seconds.

During this period:

- The current coroutine pauses.
- The event loop remains available.
- Other ready asynchronous tasks can make progress.
- After three seconds, the current coroutine resumes.

**7. Returning the Response**

```python
return {
    "message": "Async API"
}
```

After the waiting operation completes, the endpoint returns a Python dictionary.

FastAPI converts the dictionary into a JSON response.

Expected response:

```json
{
    "message": "Async API"
}
```

### 4.3 Execution Flow of the Current API

1. The client sends a GET request to `/`.
2. FastAPI receives the request.
3. The `home()` asynchronous endpoint starts executing.
4. The endpoint reaches `await asyncio.sleep(3)`.
5. The current coroutine pauses for three seconds.
6. The event loop can process other ready asynchronous tasks.
7. After three seconds, the coroutine resumes.
8. The endpoint returns the JSON response.
9. FastAPI sends the response to the client.

### 4.4 Testing Through Swagger UI

Run the application using:

```bash
python -m uvicorn main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Follow these steps:

1. Expand GET `/`.
2. Click **Try it out**.
3. Click **Execute**.
4. Wait approximately three seconds.
5. Observe the response.

Expected response:

```json
{
    "message": "Async API"
}
```

The endpoint intentionally waits for three seconds before returning the response.

---

## 5. Why Does async Matter in FastAPI?

FastAPI is designed to support asynchronous request handling.

A web application may receive multiple requests while waiting for operations such as database queries or external API responses.

When those operations are implemented using asynchronous libraries, FastAPI can suspend the current request's coroutine and allow other requests to make progress.

### Example Scenario

Imagine an application receiving requests from three users.

Each request calls an external service that takes three seconds to respond.

**Using synchronous blocking operations:**

The worker handling each request remains occupied while waiting for the external service.

**Using asynchronous operations:**

The request coroutine can pause while waiting for the external service. The event loop can then process other ready requests.

This improves the ability of the application to handle concurrent I/O-bound workloads.

### Important Difference

Declaring an endpoint with `async def` alone does not make every operation asynchronous.

For example:

```python
@app.get("/")
async def home():
    time.sleep(3)
    return {"message": "Done"}
```

This is an asynchronous endpoint containing a blocking operation.

`time.sleep(3)` blocks the thread running the event loop, preventing other tasks on that event loop from making progress during that time.

The correct asynchronous version is:

```python
@app.get("/")
async def home():
    await asyncio.sleep(3)
    return {"message": "Done"}
```

The important rule is to use non-blocking, asynchronous operations inside asynchronous endpoints whenever possible.

---

## 6. Performance Benefits of Asynchronous Programming

Asynchronous programming can improve the performance and scalability of applications, especially when they handle many I/O-bound operations.

### 6.1 Better Concurrency

Concurrency means making progress on multiple tasks during overlapping periods.

Asynchronous programming allows the event loop to switch between tasks when they are waiting for operations to complete.

This helps the server handle multiple requests efficiently.

### 6.2 Better Resource Utilization

With asynchronous programming, a thread does not need to remain blocked while waiting for an asynchronous I/O operation.

The event loop can use that time to execute other ready tasks.

This can improve resource utilization when an application handles many simultaneous I/O operations.

### 6.3 Improved Responsiveness

While one request waits for a database or network response, other requests can continue making progress.

This helps the server remain responsive under concurrent workloads.

### 6.4 Efficient I/O-Bound Operations

Asynchronous programming is particularly useful for I/O-bound operations.

I/O-bound operations spend a significant amount of time waiting for external resources.

Examples include:

- HTTP requests to external APIs.
- Asynchronous database queries.
- Network communication.
- Asynchronous file operations.
- Reading data from remote services.

### 6.5 Scalability

Asynchronous programming can help an application handle a larger number of concurrent I/O operations without requiring a separate thread for every waiting task.

This can be beneficial for web applications that receive many requests simultaneously.

### 6.6 Does Async Make Every Program Faster?

No.

Asynchronous programming is especially beneficial for I/O-bound workloads.

It does not automatically improve CPU-bound operations.

**I/O-bound operations:**

These operations spend most of their time waiting for input or output.

Examples:

- Waiting for an API response.
- Waiting for a database query.
- Waiting for network communication.

Asynchronous programming can help because the event loop can execute other tasks during the waiting period.

**CPU-bound operations:**

These operations spend most of their time performing computations.

Examples:

- Large mathematical calculations.
- Image processing.
- Machine learning computations.
- Complex data processing.

Asynchronous programming alone does not make these computations execute faster. CPU-heavy work may need to be moved to a process pool, worker system, or another suitable execution environment.

### 6.7 Synchronous vs Asynchronous Programming

| Feature | Synchronous | Asynchronous |
|---|---|---|
| Execution | Sequential within the execution flow | Tasks can make overlapping progress |
| Waiting | Blocking operations hold the executing thread | Awaiting non-blocking operations suspends the coroutine |
| Concurrency | Often requires threads or processes for concurrent work | Event loop coordinates concurrent coroutines |
| I/O Operations | Worker threads may remain occupied while waiting | Event loop can handle other ready tasks |
| CPU-Bound Tasks | Suitable for ordinary CPU work | Does not automatically speed up CPU work |
| Best Use Case | Simple sequential tasks and blocking libraries | Applications with many I/O-bound operations |

---

## 7. Important Concepts to Remember

### async def

Defines an asynchronous function that produces a coroutine object when called.

### await

Suspends the current coroutine until the awaited operation completes.

### asyncio

Python's built-in library for asynchronous programming.

### asyncio.sleep()

Provides a non-blocking asynchronous delay.

### time.sleep()

Blocks the current thread for the specified duration.

### Event Loop

Manages asynchronous tasks and executes ready coroutines.

### Coroutine

A function that can suspend its execution and resume later.

### Concurrency

The ability to make progress on multiple tasks during overlapping periods.

### I/O-Bound

A workload where execution spends a significant amount of time waiting for input or output operations.

### CPU-Bound

A workload where execution spends most of its time performing computations.

---

## 8. Important Interview Questions

### 1. What is asynchronous programming?

Asynchronous programming is an execution approach that allows tasks to pause while waiting for operations and allows other tasks to execute during that waiting period.

### 2. What is the difference between synchronous and asynchronous programming?

Synchronous programming generally executes operations sequentially, whereas asynchronous programming allows tasks to make progress concurrently while waiting for operations to complete.

### 3. What is async in Python?

`async` is a keyword used to define an asynchronous function using `async def`. Calling that function creates a coroutine object.

### 4. What is await in Python?

`await` is a keyword used inside an asynchronous function to suspend the current coroutine until an awaitable operation completes.

### 5. What is asyncio?

`asyncio` is Python's built-in library used to write and manage asynchronous programs using an event loop and coroutines.

### 6. What is the difference between time.sleep() and asyncio.sleep()?

`time.sleep()` blocks the current thread during the waiting period, whereas `asyncio.sleep()` suspends the current coroutine without blocking the event loop.

### 7. What is a coroutine?

A coroutine is a special function that can pause its execution and resume later. In Python, asynchronous functions defined using `async def` are coroutine functions.

### 8. What is an event loop?

An event loop manages asynchronous tasks and executes ready coroutines. When one coroutine is waiting for an asynchronous operation, the event loop can execute other ready tasks.

### 9. Why is asynchronous programming important in FastAPI?

It allows FastAPI to handle concurrent I/O-bound operations efficiently. While one request waits for a database or network response, other asynchronous requests can make progress.

### 10. Does async make every program faster?

No. Async is especially useful for I/O-bound workloads. It does not automatically improve the speed of CPU-bound computations.

### 11. Can FastAPI support both synchronous and asynchronous endpoints?

Yes. FastAPI supports both `def` and `async def` endpoint functions.

### 12. What happens when an async function is called?

Calling an asynchronous function creates a coroutine object. The coroutine must be awaited or scheduled on an event loop to execute.

### 13. Can await be used inside a normal def function?

No. The `await` keyword can be used inside an asynchronous function, not directly inside a normal synchronous function.

### 14. What happens if time.sleep() is used inside an async endpoint?

It blocks the thread running the event loop during the sleep period. This prevents other tasks on that event loop from making progress.

### 15. What is concurrency?

Concurrency is the ability of a system to make progress on multiple tasks during overlapping periods of time.

### 16. What are I/O-bound operations?

I/O-bound operations spend a significant amount of time waiting for input or output, such as database queries, API calls, and network communication.

### 17. What are CPU-bound operations?

CPU-bound operations spend most of their execution time performing computations, such as mathematical calculations, image processing, and machine learning tasks.

### 18. What is the role of await in FastAPI?

`await` allows an asynchronous FastAPI endpoint to suspend its coroutine while waiting for an asynchronous operation, allowing the event loop to execute other ready tasks.

### 19. Does using async def automatically make database operations asynchronous?

No. The database library must support asynchronous operations. Using a synchronous database library inside an asynchronous endpoint can still block the event loop.

### 20. What is the purpose of asyncio.gather()?

`asyncio.gather()` runs multiple awaitable operations concurrently and waits for all of them to complete.

---

## 9. Key Takeaways

- Asynchronous programming allows tasks to pause and resume during execution.
- `async def` is used to define asynchronous functions.
- `await` is used to wait for an awaitable operation.
- `asyncio` is Python's built-in asynchronous programming library.
- `time.sleep()` blocks the current thread.
- `asyncio.sleep()` does not block the event loop.
- An event loop manages asynchronous tasks.
- A coroutine is a function that can pause and resume execution.
- FastAPI supports both synchronous and asynchronous endpoints.
- Async programming is particularly useful for I/O-bound workloads.
- It can improve concurrency, responsiveness, and resource utilization.
- Async does not automatically make CPU-bound operations faster.
- Blocking operations should be avoided inside asynchronous endpoints whenever possible.

**Final Understanding:** Asynchronous programming helps FastAPI applications handle multiple I/O-bound requests efficiently. The main idea is that when one request is waiting for an operation to complete, the event loop can allow other requests to make progress instead of remaining blocked.