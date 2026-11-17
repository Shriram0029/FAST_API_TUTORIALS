# OAuth2 + JWT Authentication in FastAPI

## 1. Introduction

Authentication is the process of verifying the identity of a user before allowing access to an application.

In the previous JWT implementation, the application accepted a username and password, generated a JWT, and required that token to access a protected endpoint.

In this implementation, authentication is improved by introducing:

- OAuth2 password flow.
- JWT-based access tokens.
- Password hashing using bcrypt.
- Automatic token extraction from request headers.
- Token validation before accessing protected routes.

FastAPI provides built-in security utilities that make it easier to implement these authentication mechanisms.

### 1.1 What is OAuth2?

OAuth2 stands for Open Authorization 2.0.

It is an authorization framework that allows applications to obtain limited access to protected resources using access tokens.

For example, an application may allow a user to authenticate and then use an access token to access protected API endpoints.

OAuth2 defines different authorization flows for different application types and use cases.

In this implementation, the OAuth2 password flow is demonstrated using:

```python
OAuth2PasswordBearer
OAuth2PasswordRequestForm
```

**Important:** The password flow is suitable for understanding the basic OAuth2 concepts, but it is not recommended for new production applications. Modern applications generally use Authorization Code Flow with PKCE through an authorization server.

### 1.2 What is JWT?

JWT stands for JSON Web Token.

It is a compact token format used to transfer claims between two parties.

In this implementation, JWT is used as the access token.

After successful login:

1. The application verifies the username and password.
2. It generates a JWT containing the user's identity.
3. It signs the token using a secret key.
4. It returns the token to the client.
5. The client sends the token when accessing protected endpoints.

### 1.3 OAuth2 vs JWT

OAuth2 and JWT are not the same thing.

| OAuth2 | JWT |
|---|---|
| Authorization framework | Token format |
| Defines authorization flows | Defines how claims are represented |
| Describes how clients obtain and use access tokens | Can be used as an access token |
| Defines roles for clients, users, and authorization servers | Contains header, payload, and signature |

OAuth2 can use JWT access tokens, but it can also use other token formats.

---

# 2. Understanding the Imports

The implementation uses the following imports:

```python
from fastapi import FastAPI, Header, HTTPException, Depends
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
```

### 2.1 FastAPI

```python
from fastapi import FastAPI
```

Imports the FastAPI class used to create the application and define API endpoints.

### 2.2 Header

```python
from fastapi import Header
```

Used to extract values from HTTP request headers.

It was used in the previous implementation to manually extract the token from a custom header.

In the current implementation, `OAuth2PasswordBearer` handles token extraction, so `Header` is no longer required.

### 2.3 HTTPException

```python
from fastapi import HTTPException
```

Used to return HTTP error responses.

For example, status code 401 is returned when the submitted credentials or token are invalid.

### 2.4 Depends

```python
from fastapi import Depends
```

Used for dependency injection.

It allows FastAPI to execute functions such as `verify_token()` before executing protected endpoints.

### 2.5 JWT

```python
from jose import jwt
```

Imports JWT functionality from the Python JOSE library.

Important methods:

- `jwt.encode()` generates and signs a JWT.
- `jwt.decode()` decodes and verifies a JWT.

### 2.6 OAuth2PasswordBearer

```python
from fastapi.security import OAuth2PasswordBearer
```

This FastAPI security utility extracts a Bearer token from the Authorization request header.

It also declares an OAuth2 security scheme in the generated OpenAPI documentation.

### 2.7 OAuth2PasswordRequestForm

```python
from fastapi.security import OAuth2PasswordRequestForm
```

This utility extracts the username and password submitted through form data.

It is used by the login endpoint to receive the user's credentials in the OAuth2 password form format.

### 2.8 datetime, timedelta, timezone

Used to calculate the access token's expiration time.

### 2.9 CryptContext

```python
from passlib.context import CryptContext
```

Used for password hashing and password verification.

It provides an interface for managing password-hashing algorithms such as bcrypt.

---

# 3. JWT Configuration

