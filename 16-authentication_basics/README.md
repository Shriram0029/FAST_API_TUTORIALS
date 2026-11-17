# Authentication Basics – JWT and Token-Based Authentication

## 1. Introduction to Authentication

Authentication is the process of verifying the identity of a user who wants to access an application.

Whenever a user tries to access a protected application or resource, the application needs to verify whether that user is authorized to access it.

For example, consider an application that allows users to log in using a username and password.

The application checks the submitted credentials. If they are correct, the user is allowed to log in. If they are incorrect, access is rejected.

Authentication is commonly implemented using:

- Username and password.
- Session-based authentication.
- Token-based authentication.
- JSON Web Tokens (JWT).

In this implementation, JWT is used to generate and verify authentication tokens.

## 2. What is JWT?

JWT stands for **JSON Web Token**.

It is a compact, URL-safe format used to represent information between two parties.

JWT is commonly used in authentication systems to transfer information about an authenticated user.

When a user successfully logs in, the server generates a JWT and sends it to the client.

The client stores the token and sends it with subsequent requests to access protected endpoints.

The server verifies the token before allowing access.

### 2.1 Why is JWT Used?

Consider an application with two endpoints:

- `/login` – Used to authenticate a user.
- `/secure` – Used to access protected information.

Without authentication, anyone could potentially access the protected endpoint.

JWT helps solve this problem by requiring the client to provide a valid token.

The application verifies the token before returning protected information.

### 2.2 Structure of a JWT

A JWT consists of three main parts:

1. Header
2. Payload
3. Signature

These three parts are separated by dots (`.`).

General format:

```text
xxxxx.yyyyy.zzzzz
```

**1. Header**

The header contains information about the token type and the signing algorithm.

Example:

```json
{
    "alg": "HS256",
    "typ": "JWT"
}
```

- `alg` represents the algorithm used to sign the token.
- `typ` represents the token type.

In this implementation, the algorithm used is HS256.

**2. Payload**

The payload contains the claims, which are pieces of information carried by the token.

Example:

```json
{
    "sub": "admin",
    "exp": 1793790000
}
```

Some commonly used JWT claims are:

- `sub`: Subject of the token, commonly representing the user.
- `exp`: Expiration time of the token.
- `iat`: Time at which the token was issued.
- `iss`: Issuer of the token.
- `aud`: Intended audience of the token.

In the current implementation:

- `sub` stores the username.
- `exp` stores the token expiration time.

**3. Signature**

The signature is used to verify that the token has not been modified and that it was signed using the expected secret key and algorithm.

In this implementation, the token is signed using:

```python
jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

The server later uses the same secret key and algorithm to verify the token.

### Important Point About JWT

A signed JWT is not automatically encrypted.

Its payload can generally be decoded by anyone who obtains the token. The signature protects its integrity, not the confidentiality of its contents.

Therefore, passwords and other sensitive information should never be stored inside a normal signed JWT payload.

---

## 3. What is Token-Based Authentication?

Token-based authentication is an authentication mechanism in which a server generates a token after successfully verifying a user's credentials.

The client uses that token to prove its authenticated identity when making subsequent requests.

Instead of sending the username and password with every request, the client sends the generated token.

### 3.1 How Token-Based Authentication Works

The process involves the following steps:

**Step 1: User Login**

The user submits their username and password to the login endpoint.

Example:

```text
username = admin
password = 1234
```

**Step 2: Credential Verification**

The server checks whether the submitted credentials are correct.

If the credentials are invalid, the server returns an authentication error.

If they are valid, the server continues with token generation.

**Step 3: Token Generation**

The server creates a JWT containing information about the user.

The token is signed using a secret key and a specified algorithm.

**Step 4: Token Delivery**

The server sends the generated token to the client.

The client stores the token securely.

**Step 5: Accessing Protected Routes**

When the client wants to access a protected endpoint, it sends the token in the request header.

**Step 6: Token Verification**

The server extracts the token and verifies its signature and expiration time.

**Step 7: Granting or Rejecting Access**

- If the token is valid, the user is allowed to access the protected endpoint.
- If the token is invalid or expired, the server returns an authentication error.

### 3.2 Token-Based Authentication Flow

```text
            USER
              |
              |
       Enter Username
        and Password
              |
              v
          LOGIN API
              |
              v
     Verify Credentials
              |
        +-----+-----+
        |           |
     Invalid       Valid
        |           |
        v           v
     Return       Generate
     401 Error    JWT Token
                    |
                    v
              Send Token
               to Client
                    |
                    v
             Request Secure
                Endpoint
                    |
                    v
             Verify Token
                    |
              +-----+-----+
              |           |
           Invalid       Valid
              |           |
              v           v
          Return 401   Grant Access
                         |
                         v
                   Return Secure
                      Data
