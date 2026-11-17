# FastAPI CORS Configuration Using Environment Variables

## 1. Introduction

In this tutorial, we learn how to configure **Cross-Origin Resource Sharing (CORS)** in FastAPI and manage application configuration using environment variables.

Previously, the CORS settings were directly written inside `main.py`. Now, we are moving those settings into separate configuration files.

This approach helps us:
- Keep application code clean and organized.
- Store configuration separately from application logic.
- Manage different configurations for development and production.
- Avoid hardcoding sensitive values directly in the application.

The project contains four important files:

```text
19-cors/
│
├── main.py
├── config.py
├── .env
├── index.html
└── README.md
```

---

## 2. Understanding CORS

### What is CORS?

CORS stands for **Cross-Origin Resource Sharing**.

It is a browser security mechanism that controls whether a frontend application running on one origin can access resources from a backend running on another origin.

For example:

- Frontend: `http://localhost:5500`
- Backend: `http://127.0.0.1:8000`

These are different origins because their hostnames and ports are different.

When the frontend sends a request to the backend, the browser checks whether the backend allows that frontend origin.

If the backend does not allow it, the browser blocks the frontend from accessing the response.

### What is an Origin?

An origin consists of three components:

1. Protocol – HTTP or HTTPS.
2. Hostname – localhost, example.com, etc.
3. Port – 5500, 8000, etc.

For example:

```text
http://localhost:5500
```

Here:

- Protocol: `http`
- Hostname: `localhost`
- Port: `5500`

Even `localhost` and `127.0.0.1` are considered different hostnames and therefore different origins.

---

## 3. Understanding Environment Variables

### What are Environment Variables?

Environment variables are values stored outside the application code that can be accessed by a running application.

They are commonly used to store configuration information such as:

- Secret keys
- Database connection URLs
- Allowed frontend origins
- API credentials
- Application settings

Instead of directly writing these values inside `main.py`, they can be maintained separately.

For example, instead of:

```python
SECRET_KEY = "my-secret-key"
```

We can retrieve the value from an environment variable:

```python
SECRET_KEY = os.getenv("SECRET_KEY")
```

This makes it easier to change configurations without modifying the application code.

### What is a `.env` File?

A `.env` file is a commonly used file for storing environment variable values in a local development environment.

Example:

```env
SECRET_KEY="secret"

ORIGINS=["http://localhost:5500"]

DB_URL="sqlite:///./test.db"
```

Each entry contains a variable name and its corresponding value.

**Important:** A `.env` file is not automatically loaded by Python. We need a package such as `python-dotenv` to load its values into the environment.

The `.env` file should not be committed to a public Git repository when it contains secrets or private configuration.

---

## 4. Understanding python-dotenv

### What is python-dotenv?

`python-dotenv` is a Python package that reads values from a `.env` file and loads them into the application's environment.

Install it using:

```bash
pip install python-dotenv
```

Import it:

```python
from dotenv import load_dotenv
```

Load the environment variables:

```python
load_dotenv()
```

After calling `load_dotenv()`, we can retrieve the loaded values using:

```python
os.getenv("SECRET_KEY")
```

### Understanding `os.getenv()`

The `os` module provides functions to interact with the operating system.

`os.getenv()` retrieves the value of an environment variable.

Syntax:

```python
os.getenv("VARIABLE_NAME")
```

Example:

```python
SECRET_KEY = os.getenv("SECRET_KEY")
```

If the variable is not available, `os.getenv()` returns `None` by default.

---

## 5. Understanding config.py

The `config.py` file is responsible for loading and organizing application configuration.

### Code

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    origins = os.getenv("ORIGINS")
    SECRET_KEY = os.getenv("SECRET_KEY")
    DB_URL = os.getenv("DB_URL")

settings = Settings()
```

### Explanation

**1. Importing required modules**

```python
import os
from dotenv import load_dotenv
```

- `os` provides access to environment variables.
- `load_dotenv` loads values from the `.env` file.

**2. Loading environment variables**

```python
load_dotenv()
```

This reads the `.env` file and makes its variables available through the environment.

**3. Creating the Settings class**

```python
class Settings:
```

The `Settings` class groups all application configuration values in one place.

Instead of retrieving environment variables separately throughout the application, we can access them through this class.

**4. Reading configuration values**

```python
origins = os.getenv("ORIGINS")
SECRET_KEY = os.getenv("SECRET_KEY")
DB_URL = os.getenv("DB_URL")
```

Each variable retrieves its corresponding value from the environment.

- `origins`: Defines the frontend origins allowed to access the backend.
- `SECRET_KEY`: Stores the application's secret key.
- `DB_URL`: Stores the database connection URL.

**5. Creating a Settings object**

```python
settings = Settings()
```

This creates an object of the `Settings` class.

We can now access its configuration values using:

```python
settings.origins
settings.SECRET_KEY
settings.DB_URL
```

This object is imported into `main.py` to access the application configuration.

---

## 6. Understanding main.py

The `main.py` file contains the FastAPI application and its CORS configuration.

### Code

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings

app = FastAPI()

origins = settings.origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {
        "message": "CORS ENABLE API"
    }
```