```python
SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

These variables configure JWT generation and validation.

### 3.1 SECRET_KEY

The secret key is used to sign and verify the JWT.

```python
SECRET_KEY = "mysecret"
```

The same secret key is used when generating and verifying the token.

If a token is modified or signed with an incorrect secret, signature verification fails.

In a real application, the secret key should be strong, randomly generated, and stored securely using environment variables or a secret manager.

### 3.2 ALGORITHM

```python
ALGORITHM = "HS256"
```

Specifies the signing algorithm used for the JWT.

HS256 uses HMAC with SHA-256.

It is a symmetric signing algorithm, meaning the same secret key is used for signing and verification.

### 3.3 ACCESS_TOKEN_EXPIRE_MINUTES

```python
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

Defines a configuration value representing the access token's lifetime in minutes.

**Note about the current implementation:** Although this variable is declared, the `create_token()` function currently uses `timedelta(minutes=30)` directly. The variable itself is not used yet.

A cleaner implementation would use:

```python
expire = datetime.now(timezone.utc) + timedelta(
    minutes=ACCESS_TOKEN_EXPIRE_MINUTES
)
```

---

# 4. Password Hashing

## 4.1 What is Password Hashing?

Password hashing is the process of converting a plain-text password into a one-way hash value.

Applications should not store users' original passwords directly in the database.

For example, suppose a user registers with:

```text
Password: 1234
```

Instead of storing the original password, the application stores a hashed representation.

Conceptually:

```text
Original Password: 1234

        |
        v

Password Hashing

        |
        v

Stored Hash: $2b$12$...
```

The actual hash is a long string.

When the user logs in, the application verifies the submitted password against the stored hash.

### 4.2 Why is Password Hashing Important?

**1. Password Protection**

If a database is exposed, password hashes are safer than storing original passwords.

**2. One-Way Transformation**

Secure password hashing algorithms are designed to make it computationally difficult to recover the original password from the hash.

**3. Verification Without Storing Plain Text**

The application can verify whether a submitted password matches the stored hash without storing the original password.

**4. Protection Against Common Password Attacks**

Password-hashing algorithms such as bcrypt are designed to make large-scale password guessing more expensive.

### 4.3 What is bcrypt?

bcrypt is a password-hashing algorithm designed specifically for securely storing passwords.

It includes a salt and a configurable work factor.

A salt is random data incorporated into password hashing so that identical passwords do not necessarily produce identical hashes.

The work factor controls how computationally expensive the hashing operation is.

Higher work factors make password guessing more expensive, although they also increase the time required for legitimate password verification.

## 4.4 Password Hashing Setup

```python
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
```

This creates a password-hashing context using bcrypt.

Understanding the arguments:

**schemes=["bcrypt"]**

Specifies bcrypt as the password-hashing algorithm.

**deprecated="auto"**

Allows Passlib to identify outdated hashing schemes and manage them according to the configured policy.

## 4.5 Dummy User Database

```python
fake_user_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("1234")
    }
}
```

This dictionary represents a simple dummy user database.

It stores one user with the username `admin`.

The password is hashed using:

```python
pwd_context.hash("1234")
```

The application stores the resulting hash rather than storing the original password as the database value.

For example, the structure is conceptually:

```python
{
    "admin": {
        "username": "admin",
        "hashed_password": "bcrypt_hash_value"
    }
}
```

The actual hash is generated when the application starts.

Since bcrypt uses a salt, the generated hash can be different each time the application starts, even for the same password.

**Important:** This is a dummy in-memory user database for learning. It is not a persistent database. In a real application, user records and password hashes would be stored in a database.

## 4.6 hash_password() Function

```python
def hash_password(password: str):
    return pwd_context.hash(password)
```

This function accepts a plain-text password and returns its bcrypt hash.

Example:

```python
hashed = hash_password("1234")
```

The returned value is a hashed password, not the original password.

**Note:** This helper function is defined in the current code but is not directly called elsewhere. The dummy database uses `pwd_context.hash("1234")` directly.

## 4.7 verify_password() Function

```python
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )
```

This function checks whether a submitted plain-text password matches a previously stored hash.

It accepts two parameters:

- `plain_password`: The password submitted by the user.
- `hashed_password`: The hash stored in the user database.

The `verify()` method checks the submitted password against the stored hash.

It returns:

- `True` if the password matches.
- `False` if the password does not match.

Example:

```python
verify_password("1234", stored_hash)
```

If the stored hash corresponds to `"1234"`, the result is `True`.

The application does not need to decrypt the hash to verify the password.

### Difference Between Hashing and Verification

| Hashing | Verification |
|---|---|
| Converts a plain-text password into a hash | Checks a submitted password against a stored hash |
| Uses `pwd_context.hash()` | Uses `pwd_context.verify()` |
| Used during registration or password creation | Used during login |
| Produces a hash string | Produces True or False |

---

# 5. OAuth2 Setup

```python
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")
```

This is one of the most important additions compared with the previous JWT implementation.

## 5.1 What is OAuth2PasswordBearer?

`OAuth2PasswordBearer` is a FastAPI security utility that extracts an access token from the Authorization header.

It expects the token to be supplied using the Bearer authentication scheme.

The standard format is:

```text
Authorization: Bearer <access_token>
```

For example:

```text
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

The utility extracts the token value and makes it available to the dependency function.

It does not independently verify the JWT signature. Token validation is performed later using `jwt.decode()`.

## 5.2 Understanding tokenUrl

```python
tokenUrl="login"
```

This specifies the URL where the client obtains the access token.

Here, the login endpoint is:

```text
POST /login
```

FastAPI also uses this information when generating the OpenAPI security documentation.

## 5.3 How OAuth2PasswordBearer Works

When a protected endpoint uses:

```python
token: str = Depends(oauth2_schema)
```

FastAPI executes the OAuth2 dependency.

The dependency:

1. Checks the Authorization header.
2. Expects the Bearer authentication scheme.
3. Extracts the token.
4. Provides the extracted token to the endpoint or another dependency.

If the Authorization header is missing or does not contain a Bearer token, the dependency rejects the request.

**Important:** `OAuth2PasswordBearer` extracts the token. It does not validate its signature, expiration, or user identity.

---

# 6. Login API – OAuth2 Password Form

## 6.1 What is OAuth2PasswordRequestForm?

`OAuth2PasswordRequestForm` is a FastAPI dependency that extracts username and password values from form data.

Unlike the previous implementation, where credentials were accepted as query parameters, this implementation uses form fields.

The request uses:

```text
Content-Type: application/x-www-form-urlencoded
```

The form contains:

- `username`
- `password`

## 6.2 Login API Code

```python
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = fake_user_db.get(form_data.username)

    if not user or not verify_password(
        form_data.password,
        user["hashed_password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials(invalid usernmae or password)"
        )

    access_token = create_token({
        "sub": form_data.username
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
```

## 6.3 Understanding the Code Step by Step

**1. Defining the Login Endpoint**

```python
@app.post("/login")
```

Creates a POST endpoint used for authentication.

**2. Receiving the Form Data**

```python
form_data: OAuth2PasswordRequestForm = Depends()
```

FastAPI executes the `OAuth2PasswordRequestForm` dependency and extracts the username and password from the submitted form.

The credentials can be accessed using:

```python
form_data.username
form_data.password
```

`Depends()` tells FastAPI to resolve the form dependency before calling the login function.

**3. Finding the User**

```python
user = fake_user_db.get(form_data.username)
```

The dictionary's `get()` method searches for the submitted username.

For example, if the username is `admin`, it retrieves the corresponding user record.

If the username does not exist, `.get()` returns `None`.

**4. Verifying the Credentials**

```python
if not user or not verify_password(
    form_data.password,
    user["hashed_password"]
):
```

This condition checks two things:

- Whether the user exists.
- Whether the submitted password matches the stored password hash.

The `or` operator means that if either condition is true, authentication is rejected.

For example:

| Username | Password | Result |
|---|---|---|
| admin | 1234 | Valid |
| admin | 1111 | Invalid |
| user | 1234 | Invalid |
| user | 1111 | Invalid |

**5. Handling Invalid Credentials**

```python
raise HTTPException(
    status_code=401,
    detail="Invalid credentials(invalid usernmae or password)"
)
```

If the user does not exist or the password does not match, the application returns a 401 Unauthorized response.

**6. Creating the Access Token**

```python
access_token = create_token({
    "sub": form_data.username
})
```

If authentication is successful, the application calls `create_token()`.

The username is stored in the JWT payload using the `sub` claim.

The token also contains the expiration claim added by `create_token()`.

**7. Returning the Token**

```python
return {
    "access_token": access_token,
    "token_type": "bearer"
}
```

The login endpoint returns two values:

- `access_token`: The generated JWT.
- `token_type`: Specifies that the token uses the Bearer authentication scheme.

Example response:

```json
{
    "access_token": "generated_jwt_token",
    "token_type": "bearer"
}
```

The actual token is a long encoded string.

---

# 7. Token Generation – create_token()

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

This function generates and signs the JWT after successful authentication.

### Step-by-step explanation

**1. Copying the User Data**

```python
to_encode = data.copy()
```

Creates a copy of the original dictionary.

**2. Calculating Expiration Time**

```python
expire = datetime.now(timezone.utc) + timedelta(minutes=30)
```

Calculates an expiration time 30 minutes after the current UTC time.

**3. Adding the Expiration Claim**

```python
to_encode.update({
    "exp": expire
})
```

Adds the `exp` claim to the token payload.

**4. Generating the JWT**

```python
token = jwt.encode(
    to_encode,
    SECRET_KEY,
    algorithm=ALGORITHM
)
```

Signs the payload using the configured secret key and HS256 algorithm.

**5. Returning the Token**

```python
return token
```

Returns the generated JWT to the login endpoint.

---

# 8. Token Validation – verify_token()

Token validation ensures that the access token submitted by a client is valid before allowing access to a protected endpoint.

## 8.1 Code

```python
def verify_token(token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return username

    except jwt.JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
```

## 8.2 Understanding the Code Step by Step

**1. Receiving the Token**

```python
token: str = Depends(oauth2_schema)
```

FastAPI executes the `oauth2_schema` dependency.

The dependency extracts the Bearer token from the Authorization header.

The extracted token is passed into the `verify_token()` function.

**2. Using try and except**

```python
try:
```

The token decoding and validation process is placed inside a try block because invalid tokens can raise exceptions.

**3. Decoding and Verifying the JWT**

```python
payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM]
)
```

The `jwt.decode()` method verifies the token.

It checks:

- Whether the signature is valid.
- Whether the token was signed using an accepted algorithm.
- Whether the token has expired.

If validation succeeds, the decoded payload is returned as a dictionary.

**4. Extracting the Username**

```python
username: str = payload.get("sub")
```

The `get()` method retrieves the value associated with the `sub` claim.

For example:

```python
payload = {
    "sub": "admin",
    "exp": 1793790000
}
```

The extracted username becomes:

```text
admin
```

**5. Checking the Subject**

```python
if username is None:
    raise HTTPException(
        status_code=401,
        detail="Invalid token"
    )
```

A valid token for this application must contain a subject identifying the user.

If the `sub` claim is missing, the token is rejected.

**6. Returning the Username**

```python
return username
```

If validation succeeds, the username is returned.

The protected endpoint receives this value through dependency injection.

**7. Handling JWT Errors**

```python
except jwt.JWTError:
    raise HTTPException(
        status_code=401,
        detail="Invalid token"
    )
```

If JWT validation fails, the application returns a 401 Unauthorized response.

Examples include:

- Invalid signature.
- Malformed token.
- Expired token.

The code uses `jwt.JWTError` from the Python JOSE library to handle JWT-related errors.

---

# 9. Secure Routes – Protected Endpoint

## 9.1 What is a Protected Route?

A protected route is an API endpoint that requires successful authentication before allowing access.

For example, an application may allow anyone to access its login endpoint but restrict user information or other sensitive resources to authenticated users.

The protected endpoint in this implementation is:

```text
GET /protected
```

## 9.2 Code

```python
@app.get("/protected")
def protected_route(
    username: str = Depends(verify_token)
):
    return {
        "message": f"Hello {username}, you have access to this protected route!",
        "user": username
    }
```

### Understanding the Code Step by Step

**1. Defining the Endpoint**

```python
@app.get("/protected")
```

Creates a GET endpoint for accessing protected information.

**2. Using Dependency Injection**

```python
username: str = Depends(verify_token)
```

This is the most important part of the protected endpoint.

`Depends(verify_token)` tells FastAPI to execute the `verify_token()` function before executing the protected route.

The dependency:

1. Extracts the Bearer token.
2. Verifies the JWT.
3. Checks the expiration time.
4. Extracts the username from the `sub` claim.
5. Returns the username.

If verification fails, the protected endpoint is not executed.

**3. Returning the Protected Response**

```python
return {
    "message": f"Hello {username}, you have access to this protected route!",
    "user": username
}
```

If the token is valid, the endpoint returns a personalized success message.

Example response:

```json
{
    "message": "Hello admin, you have access to this protected route!",
    "user": "admin"
}
```

---

# 10. Complete Authentication Flow

The implementation can be understood through four stages.

### Stage 1 – User Login

1. The user submits the username and password.
2. `OAuth2PasswordRequestForm` extracts the form values.
3. The application searches for the username in `fake_user_db`.
4. `verify_password()` checks the submitted password against the stored hash.
5. If the credentials are incorrect, the application returns 401.
6. If the credentials are correct, token generation begins.

### Stage 2 – JWT Generation

1. The login endpoint calls `create_token()`.
2. The username is added to the payload using `sub`.
3. The expiration time is calculated.
4. The `exp` claim is added.
5. `jwt.encode()` signs the token using the secret key and HS256.
6. The access token is returned to the client.

### Stage 3 – Sending the Token

1. The client receives the access token.
2. The client stores the token securely.
3. When accessing a protected endpoint, the client sends the token using the Authorization header.
4. The token is sent using the Bearer scheme.

Request header:

```text
Authorization: Bearer <access_token>
```

### Stage 4 – Token Validation and Secure Access

1. `OAuth2PasswordBearer` extracts the token.
2. `verify_token()` receives the extracted token.
3. `jwt.decode()` validates the token.
4. The application checks for the `sub` claim.
5. The username is returned from the dependency.
6. The protected endpoint executes.
7. The application returns the protected response.

If validation fails, access is rejected.

---

# 11. Testing with Swagger UI

FastAPI automatically generates interactive API documentation.

Start the server:

```bash
python -m uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

The documentation contains:

- POST `/login`
- GET `/protected`

## 11.1 Testing Login API

**Endpoint:**

```text
POST /login
```

Steps:

1. Expand POST `/login`.
2. Click **Try it out**.
3. Enter the username: `admin`.
4. Enter the password: `1234`.
5. Click **Execute**.

Because `OAuth2PasswordRequestForm` is used, the credentials are submitted as form data rather than query parameters or JSON.

Expected response:

```json
{
    "access_token": "generated_jwt_token",
    "token_type": "bearer"
}
```

Copy the generated access token if testing manually.

## 11.2 Testing the Protected Route

**Endpoint:**

```text
GET /protected
```

There are two ways to test this endpoint.

**Method 1: Using the Authorize Button**

1. Click the **Authorize** button in Swagger UI.
2. Enter the username `admin`.
3. Enter the password `1234`.
4. Click **Authorize**.
5. Close the authorization dialog.
6. Expand GET `/protected`.
7. Click **Try it out**.
8. Click **Execute**.

Swagger UI uses the OAuth2 security scheme to obtain the token from the login endpoint and sends it using the Bearer scheme.

**Method 2: Manually Supplying the Token**

The request header must contain:

```text
Authorization: Bearer generated_jwt_token
```

The token must be the actual token returned by the login endpoint.

Expected response:

```json
{
    "message": "Hello admin, you have access to this protected route!",
    "user": "admin"
}
```

This confirms that the access token was successfully validated.

## 11.3 Testing Invalid Credentials

Try:

```text
Username: admin
Password: 1111
```

Expected response:

```text
401 Unauthorized
```

The application rejects the login because the submitted password does not match the stored password hash.

## 11.4 Testing Without a Token

Try accessing:

```text
GET /protected
```

without authenticating through Swagger UI or providing a Bearer token.

The request should be rejected because the OAuth2 dependency cannot extract a token.

## 11.5 Testing an Invalid Token

Submit an incorrect or modified Bearer token.

Expected response:

```text
401 Unauthorized
```

The JWT verification process rejects the token.

## 11.6 Testing an Expired Token

The token is configured to expire after 30 minutes.

After the expiration time, the token should no longer be accepted.

The application returns 401 when the expired token is submitted.

---

# 12. Important Differences from the Previous JWT Implementation

The previous implementation manually extracted a token using `Header()`.

The current implementation uses FastAPI's OAuth2 security utilities.

| Previous Implementation | Current Implementation |
|---|---|
| `Header(None)` | `OAuth2PasswordBearer` |
| Custom `token` header | Standard `Authorization: Bearer` header |
| Username and password as query parameters | Username and password as form data |
| Plain-text password comparison | Hashed password verification |
| Manually enters token header in Swagger | Swagger supports OAuth2 Authorize flow |
| `Depends(verify_token)` | `Depends(verify_token)` |

The current implementation is closer to a standard OAuth2 Bearer token authentication setup.

---

# 13. Important Concepts to Remember

| Concept | Purpose |
|---|---|
| OAuth2 | Authorization framework |
| JWT | Token format |
| OAuth2PasswordBearer | Extracts Bearer tokens from request headers |
| OAuth2PasswordRequestForm | Extracts username and password from form data |
| CryptContext | Manages password hashing and verification |
| bcrypt | Password-hashing algorithm |
| `pwd_context.hash()` | Generates a password hash |
| `pwd_context.verify()` | Checks a password against a stored hash |
| `jwt.encode()` | Generates and signs a JWT |
| `jwt.decode()` | Decodes and verifies a JWT |
| `Depends()` | Executes dependencies before endpoint functions |
| `sub` | Identifies the subject of a JWT |
| `exp` | Specifies the expiration time of a JWT |
| Bearer Token | Token sent through the Authorization header |

---

# 14. Important Interview Questions

## OAuth2 and JWT

### 1. What is OAuth2?

OAuth2 is an authorization framework that defines how applications obtain and use access tokens to access protected resources.

### 2. What is JWT?

JWT stands for JSON Web Token. It is a compact, URL-safe token format used to represent claims between two parties.

### 3. What is the difference between OAuth2 and JWT?

OAuth2 is an authorization framework, whereas JWT is a token format. OAuth2 can use JWT as an access token.

### 4. What is OAuth2PasswordBearer?

It is a FastAPI security utility that extracts a Bearer token from the Authorization request header and declares an OAuth2 security scheme in the API documentation.

### 5. What is OAuth2PasswordRequestForm?

It is a FastAPI dependency that extracts username and password values submitted as form data.

### 6. What is a Bearer token?

A Bearer token is an access token that a client presents to a server to access a protected resource. It is commonly sent using the Authorization header.

### 7. What is the format of a Bearer token?

```text
Authorization: Bearer <access_token>
```

### 8. What is the OAuth2 password flow?

It is a flow in which a client submits a user's username and password to obtain an access token. This flow is useful for understanding OAuth2 basics but is not recommended for new production applications.

## Password Hashing

### 9. What is password hashing?

Password hashing converts a plain-text password into a one-way hash value that can be stored securely.

### 10. Why should passwords be hashed?

Passwords should be hashed so that the original passwords are not directly stored in the database. If the database is exposed, attackers do not immediately obtain the original passwords.

### 11. What is bcrypt?

bcrypt is a password-hashing algorithm designed for securely storing passwords. It uses a salt and a configurable work factor.

### 12. What is the purpose of CryptContext?

`CryptContext` provides a common interface for configuring password-hashing algorithms and verifying passwords.

### 13. What is the difference between hash() and verify()?

- `hash()` generates a password hash from a plain-text password.
- `verify()` checks whether a submitted password matches an existing hash.

### 14. Can a hashed password be decrypted?

Secure password hashes are designed to be one-way. The original password is not recovered through decryption. Instead, the submitted password is checked against the stored hash.

### 15. What is a salt in password hashing?

A salt is random data added to the password-hashing process so that identical passwords can produce different hashes.

## Secure Routes and Token Validation

### 16. What is a protected route?

A protected route is an endpoint that requires successful authentication before allowing access.

### 17. What is the purpose of Depends()?

`Depends()` is FastAPI's dependency injection mechanism. It allows a function to be executed before an endpoint and supplies its returned value to the endpoint.

### 18. What is the purpose of verify_token()?

It validates the JWT, checks its claims, extracts the username, and returns the authenticated user's identity.

### 19. What happens if a JWT is expired?

The token validation process rejects the expired token, and the application returns an authentication error.

### 20. What happens if a JWT is modified?

The signature verification fails because the modified token no longer matches the original signature.

### 21. What is the difference between 401 and 403?

- 401 Unauthorized: Authentication is missing or invalid.
- 403 Forbidden: The user is authenticated but does not have permission to access the resource.

### 22. What is the purpose of the sub claim?

The `sub` claim identifies the subject of the token, commonly the authenticated user.

### 23. What is the purpose of the exp claim?

The `exp` claim defines the token's expiration time. After that time, the token must no longer be accepted.

### 24. Does OAuth2PasswordBearer validate a JWT?

No. It extracts the Bearer token from the request header. The actual JWT signature and claim validation must be performed separately using a JWT library.

### 25. What is the difference between authentication and authorization?

Authentication verifies the identity of a user. Authorization determines what resources or actions that authenticated user is permitted to access.

---

# 15. Important Practical Notes

The current implementation is a learning example. A few details are important when moving toward real applications.

**1. Use a Secure Secret Key**

Avoid hardcoding:

```python
SECRET_KEY = "mysecret"
```

Use a strong randomly generated secret stored outside the source code.

**2. Use a Persistent User Database**

The current `fake_user_db` is an in-memory Python dictionary. It is not persistent and does not store users permanently.

A real application should retrieve user records from a database.

**3. Use the Expiration Configuration**

The current code declares `ACCESS_TOKEN_EXPIRE_MINUTES` but uses a hardcoded 30-minute duration inside `create_token()`.

The function can use the configuration variable to avoid duplication.

**4. Handle Password Hashing Safely**

The dummy database generates a hash when the application starts. A real application should hash passwords during user registration and store the resulting hash in the database.

**5. Use an Appropriate Authentication Flow**

The OAuth2 password flow shown here is for learning. For new production applications, use an appropriate authorization flow such as Authorization Code with PKCE, generally through a dedicated authorization server.

**6. Use HTTPS**

Tokens and login credentials should be transmitted over HTTPS so they are protected in transit.

**7. Handle Authentication Errors Carefully**

Catch the appropriate JWT and password-verification exceptions instead of using broad exception handling. Avoid exposing sensitive internal error details to clients.

---

# 16. Key Takeaways

- OAuth2 is an authorization framework.
- JWT is a token format.
- OAuth2PasswordBearer extracts Bearer tokens from request headers.
- OAuth2PasswordRequestForm receives credentials through form data.
- Passwords should not be stored as plain text.
- bcrypt is used for password hashing.
- CryptContext manages password hashing and verification.
- `pwd_context.hash()` generates a password hash.
- `pwd_context.verify()` verifies a submitted password.
- `jwt.encode()` generates and signs an access token.
- `jwt.decode()` validates and decodes a token.
- `Depends()` executes the token verification dependency.
- Protected routes require valid authentication.
- Expired and invalid tokens must be rejected.
- The standard Bearer token format is `Authorization: Bearer <token>`.

**Final Understanding:** This implementation combines OAuth2 utilities, JWT, and bcrypt password hashing to build a more complete authentication mechanism in FastAPI. The user first submits credentials through the login endpoint. The application verifies the password hash and generates a JWT. The client then sends that token using the Bearer scheme, and FastAPI validates it before granting access to protected routes.