```

### 3.3 Advantages of Token-Based Authentication

**1. Stateless Authentication**

The server can validate a signed JWT using its signing key without maintaining a traditional server-side session for every authenticated user.

**2. Scalability**

JWT-based authentication can be useful in distributed applications because multiple services can verify tokens using the appropriate shared or public verification keys.

**3. Reduced Repeated Credential Submission**

The client does not need to send the username and password with every protected request. It sends the token instead.

**4. Expiration Support**

Tokens can have an expiration time. Once the expiration time is reached, the token is rejected.

**5. Easy Integration**

JWT can be used with different clients, such as web applications, mobile applications, and other backend services.

---

## 4. JWT Authentication Implementation in FastAPI

The current implementation uses the following libraries:

```python
from fastapi import FastAPI, Header, HTTPException, Depends
from jose import jwt
from datetime import datetime, timedelta, timezone
```

### Understanding the Imports

**1. FastAPI**

```python
from fastapi import FastAPI
```

Used to create the FastAPI application and define API endpoints.

**2. Header**

```python
from fastapi import Header
```

Used to extract values from HTTP request headers.

In this implementation, the JWT is received through a header named `token`.

**3. HTTPException**

```python
from fastapi import HTTPException
```

Used to return HTTP error responses when authentication fails.

For example, status code 401 indicates that authentication is required or the supplied credentials are invalid.

**4. Depends**

```python
from fastapi import Depends
```

Used for dependency injection.

It allows FastAPI to execute the `verify_token()` function before executing the protected endpoint.

**5. jwt**

```python
from jose import jwt
```

Imports the JWT functionality from the Python JOSE library.

It provides methods such as:

- `jwt.encode()` – Generates and signs a token.
- `jwt.decode()` – Decodes and verifies a token.

**6. datetime, timedelta, timezone**

```python
from datetime import datetime, timedelta, timezone
```

These are used to calculate the token expiration time.

- `datetime` provides date and time functionality.
- `timedelta` represents a duration.
- `timezone` provides timezone information, including UTC.

---

## 5. SECRET_KEY and ALGORITHM

```python
SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
```

These two variables are used during token generation and verification.

### 5.1 SECRET_KEY

The secret key is used to sign and verify the JWT.

In this implementation:

```python
SECRET_KEY = "mysecret"
```

The same secret key is used when generating and verifying the token.

If the token is modified or signed using an incorrect key, verification fails.

In real applications, a strong randomly generated secret should be stored securely in environment variables or a secret manager rather than directly inside the source code.

### 5.2 ALGORITHM

```python
ALGORITHM = "HS256"
```

Specifies the signing algorithm used for the JWT.

HS256 stands for HMAC using SHA-256.

It is a symmetric signing algorithm, meaning the same secret key is used to sign and verify the token.

---

## 6. Token Generation – create_token()

The `create_token()` function is responsible for generating a JWT.

### Code

```python
def create_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token
```

### Understanding the Code Step by Step

**1. Receiving the Data**

```python
def create_token(data: dict):
```

The function receives a dictionary containing the information that needs to be included in the JWT payload.

For example:

```python
{
    "sub": "admin"
}
```

Here, `sub` represents the subject of the token, which identifies the user.

**2. Copying the Data**

```python
to_encode = data.copy()
```

The `copy()` method creates a separate copy of the original dictionary.

This allows the function to add additional information without directly modifying the original dictionary.

**3. Calculating the Expiration Time**

```python
expire = datetime.now(timezone.utc) + timedelta(minutes=30)
```

This statement calculates the token's expiration time.

- `datetime.now(timezone.utc)` obtains the current UTC date and time.
- `timedelta(minutes=30)` represents a duration of 30 minutes.
- Adding them calculates the time at which the token expires.

For example, if the token is generated at 10:00 AM UTC, its expiration time will be 10:30 AM UTC.

**4. Adding the Expiration Claim**

```python
to_encode.update({
    "exp": expire
})
```

The `update()` method adds the expiration information to the dictionary.

The `exp` claim represents the expiration time of the JWT.

The token becomes invalid after this expiration time.

**5. Generating the JWT**

```python
token = jwt.encode(
    to_encode,
    SECRET_KEY,
    algorithm=ALGORITHM
)
```

The `jwt.encode()` method generates and signs the JWT.

It accepts three important arguments:

- `to_encode`: The payload containing the user's information and expiration time.
- `SECRET_KEY`: The secret key used for signing.
- `algorithm`: The signing algorithm.

The method returns the generated JWT as a string.

**6. Returning the Token**

```python
return token
```

The generated token is returned to the function that called `create_token()`.

---

## 7. Login API – Token Generation

The login endpoint verifies the user's credentials and generates a JWT when authentication is successful.

### Code

```python
@app.post("/login")
def login(username: str, password: str):

    if username != "admin" or password != "1234":
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_token({
        "sub": username
    })

    return {
        "access_token": token
    }
