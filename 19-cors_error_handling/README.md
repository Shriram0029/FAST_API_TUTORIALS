# CORS in FastAPI – Connecting HTML Frontend with FastAPI Backend

## 1. Introduction

In a web application, the frontend and backend are often hosted on different origins.

For example:

- Frontend: `http://localhost:5500`
- Backend: `http://127.0.0.1:8000`

When the frontend tries to communicate with the backend, the browser applies security restrictions based on the Same-Origin Policy.

This is where **CORS (Cross-Origin Resource Sharing)** becomes important.

FastAPI provides `CORSMiddleware` to configure which frontend origins are allowed to access the backend.

In this implementation, a simple HTML frontend communicates with a FastAPI backend using JavaScript's `fetch()` function.

### Topics Covered

1. What is CORS?
2. What is Same-Origin Policy?
3. Why is CORS required?
4. CORS middleware in FastAPI
5. Connecting HTML with FastAPI
6. Testing the frontend-backend connection
7. Interview questions

---

# 2. What is CORS?

CORS stands for **Cross-Origin Resource Sharing**.

It is a browser security mechanism that controls whether a webpage from one origin can access resources from another origin.

For example, consider the following applications:

- React or HTML frontend running on `http://localhost:5500`
- FastAPI backend running on `http://127.0.0.1:8000`

When the frontend sends a request to the backend, the browser checks whether the backend allows requests from the frontend's origin.

If the origin is allowed, the browser permits the frontend JavaScript to access the response.

If the origin is not allowed, the browser blocks the frontend from accessing the response.

### 2.1 What is an Origin?

An origin consists of three components:

1. Protocol
2. Hostname
3. Port number

For example:

```text
http://localhost:5500
```

| Component | Value |
|---|---|
| Protocol | `http` |
| Hostname | `localhost` |
| Port | `5500` |

All three components are considered when determining whether two URLs have the same origin.

### 2.2 Same-Origin Examples

Consider the following URLs:

| URL | Same origin as `http://localhost:5500`? |
|---|---|
| `http://localhost:5500/about` | Yes |
| `http://localhost:5500/home` | Yes |
| `http://localhost:8000` | No |
| `https://localhost:5500` | No |
| `http://127.0.0.1:5500` | No |

Even though `localhost` and `127.0.0.1` refer to the local machine, they are different hostnames and therefore different origins.

### 2.3 What is Same-Origin Policy?

Same-Origin Policy is a browser security mechanism that restricts how a webpage can interact with resources from a different origin.

Its purpose is to prevent unauthorized cross-origin interactions.

For example:

```text
Frontend: http://localhost:5500
Backend:  http://127.0.0.1:8000
```

These applications have different origins.

Therefore, browser JavaScript cannot freely access the backend response unless the backend permits the cross-origin request through CORS.

CORS provides a controlled way to allow specific cross-origin communication.

---

# 3. Why Do We Need CORS?

Consider a real-world application:

- Frontend is developed using React.
- Backend is developed using FastAPI.
- Frontend and backend run on different ports.

The frontend needs to communicate with the backend to retrieve data, submit forms, and perform other operations.

Without the correct CORS configuration, the browser may block JavaScript from accessing the backend response.

CORS allows the backend to specify which origins are permitted.

For example:

```python
origins = [
    "http://localhost:5500"
]
```

This means the backend allows browser requests from the specified frontend origin.

**Important:** CORS is not an authentication or authorization mechanism. It controls browser access to cross-origin responses; it does not prevent other clients, such as Postman or command-line programs, from making HTTP requests.

---

# 4. Project Structure

The implementation contains two files inside the same folder.

```text
19-cors/
│
├── main.py
│
└── index.html
```

### main.py

Contains the FastAPI backend application and CORS middleware configuration.

### index.html

Contains the frontend interface, CSS styling, and JavaScript code used to communicate with FastAPI.

---

# 5. Backend Implementation – main.py

## 5.1 Complete Code

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allowed Frontend Origins
origins = [
    "http://localhost:5500"
]

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {
        "message": "CORS ENABLE API"
    }
