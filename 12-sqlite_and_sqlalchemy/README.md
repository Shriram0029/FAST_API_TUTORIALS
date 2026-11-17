# Database Integration with FastAPI (SQLite)

## 1. What is SQLite?

SQLite is a lightweight, serverless, self-contained relational database management system (RDBMS). It is used to store and manage structured data in tables.

Unlike databases such as MySQL and PostgreSQL, SQLite does not require a separate database server to run. The entire database is stored in a single file, usually with the `.db` extension.

For example:

```text
test.db
```

This file contains the database structure, tables, and stored records.

### Important Features of SQLite

1. **Serverless:** SQLite does not require a separate database server. The application directly communicates with the database file.
2. **Lightweight:** It is simple to set up and requires very few resources.
3. **Self-contained:** The database is stored in a single file.
4. **Zero Configuration:** No separate database installation or server configuration is required.
5. **Relational Database:** Data is organized into tables containing rows and columns.
6. **ACID Compliant:** It supports reliable transactions through Atomicity, Consistency, Isolation, and Durability.

### Why is SQLite used with FastAPI?

SQLite is commonly used while learning FastAPI because it is easy to configure and does not require a separate database server.

It is suitable for:
- Learning database integration.
- Small applications and prototypes.
- Local development and testing.
- Applications that need a simple file-based database.

---

## 2. Setting Up the Database

Python provides a built-in module called `sqlite3` to work with SQLite databases.

Therefore, there is no need to install a separate SQLite Python package.

### Importing Required Modules

```python
import sqlite3
from fastapi import FastAPI
```

**sqlite3:**

The `sqlite3` module provides the functionality required to connect to SQLite databases, execute SQL queries, create tables, insert records, update records, and retrieve data.

**FastAPI:**

FastAPI is used to create API endpoints through which clients can communicate with the application.

### Creating the FastAPI Application

```python
app = FastAPI()
```

The `FastAPI()` class creates the application instance.

The `app` object is used to define API routes using decorators such as `@app.get()` and `@app.post()`.

### Establishing a Database Connection

```python
conn = sqlite3.connect("test.db", check_same_thread=False)
```

The `sqlite3.connect()` method establishes a connection to the SQLite database.

**Understanding the parameters:**

- `test.db`: Specifies the database file name.
- `check_same_thread=False`: Allows the database connection to be accessed from threads other than the thread in which it was originally created.

If the specified database file does not exist, SQLite automatically creates it.

**What is `conn`?**

`conn` represents the database connection object. It acts as the communication link between the FastAPI application and the SQLite database.

Through this connection, the application can execute SQL statements and interact with the database.

**What is `check_same_thread=False`?**

By default, SQLite checks whether the connection is being used from the same thread in which it was created.

Setting this parameter to `False` disables that particular check. This can be useful in a FastAPI application where requests may be handled across different threads.

However, it does not make a connection automatically thread-safe. Concurrent access must still be managed carefully. For larger applications, managing connections per request is generally preferable.

### Creating a Cursor Object

```python
cursor = conn.cursor()
```

A cursor is an object used to execute SQL statements against the database.

It acts as an interface through which Python sends SQL commands to SQLite.

For example, the cursor can execute commands such as:

- `CREATE TABLE`
- `INSERT`
- `SELECT`
- `UPDATE`
- `DELETE`

**Difference between Connection and Cursor:**

- Connection (`conn`): Establishes communication with the database.
- Cursor (`cursor`): Executes SQL statements through that connection.

### Creating a Table

```python
cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY,
    title TEXT,
    completed TEXT
)
""")
```

The `execute()` method executes the SQL statement provided to it.

Here, the SQL command creates a table named `todos`.

**Understanding the SQL statement:**

**CREATE TABLE:**

This SQL command is used to create a new table inside the database.

**IF NOT EXISTS:**

This condition checks whether a table with the specified name already exists.

If the table exists, SQLite does not create another copy. If it does not exist, SQLite creates it.

This prevents errors when the application is restarted and the table has already been created.

**Table Structure:**

The `todos` table contains three columns:

| Column | Data Type | Description |
|---|---|---|
| id | INTEGER | Stores the unique identifier of each todo |
| title | TEXT | Stores the title or description of the todo |
| completed | TEXT | Stores the completion status |

**Understanding INTEGER PRIMARY KEY:**

The `id` column is defined as `INTEGER PRIMARY KEY`.

It uniquely identifies each record in the table. In SQLite, an `INTEGER PRIMARY KEY` column normally aliases the internal row identifier and can automatically receive an integer value when one is not supplied.

**Understanding TEXT:**

The `TEXT` data type is used to store text values, such as task titles and completion status.

For example:

- `Learn FastAPI`
- `Complete database integration`
- `True`
- `False`

For a real application, a completion status can also be represented using an integer or a Boolean-like constraint.

### Committing the Changes

```python
conn.commit()
```

The `commit()` method saves the changes made to the database.

Database operations such as creating tables, inserting records, updating records, and deleting records are performed within transactions.

Calling `commit()` makes the pending transaction changes permanent.

Without committing a transaction, changes may not be permanently saved.

---

## 3. Connecting FastAPI with SQLite

After establishing the database connection and creating the table, FastAPI can expose API endpoints to communicate with the application.

### Creating a GET Endpoint

```python
@app.get("/")
def home():
    return {
        "message": "SQLITE connection fine"
    }
```

**Understanding the code:**

- `@app.get("/")`: Defines a GET endpoint at the root URL.
- `def home()`: Defines the function executed when the endpoint is requested.
- `return`: Sends a Python dictionary as a JSON response.

When a client sends a GET request to the root endpoint, FastAPI executes the `home()` function and returns the response.

**Expected Response:**

```json
{
    "message": "SQLITE connection fine"
}
```

### Important Understanding

The current endpoint returns a success message. It does not actually execute a database query.

The database connection and table creation happen when the Python application starts, while the GET endpoint simply returns a message.

To retrieve or modify records, additional endpoints must be implemented using SQL queries.

### Execution Flow

1. The application imports the `sqlite3` and `FastAPI` modules.
2. A FastAPI application instance is created.
3. SQLite establishes a connection with `test.db`.
4. A cursor object is created to execute SQL statements.
5. The `CREATE TABLE IF NOT EXISTS` command creates the `todos` table if it does not already exist.
6. `conn.commit()` saves the table creation operation.
7. FastAPI defines the root GET endpoint.
8. When the client sends a GET request, the endpoint returns a JSON response.

### Running the Application

Open the terminal inside the topic folder and execute:

```bash
python -m uvicorn main:app --reload
```

**Command Explanation:**

- `python -m uvicorn`: Runs Uvicorn using the current Python environment.
- `main`: Refers to the Python file `main.py`.
- `app`: Refers to the FastAPI application instance.
- `--reload`: Automatically restarts the server when code changes are detected.

The application runs at:

```text
http://127.0.0.1:8000
```

### Testing Through Swagger UI

Open the following URL in a browser:

```text
http://127.0.0.1:8000/docs
```

Swagger UI provides an interactive interface to test the API endpoints.

Execute the GET `/` endpoint.

Expected response:

```json
{
    "message": "SQLITE connection fine"
}
```

---

## 4. SQLite vs SQLAlchemy

SQLite and SQLAlchemy are related to database management, but they are not the same thing.

### SQLite

SQLite is a relational database management system.

It stores data in a database file and supports SQL commands to create, retrieve, update, and delete records.

When using Python, the built-in `sqlite3` module allows an application to communicate directly with SQLite.

### SQLAlchemy

SQLAlchemy is a Python SQL toolkit and Object Relational Mapper (ORM).

It provides a higher-level way to interact with databases using Python objects and classes instead of writing every SQL query manually.

It also supports multiple database systems, including SQLite, PostgreSQL, and MySQL.

### Difference Between SQLite and SQLAlchemy