```

### Understanding the Code Step by Step

**1. Defining the Login Endpoint**

```python
@app.post("/login")
```

Creates a POST endpoint at `/login`.

POST is used because the client is submitting login credentials to the server.

**2. Receiving the Credentials**

```python
def login(username: str, password: str):
```

The function accepts two parameters:

- `username`: The username submitted by the client.
- `password`: The password submitted by the client.

Since these are simple parameters and are not path parameters or declared request-body models, FastAPI treats them as query parameters by default.

For this implementation, Swagger UI will allow the values to be entered as query parameters.

**3. Validating the Credentials**

```python
if username != "admin" or password != "1234":
```

This condition checks whether the submitted credentials match the expected values.

The `or` operator means that if either condition is true, the login is rejected.

For example:

| Username | Password | Result |
|---|---|---|
| admin | 1234 | Valid |
| admin | 1111 | Invalid |
| user | 1234 | Invalid |
| user | 1111 | Invalid |

**4. Returning an Authentication Error**

```python
raise HTTPException(
    status_code=401,
    detail="Invalid credentials"
)
```

If the credentials are incorrect, the application raises an HTTP exception.

- `401` represents Unauthorized.
- `detail` contains the error message.

Example response:

```json
{
    "detail": "Invalid credentials"
}
```

**5. Generating the Token**

```python
token = create_token({
    "sub": username
})
```

If the credentials are correct, the application calls `create_token()`.

The username is passed inside a dictionary using the `sub` claim.

For the username `admin`, the payload contains the subject `admin`, along with the expiration time added by `create_token()`.

**6. Returning the Access Token**

```python
return {
    "access_token": token
}
```

The generated JWT is returned to the client.

Example response:

```json
{
    "access_token": "generated_jwt_token"
}
```

The actual token will be a long encoded string.

---

## 8. Token Verification – verify_token()

After generating the token, the application must verify it whenever the user tries to access a protected endpoint.

The `verify_token()` function performs this verification.

### Code

```python
def verify_token(token: str = Header(None)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
```

### Understanding the Code Step by Step

**1. Receiving the Token from the Header**

```python
def verify_token(token: str = Header(None)):
```

The `Header()` function tells FastAPI to obtain the value from an HTTP request header.

Here:

- `token` is the parameter name.
- `Header(None)` indicates that the header is optional at the parameter declaration level and defaults to `None` if it is absent.

FastAPI uses the parameter name `token` as the header name by default.

Therefore, the client must send:

```text
token: generated_jwt_token
```

**2. Using try and except**

```python
try:
```

The `try` block contains the token verification operation.

If verification fails because the token is missing, invalid, incorrectly signed, or expired, an exception is raised.

**3. Decoding and Verifying the Token**

```python
payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM]
)
```

The `jwt.decode()` method decodes the JWT and verifies its signature and registered claims, including expiration when present.

It accepts:

- `token`: The JWT received from the request header.
- `SECRET_KEY`: The secret key used to verify the signature.
- `algorithms`: A list of permitted signing algorithms.

The permitted algorithm must match the algorithm used to sign the token.

If verification succeeds, the decoded payload is returned as a Python dictionary.

For example:

```python
{
    "sub": "admin",
    "exp": 1793790000
}
```

The exact expiration value depends on when the token was generated.

**4. Returning the Payload**

```python
return payload
```

If the token is valid, the decoded payload is returned.

The protected endpoint can use this information to identify the authenticated user.

**5. Handling Invalid Tokens**

```python
except:
    raise HTTPException(
        status_code=401,
        detail="Invalid or expired token"
    )