### Explanation

**1. Importing FastAPI and CORS middleware**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
```

- `FastAPI` is used to create the backend application.
- `CORSMiddleware` handles CORS-related request and response headers.

**2. Importing application settings**

```python
from config import settings
```

This imports the `settings` object created in `config.py`.

It allows `main.py` to access configuration values without directly reading the `.env` file.

**3. Creating the FastAPI application**

```python
app = FastAPI()
```

This creates the FastAPI application instance.

**4. Retrieving allowed origins**

```python
origins = settings.origins
```

The allowed frontend origins are retrieved from the configuration object.

This means the origin configuration is maintained in `.env` instead of being hardcoded inside `main.py`.

**5. Adding CORS middleware**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

This registers CORS middleware with the FastAPI application.

Understanding each parameter:

- `CORSMiddleware`: Middleware responsible for handling CORS.
- `allow_origins`: Specifies which frontend origins are allowed to communicate with the backend.
- `allow_credentials=True`: Allows browser requests to include credentials such as cookies or authorization-related credentials, subject to browser CORS rules.
- `allow_methods=["*"]`: Allows all HTTP methods, including GET, POST, PUT, PATCH, and DELETE.
- `allow_headers=["*"]`: Allows all request headers.

**6. Creating the home endpoint**

```python
@app.get("/")
def home():
    return {
        "message": "CORS ENABLE API"
    }
```

This creates a GET endpoint at the root URL.

When the frontend sends a GET request to the backend, this endpoint returns a JSON response.

---

## 7. Understanding index.html

The `index.html` file acts as the frontend application.

It contains HTML for the page, CSS for styling, and JavaScript to communicate with the FastAPI backend.

### 7.1 HTML Structure

```html
<h1>FastAPI CORS Demo</h1>

<p>Click below to connect with FastAPI</p>

<button onclick="connectBackend()">
    Connect to FastAPI
</button>

<div id="result"></div>
```

- `<h1>` displays the page heading.
- `<p>` displays an instruction.
- `<button>` creates a button.
- `onclick` calls the JavaScript function when the button is clicked.
- `<div id="result">` provides a place to display the backend response.

### 7.2 CSS Styling

The `<style>` section controls the appearance of the webpage.

It defines:

- Font family.
- Text alignment.
- Background color.
- Heading color.
- Button size and background color.
- Result text styling.

CSS improves the appearance of the frontend but does not control the CORS communication itself.

### 7.3 JavaScript Function

```javascript
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
```

**1. Async function**

```javascript
async function connectBackend()
```

The `async` keyword allows the function to use `await` when working with asynchronous operations.

**2. Accessing the result element**

```javascript
const result = document.getElementById("result");
```

This retrieves the HTML element whose ID is `result`.

The backend response or error message will be displayed inside this element.

**3. Using fetch()**

```javascript
const response = await fetch(
    "http://127.0.0.1:8000/",
    {
        method: "GET"
    }
);
```

`fetch()` is a JavaScript function used to send HTTP requests to a server.

Here:

- URL: `http://127.0.0.1:8000/`
- Method: `GET`
- Destination: FastAPI backend.

**4. Understanding await**

`await` pauses the execution of the current async function until the asynchronous operation completes.

Here, JavaScript waits for the backend response before continuing.

**5. Converting the response into JSON**

```javascript
const data = await response.json();
```

The backend returns JSON data.

The `response.json()` method reads and parses that response into a JavaScript object.

For example:

```json
{
    "message": "CORS ENABLE API"
}
```

We can access the message using:

```javascript
data.message
```

**6. Displaying the backend response**

```javascript
result.innerHTML =
    "Backend Response: " + data.message;
```

This displays the response received from FastAPI on the webpage.

Expected output:

```text
Backend Response: CORS ENABLE API
```

**7. Handling errors using try-catch**

```javascript
catch (error) {
    result.innerHTML =
        "Error: " + error.message;
}
```

If the request fails or the browser blocks access to the response because of CORS, the catch block displays an error message.

---

## 8. Complete Application Execution Flow

The application works in the following sequence:

1. The FastAPI application starts by executing `main.py`.
2. `main.py` imports the `settings` object from `config.py`.
3. `config.py` loads the `.env` file using `load_dotenv()`.
4. The `Settings` class retrieves the environment variable values.
5. The `settings` object makes these values available to `main.py`.
6. FastAPI retrieves the allowed frontend origins through `settings.origins`.
7. CORS middleware is registered with the application.
8. The frontend is opened in the browser.
9. The user clicks the **Connect to FastAPI** button.
10. JavaScript executes the `connectBackend()` function.
11. `fetch()` sends a GET request to the FastAPI backend.
12. The browser checks the CORS response headers.
13. Since the frontend origin is allowed, the browser permits JavaScript to access the response.
14. FastAPI returns the JSON response.
15. JavaScript extracts the message and displays it on the webpage.

---

## 9. Running the Application

### Step 1: Install required packages

Run:

```bash
pip install fastapi uvicorn python-dotenv
```