```

## 5.2 Understanding the Imports

### FastAPI

```python
from fastapi import FastAPI
```

Imports the FastAPI class used to create the backend application and define API endpoints.

### CORSMiddleware

```python
from fastapi.middleware.cors import CORSMiddleware
```

Imports the CORS middleware provided by FastAPI.

Middleware is a component that processes requests and responses as they pass through the application.

`CORSMiddleware` handles cross-origin requests and adds the appropriate CORS response headers.

## 5.3 Creating the FastAPI Application

```python
app = FastAPI()
```

Creates an instance of the FastAPI application.

All API endpoints and middleware configurations are attached to this application.

## 5.4 Defining Allowed Origins

```python
origins = [
    "http://localhost:5500"
]
```

This list contains the frontend origins that are permitted to access the backend through a browser.

In this implementation, the HTML frontend is served at:

```text
http://localhost:5500
```

Therefore, that exact origin is added to the allowed origins list.

If another frontend runs on a different origin, it must also be included if it needs permission to access the backend.

**Important:** An origin includes the protocol, hostname, and port. For example, `http://127.0.0.1:5500` is not the same origin as `http://localhost:5500`.

## 5.5 Adding CORS Middleware

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"]
)
```

This is the main CORS configuration.

The `app.add_middleware()` method registers middleware with the FastAPI application.

Let's understand each argument.

### 1. CORSMiddleware

```python
CORSMiddleware
```

Specifies which middleware should be added.

Here, FastAPI uses CORSMiddleware to handle cross-origin resource sharing.

### 2. allow_origins

```python
allow_origins=origins
```

Specifies the frontend origins that are allowed to access the backend.

In this example:

```python
origins = [
    "http://localhost:5500"
]
```

Only the specified origin is allowed by this configuration.

### 3. allow_credentials

```python
allow_credentials=False
```

Controls whether cross-origin requests are allowed to include credentials such as cookies and HTTP authentication credentials.

Here, it is set to `False` because the current example does not use cookies or credential-based authentication.

### 4. allow_methods

```python
allow_methods=["GET"]
```

Specifies which HTTP methods are allowed for cross-origin requests.

Here, only GET requests are permitted.

Common HTTP methods include:

- GET – Retrieve data.
- POST – Create or submit data.
- PUT – Update data.
- PATCH – Partially update data.
- DELETE – Delete data.

If the application later needs POST, PUT, or DELETE requests from the frontend, those methods must also be allowed.

### 5. allow_headers

```python
allow_headers=["*"]
```

Specifies which request headers are allowed in cross-origin requests.

The wildcard `*` allows all request headers in this configuration.

Examples of HTTP headers include:

- Content-Type
- Authorization
- Accept

## 5.6 Creating the Home API

```python
@app.get("/")
def home():
    return {
        "message": "CORS ENABLE API"
    }
```

Creates a GET endpoint at the root URL.

When the frontend sends a GET request to:

```text
http://127.0.0.1:8000/
```

FastAPI returns:

```json
{
    "message": "CORS ENABLE API"
}
```

This response is used to verify that the frontend can communicate with the backend.

---

# 6. Frontend Implementation – index.html

## 6.1 Complete Code

```html
<!DOCTYPE html>
<html>
<head>
    <title>FastAPI CORS Demo</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 100px;
            background-color: #f4f4f4;
        }

        h1 {
            color: #2563eb;
        }

        button {
            padding: 12px 25px;
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }

        #result {
            margin-top: 25px;
            font-size: 18px;
            color: green;
        }
    </style>
</head>

<body>

    <h1>FastAPI CORS Demo</h1>

    <p>Click below to connect with FastAPI</p>

    <button onclick="connectBackend()">
        Connect to FastAPI
    </button>

    <div id="result"></div>

    <script>
        async function connectBackend() {

            const result = document.getElementById("result");

            try {
                const response = await fetch(
                    "http://127.0.0.1:8000/",
                    {
                        method: "GET"
                    }
                );

                const data = await response.json();

                result.innerHTML =
                    "Backend Response: " + data.message;

            } catch (error) {

                result.innerHTML =
                    "Error: " + error.message;

            }
        }
    </script>

</body>
</html>
```

## 6.2 Understanding the HTML Structure

### 1. HTML Document Declaration

```html
<!DOCTYPE html>
```

Declares that the document uses HTML5.

### 2. HTML Element

```html
<html>
</html>
```

The root element of the HTML document.

It contains the complete webpage structure.

### 3. Head Section

```html
<head>
    <title>FastAPI CORS Demo</title>