```

If token verification fails, the application returns a 401 Unauthorized response.

Example response:

```json
{
    "detail": "Invalid or expired token"
}
```

A production implementation should catch the appropriate JWT and token-related exceptions rather than using a bare `except`.

---

## 9. Protected Route – secure_data()

A protected route is an API endpoint that requires successful authentication before allowing access.

### Code

```python
@app.get("/secure")
def secure_data(user=Depends(verify_token)):
    return {
        "message": "Secure Data Accessed",
        "user": user
    }
```

### Understanding the Code Step by Step

**1. Defining the Protected Endpoint**

```python
@app.get("/secure")
```

Creates a GET endpoint at `/secure`.

This endpoint is intended to return information only to users who provide a valid token.

**2. Using Depends()**

```python
user = Depends(verify_token)
```

This is the most important part of the protected route.

`Depends()` is FastAPI's dependency injection mechanism.

It tells FastAPI to execute the `verify_token()` function before executing the `secure_data()` endpoint.

The execution works as follows:

1. The client sends a request to `/secure`.
2. FastAPI identifies the dependency.
3. FastAPI calls `verify_token()`.
4. `verify_token()` extracts the token from the request header.
5. The token is decoded and verified.
6. If verification succeeds, the decoded payload is returned.
7. That returned payload is assigned to the `user` parameter.
8. The `secure_data()` endpoint executes.

If token verification fails, the dependency raises an HTTPException, and the protected endpoint does not execute.

**3. Returning the Protected Data**

```python
return {
    "message": "Secure Data Accessed",
    "user": user
}
```

If authentication is successful, the endpoint returns a success message and the decoded JWT payload.

Example response:

```json
{
    "message": "Secure Data Accessed",
    "user": {
        "sub": "admin",
        "exp": 1793790000
    }
}
```

The actual expiration timestamp will vary.

---

## 10. Complete Authentication Flow

The complete implementation can be understood through three main stages.

### Stage 1: Login and Credential Validation

The user sends a POST request to `/login` with the username and password.

The server checks the credentials.

If they are incorrect, the server returns 401 Unauthorized.

If they are correct, the server calls `create_token()`.

### Stage 2: JWT Generation

The `create_token()` function:

1. Receives the user's information.
2. Copies the data.
3. Calculates the expiration time.
4. Adds the `exp` claim.
5. Signs the payload using the secret key and HS256.
6. Returns the generated JWT.

The login endpoint sends the token to the client.

### Stage 3: Token Verification and Secure Access

The client sends the generated token in the request header while accessing `/secure`.

FastAPI calls `verify_token()` through `Depends()`.

The token is decoded and verified.

- Valid token: The protected endpoint executes.
- Invalid or expired token: The application returns 401 Unauthorized.

---

## 11. Testing Authentication Using Swagger UI

FastAPI automatically generates Swagger UI documentation.

Start the application:

```bash
python -m uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