| Feature | SQLite | SQLAlchemy |
|---|---|---|
| Type | Database management system | Python SQL toolkit and ORM |
| Purpose | Stores and manages data | Provides an interface to interact with databases |
| Database Server | Not required | Depends on the database being used |
| Querying | Uses SQL statements | Supports SQL expressions and ORM operations |
| Database Support | SQLite only | Multiple database systems |
| Installation | Python provides the `sqlite3` module | Requires installing SQLAlchemy |
| Data Storage | Stores data in a database file | Does not itself store data |

### Can SQLite and SQLAlchemy Be Used Together?

Yes. SQLAlchemy can use SQLite as its database backend.

For example:

- SQLite acts as the database where the data is stored.
- SQLAlchemy acts as the interface through which Python interacts with the database.
- FastAPI exposes API endpoints to clients.

Therefore, SQLite and SQLAlchemy are not alternatives to each other. They can work together in the same application.

### Direct SQLite vs SQLAlchemy

**Using SQLite directly:**

```python
cursor.execute(
    "SELECT * FROM todos"
)
```

Here, SQL statements are written and executed directly using the `sqlite3` module.

**Using SQLAlchemy:**

```python
todos = db.query(Todo).all()
```

Here, the application uses SQLAlchemy ORM methods to retrieve records represented by Python model objects.

---

## 5. Important Interview Questions

### 1. What is SQLite?

SQLite is a lightweight, serverless relational database management system that stores data in a single file. It does not require a separate database server.

### 2. Why is SQLite used with FastAPI?

SQLite is easy to configure, lightweight, and does not require a separate database server. It is useful for learning, local development, testing, and small applications.

### 3. What is the purpose of the sqlite3 module?

The `sqlite3` module is a built-in Python module that allows applications to connect to SQLite databases and execute SQL statements.

### 4. What is a database connection?

A database connection is the communication link between an application and a database. It allows the application to execute database operations.

### 5. What is a cursor in SQLite?

A cursor is an object used to execute SQL statements and retrieve query results through a database connection.

### 6. What is the purpose of `cursor.execute()`?

The `execute()` method executes an SQL statement against the database. It can be used for creating tables, inserting records, retrieving records, updating records, and deleting records.

### 7. What is the purpose of `conn.commit()`?

The `commit()` method permanently saves the changes made during the current database transaction.

### 8. What is the use of `CREATE TABLE IF NOT EXISTS`?

It creates a table only if the table does not already exist. This prevents errors caused by attempting to create an existing table.

### 9. What is `check_same_thread=False`?

It disables SQLite's default check that restricts a connection to the thread in which it was created. It does not automatically make concurrent access safe.

### 10. What is the difference between SQLite and SQLAlchemy?

SQLite is a relational database management system used to store data, whereas SQLAlchemy is a Python toolkit and ORM used to interact with databases.

### 11. Does SQLite require a separate database server?

No. SQLite is serverless and stores the database directly in a file.

### 12. What happens if the database file does not exist?

When `sqlite3.connect()` is called with a database filename that does not exist, SQLite automatically creates the database file.

### 13. What is the purpose of a primary key?

A primary key uniquely identifies each record in a database table. It prevents duplicate identification of records.

### 14. What is the difference between `execute()` and `commit()`?

`execute()` runs an SQL statement, whereas `commit()` saves the transaction changes permanently.

### 15. Does the current FastAPI GET endpoint retrieve records from SQLite?

No. The current GET endpoint only returns a JSON message. It does not execute a database query. Additional SQL operations and API endpoints are required to retrieve or modify records.

---

## 6. Key Takeaways

- SQLite is a lightweight, serverless relational database.
- SQLite stores its data in a single database file.
- Python provides the built-in `sqlite3` module for database operations.
- `sqlite3.connect()` establishes a database connection.
- `cursor()` creates an object for executing SQL statements.
- `cursor.execute()` executes SQL commands.
- `CREATE TABLE IF NOT EXISTS` creates a table only when it does not already exist.
- `conn.commit()` saves database changes.
- FastAPI provides API endpoints through which clients can communicate with the application.
- SQLite and SQLAlchemy are different technologies and can also be used together.

**Note:** This implementation demonstrates the initial SQLite connection and table setup. It does not yet implement CRUD operations or SQLAlchemy integration.