</head>
```

The head section contains page information and resources.

The title appears in the browser tab.

### 4. Body Section

```html
<body>
    <h1>FastAPI CORS Demo</h1>
    <p>Click below to connect with FastAPI</p>
</body>
```

The body contains the visible elements of the webpage.

In this implementation, it contains:

- A heading.
- A description.
- A button.
- A result area.

## 6.3 Understanding the CSS

CSS is used to control the appearance and layout of the webpage.

The code contains styling for the body, heading, button, and result section.

### Body Styling

```css
body {
    font-family: Arial, sans-serif;
    text-align: center;
    margin-top: 100px;
    background-color: #f4f4f4;
}
```

- `font-family`: Sets the font.
- `text-align`: Aligns the text to the center.
- `margin-top`: Adds space above the content.
- `background-color`: Sets the background color.

### Button Styling

```css
button {
    padding: 12px 25px;
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
}
```

This controls the button's size, background, text color, border, and cursor.

### Result Styling

```css
#result {
    margin-top: 25px;
    font-size: 18px;
    color: green;
}
```

The `#result` selector targets the HTML element whose ID is `result`.

It controls how the backend response is displayed.

---

# 7. Understanding JavaScript and Fetch API

JavaScript is responsible for communicating with the FastAPI backend.

The most important part of this implementation is the `connectBackend()` function.

## 7.1 Button Click Event

```html
<button onclick="connectBackend()">
    Connect to FastAPI
</button>
```

The button contains an `onclick` event.

When the user clicks the button, the browser executes:

```javascript
connectBackend()
```

This triggers the function that sends the request to FastAPI.

## 7.2 Creating an Asynchronous Function

```javascript
async function connectBackend() {
```

The `async` keyword defines an asynchronous function.

An asynchronous function allows operations that take time, such as HTTP requests, to be handled without blocking the normal execution of the browser interface.

The function uses `await` while waiting for the backend response.

## 7.3 Accessing the Result Element

```javascript
const result = document.getElementById("result");
```

`document.getElementById()` searches the HTML document for an element with the specified ID.

Here, it retrieves:

```html
<div id="result"></div>
```

The returned element is stored in the `result` variable.

JavaScript uses this element to display the backend response.

## 7.4 Using the Fetch API

```javascript
const response = await fetch(
    "http://127.0.0.1:8000/",
    {
        method: "GET"
    }
);
```

The `fetch()` function is a built-in JavaScript API used to send HTTP requests and communicate with servers.

It accepts:

1. The URL of the backend endpoint.
2. An optional configuration object containing request details.

Here, the request is sent to:

```text
http://127.0.0.1:8000/
```

The method is:

```javascript
method: "GET"
```

This sends a GET request to the FastAPI home endpoint.

### What does await do?

`fetch()` returns a Promise.

A Promise represents the eventual result of an asynchronous operation.

The `await` keyword pauses the execution of the current async function until the Promise settles.

After the response arrives, it is stored in:

```javascript
const response
```

## 7.5 Converting the Response into JSON

```javascript
const data = await response.json();
```

The backend returns JSON data.

The `response.json()` method reads the response body and parses it into a JavaScript object.

For example, FastAPI returns:

```json
{
    "message": "CORS ENABLE API"
}
```

JavaScript receives the parsed object:

```javascript
data = {
    message: "CORS ENABLE API"
}
```

Now the message can be accessed using:

```javascript
data.message
```

## 7.6 Displaying the Backend Response

```javascript
result.innerHTML =
    "Backend Response: " + data.message;
```

The `innerHTML` property changes the content inside the HTML element.

The backend response is displayed inside:

```html
<div id="result"></div>
```

The final displayed text becomes:

```text
Backend Response: CORS ENABLE API
```

## 7.7 Understanding Try and Catch

```javascript
try {
    // API request
}
catch (error) {
    // Handle error
}
```

The `try` block contains code that may produce an error.

If an error occurs while executing the request or processing the response, the `catch` block handles it.

In this implementation:

```javascript
result.innerHTML =
    "Error: " + error.message;
```

Displays the error message on the webpage.

This helps identify connection failures and other request errors.

---