There are two endpoints in this implementation:

- POST `/login`
- GET `/secure`

### 11.1 Testing Login API

**Endpoint:**

```text
POST /login
```

Steps:

1. Expand POST `/login`.
2. Click **Try it out**.
3. Enter the username as `admin`.
4. Enter the password as `1234`.
5. Click **Execute**.

Since the parameters are simple function parameters, Swagger sends them as query parameters.

Example request:

```text
POST /login?username=admin&password=1234
```

Expected response:

```json
{
    "access_token": "generated_jwt_token"
}
```

Copy the generated access token.

### 11.2 Testing the Protected Route

**Endpoint:**

```text
GET /secure
```

Steps:

1. Expand GET `/secure`.
2. Click **Try it out**.
3. Locate the `token` header field.
4. Paste the access token generated by the login API.
5. Click **Execute**.

The request must contain:

```text
token: generated_jwt_token
```

Expected response:

```json
{
    "message": "Secure Data Accessed",
    "user": {
        "sub": "admin",
        "exp": 1793790000
    }
}
```

This confirms that the token was successfully verified and the protected endpoint was accessed.

### 11.3 Testing Invalid Credentials

Try logging in with:

```text
username = admin
password = 1111
```

Expected status code:

```text
401 Unauthorized
```

Response:

```json
{
    "detail": "Invalid credentials"
}
```

### 11.4 Testing Invalid Token

Try accessing `/secure` with an incorrect token.

Expected status code:

```text
401 Unauthorized
```

Response:

```json
{
    "detail": "Invalid or expired token"
}
```

### 11.5 Testing Expired Token

The token is configured to expire after 30 minutes.

After the expiration time, using that token to access `/secure` should result in:

```text
401 Unauthorized
```

This happens because `jwt.decode()` verifies the expiration claim.

---

## 12. Important Functions and Concepts Used

| Function / Concept | Purpose |
|---|---|
| `jwt.encode()` | Generates and signs a JWT |
| `jwt.decode()` | Decodes and verifies a JWT |
| `datetime.now()` | Gets the current date and time |
| `timezone.utc` | Uses UTC timezone information |
| `timedelta()` | Represents a time duration |
| `data.copy()` | Creates a copy of a dictionary |
| `dict.update()` | Adds or updates dictionary values |
| `Header()` | Extracts information from request headers |
| `HTTPException()` | Returns an HTTP error response |
| `Depends()` | Executes a dependency before the endpoint |
| `try` | Contains code that may raise an exception |
| `except` | Handles exceptions raised inside the try block |

---

## 13. Important Interview Questions

### JWT Questions

**1. What is JWT?**

JWT stands for JSON Web Token. It is a compact, URL-safe token format used to transfer claims between two parties. It is commonly used for authentication and authorization.

**2. What are the three parts of a JWT?**

The three parts are:

1. Header
2. Payload
3. Signature

**3. What is the purpose of the JWT header?**

The header contains metadata about the token, including its type and the signing algorithm.

**4. What is the purpose of the JWT payload?**

The payload contains claims, which represent information about the token or its subject, such as username and expiration time.

**5. What is the purpose of the JWT signature?**

The signature allows the receiving application to verify the integrity and authenticity of the token.

**6. Is JWT encrypted?**

A typical signed JWT is not encrypted. Its payload can be decoded by anyone who obtains it. The signature protects its integrity, not its confidentiality.

**7. What is HS256?**

HS256 is a symmetric JWT signing algorithm based on HMAC and SHA-256. The same secret key is used to sign and verify the token.

### Token-Based Authentication Questions

**8. What is token-based authentication?**

Token-based authentication is a mechanism in which the server generates a token after verifying the user's credentials. The client sends that token with subsequent requests to access protected resources.

**9. Why is JWT used in authentication?**