### Step 2: Start the FastAPI backend

Open the terminal inside the project folder and execute:

```bash
python -m uvicorn main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

### Step 3: Start the frontend server

Open another terminal inside the same project folder and execute:

```bash
python -m http.server 5500
```

The frontend runs at:

```text
http://localhost:5500
```

### Step 4: Open the frontend

Open the following URL in your browser:

```text
http://localhost:5500
```

### Step 5: Test the connection

Click the **Connect to FastAPI** button.

Expected output:

```text
Backend Response: CORS ENABLE API
```

This confirms that the frontend successfully accessed the FastAPI backend.

Keep both terminal windows running while testing. Use `Ctrl + C` to stop each server.

---

## 10. Important Concepts to Remember

| Concept | Purpose |
|---|---|
| CORS | Controls browser access to cross-origin responses |
| Origin | Combination of protocol, hostname, and port |
| Environment variables | Store configuration outside application code |
| `.env` | Local file used to define environment variables |
| `python-dotenv` | Loads `.env` values into the environment |
| `load_dotenv()` | Reads the `.env` file |
| `os.getenv()` | Retrieves an environment variable |
| Settings class | Organizes application configuration |
| `CORSMiddleware` | Handles CORS configuration |
| `allow_origins` | Defines permitted frontend origins |
| `allow_credentials` | Controls whether credentials may be included |
| `allow_methods` | Defines permitted HTTP methods |
| `allow_headers` | Defines permitted request headers |
| `fetch()` | Sends HTTP requests from JavaScript |
| `async/await` | Handles asynchronous operations |
| `try-catch` | Handles JavaScript errors |

---

## 11. Important Notes and Improvements

**1. Environment variable values are strings**

`os.getenv()` returns a string. Therefore, the value of `ORIGINS` in the current `.env` file is not automatically converted into a Python list.

For this tutorial, the following:

```env
ORIGINS=["http://localhost:5500"]
```

would be retrieved as a string, not a list.

Convert it before passing it to `allow_origins`:

```python
import json

origins = json.loads(settings.origins)
```

This converts the JSON-formatted string into a Python list.

**2. Correct database URL**

Use:

```env
DB_URL="sqlite:///./test.db"
```

This is the SQLite connection URL format. The value should be quoted in the `.env` file.

**3. Be careful with allow_credentials**

When `allow_credentials=True`, do not use a wildcard origin (`"*"`). Specify the permitted origins explicitly.

**4. Protect the `.env` file**

Do not upload real secret keys, database credentials, or other private values to a public Git repository.

Add the following to `.gitignore`:

```gitignore
.env
```

**5. CORS is not authentication**

CORS does not authenticate users or secure backend endpoints. It is a browser-enforced access-control mechanism. APIs still need appropriate authentication and authorization.

---

## 12. Interview Questions

**Q1. What is CORS?**

CORS stands for Cross-Origin Resource Sharing. It is a browser security mechanism that controls whether a frontend from one origin can access resources from another origin.

**Q2. Why do we use CORSMiddleware in FastAPI?**

We use `CORSMiddleware` to configure which frontend origins, HTTP methods, and request headers are permitted to access the backend through browser-based requests.

**Q3. What is an origin?**

An origin is defined by the combination of protocol, hostname, and port.

**Q4. What is an environment variable?**

An environment variable is a configuration value stored outside the application source code and accessed by the running application.

**Q5. What is the purpose of a `.env` file?**

A `.env` file stores environment variables, such as secret keys, database URLs, and application configuration values, commonly for local development.

**Q6. What is python-dotenv?**

It is a Python package that loads variables from a `.env` file into the environment.

**Q7. What is the purpose of `load_dotenv()`?**

It reads the `.env` file and loads its values into the environment so they can be accessed using functions such as `os.getenv()`.

**Q8. What is the difference between `os.getenv()` and `load_dotenv()`?**

`load_dotenv()` loads variables from a `.env` file, whereas `os.getenv()` retrieves the value of a particular environment variable.

**Q9. Why do we create a Settings class?**

A Settings class organizes application configuration in one place, making the application easier to maintain and configure.

**Q10. What is the purpose of `allow_origins`?**

It specifies which frontend origins are allowed to access the backend through browser-based cross-origin requests.

**Q11. Does CORS provide authentication?**

No. CORS controls browser access to cross-origin responses. Authentication verifies the identity of a user or client.

**Q12. Why do we use `async` and `await` in JavaScript?**

They help handle asynchronous operations, such as sending HTTP requests and waiting for server responses, without blocking the browser's main execution thread.

---

## 13. Conclusion

In this tutorial, we implemented CORS in FastAPI and improved configuration management by separating application settings from the main application code.

We learned how to:

- Configure CORS using `CORSMiddleware`.
- Define allowed frontend origins.
- Store configuration values in a `.env` file.
- Load environment variables using `python-dotenv`.
- Retrieve environment variables using `os.getenv()`.
- Organize application settings using a Python class.
- Connect an HTML frontend to a FastAPI backend using JavaScript `fetch()`.

This structure provides a foundation for managing configuration in larger FastAPI applications.