# 8. Complete Frontend-Backend Execution Flow

The entire implementation works in the following sequence.

### Step 1 – Start the Backend

FastAPI starts using Uvicorn.

```bash
python -m uvicorn main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

### Step 2 – Start the Frontend

The HTML file is served using Python's built-in HTTP server.

```bash
python -m http.server 5500
```

The frontend runs at:

```text
http://localhost:5500
```

### Step 3 – User Clicks the Button

The user opens the HTML page and clicks the Connect to FastAPI button.

The `onclick` event executes `connectBackend()`.

### Step 4 – JavaScript Sends a Request

The `fetch()` function sends a GET request to:

```text
http://127.0.0.1:8000/
```

### Step 5 – Browser Applies CORS Rules

The browser checks whether the backend allows the frontend origin.

The frontend origin is:

```text
http://localhost:5500
```

The backend has configured this origin inside `allow_origins`.

For this simple GET request, the browser can send the request directly and check the CORS response headers.

### Step 6 – FastAPI Processes the Request

The request reaches the FastAPI endpoint:

```python
@app.get("/")
def home():
    return {
        "message": "CORS ENABLE API"
    }
```

FastAPI generates the JSON response.

### Step 7 – Response Returns to JavaScript

The browser makes the response available to JavaScript because the CORS configuration allows the frontend origin.

JavaScript parses the JSON using:

```javascript
response.json()
```

### Step 8 – Display the Result

The response message is displayed inside the HTML page.

Final output:

```text
Backend Response: CORS ENABLE API
```

---

# 9. Running and Testing the Application

Both applications must run simultaneously.

## 9.1 Start FastAPI

Open the terminal inside the `19-cors` folder.

Execute:

```powershell
python -m uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Keep this terminal running.

## 9.2 Start the HTML Server

Open a second terminal in the same folder.

Execute:

```powershell
python -m http.server 5500
```

Frontend URL:

```text
http://localhost:5500
```

## 9.3 Open the Frontend

Open the following URL in your browser:

```text
http://localhost:5500
```

The webpage displays:

- FastAPI CORS Demo heading.
- A description.
- Connect to FastAPI button.

## 9.4 Test the Connection

1. Click the Connect to FastAPI button.
2. JavaScript sends a GET request.
3. FastAPI receives the request.
4. FastAPI returns the JSON response.
5. JavaScript displays the response.

Expected output:

```text
Backend Response: CORS ENABLE API
```

---

# 10. Common Errors and Troubleshooting

### 1. CORS Policy Error

**Possible reason:** The frontend origin does not match the value configured in `allow_origins`.

For example, the backend allows:

```python
origins = [
    "http://localhost:5500"
]
```

But the frontend is opened using:

```text
http://127.0.0.1:5500
```

These are different origins.

**Solution:** Open the frontend using the exact allowed origin or add the intended origin to the backend configuration.

### 2. Failed to Fetch

Possible reasons:

- FastAPI server is not running.
- Incorrect backend URL.
- Incorrect port number.
- Network or browser request failure.

**Solution:** Check whether FastAPI is running at:

```text
http://127.0.0.1:8000
```

### 3. Frontend Page Does Not Open

Possible reason: The Python HTTP server is not running.

**Solution:** Execute:

```powershell
python -m http.server 5500
```

### 4. Method Not Allowed by CORS

The current backend configuration allows only:

```python
allow_methods=["GET"]
```

If the frontend sends a POST, PUT, or DELETE request, the CORS configuration must be updated to allow that method.

### 5. Port Already in Use

If port 5500 is already being used, the frontend server cannot start on that port.

Choose another available port, such as 5501, and update the allowed origin in FastAPI accordingly.

---

# 11. Important Concepts to Remember

| Concept | Purpose |
|---|---|
| CORS | Controls browser access to cross-origin responses |
| Same-Origin Policy | Restricts cross-origin interactions |
| Origin | Combination of protocol, hostname, and port |
| CORSMiddleware | Handles CORS in FastAPI |
| `add_middleware()` | Registers middleware in FastAPI |
| `allow_origins` | Specifies permitted frontend origins |
| `allow_methods` | Specifies permitted HTTP methods |
| `allow_headers` | Specifies permitted request headers |
| `allow_credentials` | Controls cross-origin credential support |
| `fetch()` | Sends HTTP requests from JavaScript |
| `async` | Defines an asynchronous function |
| `await` | Waits for a Promise to settle |
| `response.json()` | Parses a JSON response |
| `getElementById()` | Finds an HTML element by its ID |
| `innerHTML` | Updates the contents of an HTML element |
| `try-catch` | Handles JavaScript errors |