JWT provides a convenient way to represent authenticated user information and verify token integrity without requiring a traditional server-side session for every request.

**10. What happens when a user logs in successfully?**

The server verifies the credentials, generates a JWT, and returns the token to the client.

**11. Why is token expiration important?**

Token expiration limits how long a token can be used. It reduces the period during which a stolen token may remain valid.

**12. What is stateless authentication?**

Stateless authentication means that the server does not need to maintain a traditional session record for every authenticated client. It can validate a signed token using its verification key and the token's claims.

### FastAPI Questions

**13. What is Header() in FastAPI?**

`Header()` is used to extract values from HTTP request headers and make them available as function parameters.

**14. What is Depends() in FastAPI?**

`Depends()` is used for dependency injection. It allows FastAPI to execute a dependency function and provide its returned value to an endpoint.

**15. Why is Depends(verify_token) used in the secure endpoint?**

It ensures that token verification happens before the protected endpoint executes. If verification fails, FastAPI returns an error instead of allowing access.

**16. What is HTTP 401 Unauthorized?**

HTTP 401 indicates that the request does not contain valid authentication credentials.

**17. What is the difference between 401 and 403?**

- 401 Unauthorized: Authentication is missing or invalid.
- 403 Forbidden: The user is authenticated but does not have permission to access the requested resource.

**18. What happens when an expired JWT is submitted?**

The JWT verification process detects that the expiration time has passed and rejects the token. The application returns an authentication error.

### Implementation Questions

**19. What is the purpose of jwt.encode()?**

It creates a JWT from the supplied payload and signs it using the specified secret key and algorithm.

**20. What is the purpose of jwt.decode()?**

It decodes the JWT and verifies its signature and applicable claims, including expiration.

**21. What is the purpose of the `sub` claim?**

The `sub` claim identifies the subject of the token, commonly the user associated with the token.

**22. What is the purpose of the `exp` claim?**

The `exp` claim defines the expiration time after which the token must no longer be accepted.

**23. Why is the same secret key used during encoding and decoding?**

HS256 is a symmetric signing algorithm. The same secret key is required to generate and verify the token signature.

**24. What happens if the JWT is modified?**

If the payload or other signed content is modified, signature verification fails unless the token is correctly signed again using the appropriate secret key.

**25. Where should the JWT secret key be stored in a real application?**

It should be stored securely using environment variables or a secret management system, rather than hardcoding it in the source code.

**26. Should passwords be stored inside a JWT payload?**

No. A signed JWT is not encrypted by default, so its payload can be decoded. Sensitive information such as passwords should never be included.

**27. What is the difference between authentication and authorization?**

Authentication verifies who the user is. Authorization determines what an authenticated user is allowed to access.

**28. What is the difference between session-based and token-based authentication?**

Session-based authentication generally stores session information on the server and identifies the session using a session ID. Token-based authentication uses a token that the server can verify to establish the user's authenticated identity.

---

## 14. Key Takeaways

- Authentication verifies the identity of a user.
- JWT stands for JSON Web Token.
- A JWT contains a header, payload, and signature.
- HS256 is a symmetric signing algorithm.
- `jwt.encode()` generates and signs a token.
- `jwt.decode()` verifies and decodes a token.
- `SECRET_KEY` is used to sign and verify the token.
- `sub` identifies the subject of the token.
- `exp` specifies the token expiration time.
- `datetime.now(timezone.utc)` obtains the current UTC time.
- `timedelta(minutes=30)` represents a 30-minute duration.
- `Header()` extracts the token from the request header.
- `Depends()` executes token verification before the protected endpoint.
- HTTP 401 indicates an authentication failure.
- A valid token allows access to the protected endpoint.
- An invalid or expired token is rejected.

**Final Understanding:** The implementation demonstrates JWT-based authentication in FastAPI. A user first logs in with valid credentials, receives a signed JWT, and then sends that token in the request header to access protected endpoints. FastAPI verifies the token through dependency injection before allowing access to secure data.