---

# 12. Important Interview Questions

### 1. What is CORS?

CORS stands for Cross-Origin Resource Sharing. It is a browser security mechanism that allows servers to specify which external origins can access their resources through browser-based requests.

### 2. Why do we need CORS?

CORS is required when a frontend application communicates with a backend hosted on a different origin. It allows the backend to explicitly permit selected frontend origins.

### 3. What is Same-Origin Policy?

Same-Origin Policy is a browser security mechanism that restricts webpages from accessing resources from different origins unless cross-origin access is permitted.

### 4. What is an origin?

An origin consists of three components: protocol, hostname, and port number.

For example:

```text
http://localhost:5500
```

### 5. What is CORSMiddleware?

CORSMiddleware is middleware provided by FastAPI through Starlette. It handles cross-origin requests by adding the appropriate CORS headers to responses.

### 6. What is allow_origins?

`allow_origins` specifies the list of frontend origins permitted to access the backend through browser-based cross-origin requests.

### 7. What is allow_methods?

`allow_methods` specifies which HTTP methods are allowed for cross-origin requests, such as GET, POST, PUT, and DELETE.

### 8. What is allow_headers?

`allow_headers` specifies which HTTP request headers are permitted in cross-origin requests.

### 9. What is allow_credentials?

`allow_credentials` determines whether cross-origin requests can include credentials such as cookies and HTTP authentication information.

### 10. What is a preflight request?

A preflight request is an HTTP OPTIONS request that a browser sends before certain cross-origin requests.

It checks whether the server permits the intended origin, HTTP method, and request headers.

### 11. Does every cross-origin request trigger a preflight request?

No. Some simple cross-origin requests can be sent without a preflight request. Requests using certain methods, headers, or content types require a preflight check.

### 12. What is the Fetch API?

The Fetch API is a built-in JavaScript interface used to make HTTP requests and receive responses from servers.

### 13. What is the difference between async and await?

`async` declares an asynchronous function, while `await` pauses the execution of that async function until a Promise settles.

### 14. What is the purpose of response.json()?

It reads the response body and parses JSON data into a JavaScript object.

### 15. Does CORS provide authentication?

No. CORS is not an authentication mechanism. It controls browser access to cross-origin responses. Authentication is used to verify the identity of users or clients.

### 16. Does CORS block requests from Postman?

No. CORS is enforced by browsers. Postman and other non-browser clients are not restricted by the browser's CORS enforcement.

### 17. Can we allow multiple frontend origins?

Yes. Multiple origins can be specified inside the `allow_origins` list.

Example:

```python
origins = [
    "http://localhost:5500",
    "http://localhost:3000",
    "http://localhost:5173"
]
```

### 18. What happens if the frontend origin is not allowed?

The browser prevents frontend JavaScript from accessing the cross-origin response and reports a CORS error.

---

# 13. Key Takeaways

- CORS stands for Cross-Origin Resource Sharing.
- Same-Origin Policy restricts cross-origin browser interactions.
- An origin consists of protocol, hostname, and port.
- FastAPI provides CORSMiddleware to configure cross-origin access.
- `allow_origins` specifies permitted frontend origins.
- `allow_methods` specifies allowed HTTP methods.
- `allow_headers` specifies permitted request headers.
- `allow_credentials` controls cross-origin credential support.
- JavaScript's `fetch()` function communicates with the FastAPI backend.
- `async` and `await` help handle asynchronous HTTP requests.
- `response.json()` converts the backend JSON response into a JavaScript object.
- CORS is a browser security mechanism, not an authentication system.

**Final Understanding:** In this implementation, the HTML frontend runs on `http://localhost:5500` and the FastAPI backend runs on `http://127.0.0.1:8000`. Since they have different origins, the browser applies CORS restrictions. By configuring `CORSMiddleware` to allow the frontend origin, the frontend can successfully communicate with the FastAPI backend and display its JSON response.