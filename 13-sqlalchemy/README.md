# Database Integration with FastAPI (SQLAlchemy)

## 1. What is SQLAlchemy?

SQLAlchemy is a Python SQL toolkit and Object Relational Mapper (ORM) that allows Python applications to communicate with relational databases.

It provides a convenient way to interact with databases using Python classes and objects instead of writing SQL queries manually for every database operation.

SQLAlchemy supports multiple relational databases, including:

- SQLite
- MySQL
- PostgreSQL
- Oracle
- Microsoft SQL Server

### What is ORM?

ORM stands for **Object Relational Mapping**.

It is a technique that connects objects in a programming language with tables in a relational database.

Normally, databases store information in tables containing rows and columns. In Python, information is represented using classes and objects.

ORM acts as a bridge between these two structures.

For example:

In a database, a table may look like this:

| id | title | completed |
|---|---|---|
| 1 | Learn FastAPI | False |
| 2 | Learn SQLAlchemy | True |

In Python, the same table can be represented using a class:

```python
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    completed = Column(String)
```

Here:

- `Todo` is a Python class.
- `todos` is the corresponding database table.
- `id`, `title`, and `completed` represent the table columns.

SQLAlchemy ORM maps the Python class to the database table and allows the application to work with database records as Python objects.

### Why is SQLAlchemy used with FastAPI?

SQLAlchemy is commonly used with FastAPI to manage database operations.

It provides several advantages:

1. **Object Relational Mapping:** Database tables can be represented using Python classes.
2. **Multiple Database Support:** It supports different relational database systems.
3. **Reduced SQL Writing:** Many database operations can be performed using Python methods.
4. **Database Session Management:** It provides sessions to manage database operations and transactions.
5. **Maintainability:** Database logic can be organized using models and reusable operations.
6. **Flexibility:** Developers can use ORM operations as well as direct SQL queries when required.

---

## 2. Installing SQLAlchemy

SQLAlchemy is an external Python package, so it must be installed before using it.

Open the VS Code terminal and execute:

```bash
pip install sqlalchemy
```

Alternatively, use:

```bash
python -m pip install sqlalchemy
```

The second command installs SQLAlchemy using the Python interpreter associated with the current environment.

### Verifying the Installation

To verify whether SQLAlchemy is installed, execute:

```bash
pip show sqlalchemy
```

If the package is installed, the terminal displays information such as its version, installation location, and dependencies.

### Importing Required Modules

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import Column, Integer, String
from fastapi import FastAPI, Depends
```

Each imported component has a specific responsibility.

**1. create_engine**

`create_engine()` creates the SQLAlchemy Engine.

The Engine is responsible for managing database connectivity and providing connections when database operations are performed.

**2. sessionmaker**

`sessionmaker` is used to create a factory for generating database sessions.

A session is used to perform database operations such as inserting, retrieving, updating, and deleting records.

**3. declarative_base**

`declarative_base()` creates a base class for defining SQLAlchemy ORM models.

All model classes inherit from this base class so that SQLAlchemy can identify and manage them.

**4. Session**

`Session` represents the SQLAlchemy session type.

It is used as a type annotation to indicate that a variable or function parameter represents a database session.

**5. Column**

`Column` is used to define individual columns inside a database table.

**6. Integer**

`Integer` represents a column that stores integer values.

**7. String**

`String` represents a column that stores string or text values.

**8. FastAPI**

`FastAPI` is used to create the application and define API endpoints.

**9. Depends**

`Depends` is FastAPI's dependency injection mechanism.

It allows an endpoint to receive required resources, such as a database session, without manually creating those resources inside every endpoint.

---

## 3. Setting Up the Database

### Creating the FastAPI Application

```python
app = FastAPI()
```

The `FastAPI()` class creates the application instance.

The `app` object is used to define API endpoints using decorators such as `@app.get()` and `@app.post()`.

### Defining the Database URL

```python
DATABASE_URL = "sqlite:///./test.db"
```

The database URL specifies which database SQLAlchemy should connect to.

SQLAlchemy uses this URL to identify the database type and its location.

**Understanding the URL:**

- `sqlite`: Specifies that SQLite is being used as the database.
- `///`: Indicates the SQLite database URL format for a file-based database.
- `./test.db`: Specifies the database file named `test.db` in the current working directory.

The `./` indicates a relative path.

If the database file does not exist, SQLite can create it when the application first connects to it.

### Creating the Database Engine

```python
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
```

The `create_engine()` function creates the SQLAlchemy Engine using the database URL.

The Engine acts as the central component responsible for database connectivity.

It manages the process of obtaining database connections whenever SQLAlchemy needs to communicate with the database.

**Understanding the parameters:**

**1. DATABASE_URL**

Specifies the database to which SQLAlchemy should connect.

In this implementation, it points to the SQLite database file `test.db`.

**2. connect_args**

This parameter allows additional connection arguments to be passed to the database driver.

Here, the argument is:

```python
{"check_same_thread": False}
```

SQLite normally restricts a database connection to the thread in which it was created.

Setting `check_same_thread=False` disables that particular restriction.

This is useful in FastAPI applications because synchronous endpoints may execute in different worker threads.

However, disabling this check does not automatically make a database connection safe for unrestricted concurrent use. SQLAlchemy sessions should be used carefully and should not be shared between concurrent requests.

### Understanding the Engine

The Engine is an important component of SQLAlchemy.

Its responsibilities include:

- Establishing database connectivity.
- Managing database connections.
- Providing connections for executing SQL statements.
- Acting as the connection interface between SQLAlchemy and the database.

**Important distinction:**

The Engine is not the same as a database session.

- Engine manages database connectivity.
- Session manages database operations and transactions for a particular unit of work.

---

## 4. Creating the Database Session

```python
sessionLocal = sessionmaker(bind=engine)
```

The `sessionmaker()` function creates a session factory.

A session factory is responsible for generating database session objects whenever the application needs to interact with the database.

**Understanding the code:**

- `sessionmaker`: Creates a factory for database sessions.
- `bind=engine`: Connects the session factory to the previously created SQLAlchemy Engine.
- `sessionLocal`: Stores the configured session factory.

Whenever `sessionLocal()` is called, a new database session is created.

For example:

```python
db = sessionLocal()
```

Here, `db` represents a new SQLAlchemy session.

The session can now be used to perform database operations.

### What is a Database Session?

A database session represents a working interaction between the application and the database.

It manages database operations within a unit of work.

A session can perform operations such as:

- Adding new records.
- Retrieving existing records.
- Updating records.
- Deleting records.
- Committing transactions.
- Rolling back unsuccessful transactions.

For example:

```python
db.add(todo)
db.commit()
```

Here:

- `db.add(todo)` adds an object to the session.
- `db.commit()` commits the pending changes to the database.

A session should be closed after its work is completed to release its associated resources.

---

## 5. Creating the Declarative Base

```python
Base = declarative_base()
```

The `declarative_base()` function creates a base class used for defining SQLAlchemy ORM models.

All ORM model classes inherit from this base class.

It provides SQLAlchemy with the information needed to identify the classes that represent database tables.

For example:

```python
class Todo(Base):
    pass
```

Here, `Todo` inherits from `Base`, which allows SQLAlchemy to treat it as an ORM model.

**Understanding the importance of Base:**

- It provides the common foundation for ORM model classes.
- It maintains metadata about the models.
- It helps SQLAlchemy understand the structure of database tables.
- It allows SQLAlchemy to create tables using the metadata information.

### What is Metadata?

Metadata represents information about database structures.

It contains details such as:

- Table names.
- Column names.
- Column data types.
- Primary keys.
- Constraints.
- Indexes.

SQLAlchemy uses this metadata when creating database tables.

---

## 6. Creating the Model (Table Definition)

```python
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(String, index=True)
```

A model is a Python class that represents a database table.

Here, the `Todo` class represents the `todos` table.

### Understanding Each Component

**1. class Todo(Base)**

Defines a Python class named `Todo`.

It inherits from `Base`, allowing SQLAlchemy to recognize it as an ORM model.

**2. __tablename__**

```python
__tablename__ = "todos"
```

`__tablename__` is a special class attribute used to specify the actual database table name.

Here, SQLAlchemy maps the `Todo` Python class to a database table named `todos`.

The Python class name and database table name do not have to be identical.

**3. id Column**

```python
id = Column(Integer, primary_key=True, index=True)
```

This defines the `id` column.

- `Column`: Declares a database column.
- `Integer`: Specifies the integer data type.
- `primary_key=True`: Makes this column the primary key.
- `index=True`: Requests an index for this column.

A primary key uniquely identifies each record in the table.

An index is a database structure that can improve the speed of certain queries.

**4. title Column**

```python
title = Column(String, index=True)
```

This defines the `title` column.

- `String`: Specifies that the column stores string values.
- `index=True`: Requests an index on the title column.

Example values:

- Learn FastAPI
- Learn SQLAlchemy
- Complete database integration

**5. completed Column**

```python
completed = Column(String, index=True)
```

This defines the `completed` column.

It stores the completion status of a todo item.

Example values:

- True
- False

In this implementation, the values are stored as strings because the column uses the `String` type.

A Boolean column or an integer representation could also be used for a completion status.

### Understanding the Complete Model

| Python Attribute | Database Column | Data Type | Purpose |
|---|---|---|---|
| id | id | Integer | Unique record identifier |
| title | title | String | Stores the todo title |
| completed | completed | String | Stores completion status |

**Important: Model vs Table**

A model is the Python representation of a database table.

The model defines the structure of the table, but defining the class alone does not immediately create the physical table in the database.

SQLAlchemy must be instructed to create the table using its metadata.

---

## 7. Creating the Table in the Database

```python
Base.metadata.create_all(bind=engine)
```

This statement creates the database tables defined by the SQLAlchemy models.

It uses the metadata information collected from all model classes that inherit from `Base`.

**Understanding the statement:**

**1. Base.metadata**

`Base.metadata` contains the database structure information associated with the declarative models.

It includes table names, columns, data types, primary keys, and other table definitions.

**2. create_all()**

The `create_all()` method checks the database for the tables registered in the metadata.

If a required table does not exist, SQLAlchemy creates it.

If the table already exists, it is not recreated.

**3. bind=engine**

The `bind=engine` argument specifies the database Engine through which SQLAlchemy should perform the table creation operations.

### Difference Between Model Creation and Table Creation

| Model Creation | Table Creation |
|---|---|
| Defines a Python class | Creates a physical database table |
| Uses `class Todo(Base)` | Uses `Base.metadata.create_all()` |
| Describes table structure | Applies the structure to the database |
| Exists in Python code | Exists inside the database |

### Important Note About create_all()

`create_all()` creates missing tables, but it does not automatically update an existing table when the model structure changes.

For example, if a new column is added to the `Todo` model after the table has already been created, `create_all()` will not automatically add that column to the existing database table.

For managing database schema changes, tools such as Alembic are commonly used.

---

## 8. Connecting FastAPI with the Database

After configuring the Engine, session factory, and ORM model, the next step is to make database sessions available to FastAPI endpoints.

### Creating the get_db() Function

```python
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
```

The `get_db()` function is used to provide a database session to FastAPI endpoints.

It creates a new session, provides it to the endpoint, and closes it after the request processing is completed.

### Understanding the Code Step by Step

**1. Creating a Session**

```python
db = sessionLocal()
```

This creates a new database session using the session factory.

The newly created session is stored in the variable `db`.

**2. Using try**

```python
try:
    yield db
```

The `try` block contains the code that provides the session to the application.

Here, `yield` temporarily provides the database session to the calling endpoint.

Unlike `return`, which ends the function, `yield` pauses the function and allows it to continue later.

FastAPI recognizes this as a dependency with cleanup logic.

The endpoint receives the yielded database session and uses it to perform database operations.

**3. Using finally**

```python
finally:
    db.close()
```

The `finally` block executes when the dependency's work is finished, including when an exception occurs during request processing.

`db.close()` closes the database session and releases its associated resources.

This prevents database sessions from remaining open unnecessarily.

### Why is yield Used Instead of return?

If `return` were used:

```python
def get_db():
    db = sessionLocal()
    return db
```

The function would return the session immediately and would not have a cleanup section that runs after the endpoint finishes using it.

With `yield`, FastAPI can:

1. Create the session.
2. Provide the session to the endpoint.
3. Allow the endpoint to use the session.
4. Resume the dependency after endpoint processing.
5. Execute the `finally` block.
6. Close the session.

Therefore, `yield` is useful for managing resources that must be cleaned up after a request.

---

## 9. Using Depends() in FastAPI

```python
@app.get("/home")
def home(db: Session = Depends(get_db)):
    return {
        "message": "DB Connection Successful"
    }
```

This endpoint demonstrates how FastAPI receives a database session through dependency injection.

### Understanding Depends()

`Depends()` is a FastAPI function used to declare dependencies.

A dependency is a resource or function that an endpoint requires to perform its work.

For example, an endpoint may require:

- A database session.
- Authentication information.
- User permissions.
- Common validation logic.

Instead of creating these resources manually inside every endpoint, FastAPI can provide them through dependency injection.

### Understanding the Endpoint

**1. @app.get("/home")**

Defines a GET endpoint at `/home`.

When a client sends a GET request to this URL, FastAPI executes the `home()` function.

**2. db: Session**

This is a type annotation.

It indicates that the `db` parameter is expected to contain a SQLAlchemy Session object.

**3. Depends(get_db)**

```python
db: Session = Depends(get_db)
```

This tells FastAPI to execute the `get_db()` dependency and provide its yielded database session to the endpoint.

The endpoint does not need to create the session manually.

**4. Returning the Response**

```python
return {
    "message": "DB Connection Successful"
}
```

The endpoint returns a Python dictionary, which FastAPI converts into a JSON response.

Expected response:

```json
{
    "message": "DB Connection Successful"
}
```

### Important Understanding

In the current implementation, the `db` session is injected into the endpoint, but it is not actually used to execute a database query.

The dependency creates and provides the session, and then closes it after the request.

Therefore, the returned message confirms that the endpoint executed, but it does not independently prove that a database query was successfully performed.

A real database query would be required to verify database access through the session.

---

## 10. Complete Execution Flow

The entire SQLAlchemy database integration process works in the following order.

1. The application imports SQLAlchemy and FastAPI components.
2. A FastAPI application instance is created.
3. The database URL specifies the SQLite database file.
4. `create_engine()` creates the SQLAlchemy Engine.
5. `sessionmaker()` creates a session factory connected to the Engine.
6. `declarative_base()` creates the base class for ORM models.
7. The `Todo` class is defined and mapped to the `todos` database table.
8. The model defines the table columns and their data types.
9. `Base.metadata.create_all(bind=engine)` creates the table if it does not already exist.
10. The `get_db()` function creates a new database session when required.
11. The `yield` statement provides the session to FastAPI.
12. `Depends(get_db)` injects the session into the endpoint.
13. The endpoint executes and returns its response.
14. After endpoint processing, the `finally` block closes the database session.

### Overall Architecture

```text
                 FastAPI Application
                         |
                         |
                   API Endpoint
                     /home
                         |
                         |
                  Depends(get_db)
                         |
                         |
                     get_db()
                         |
                         |
                  sessionLocal()
                         |
                         |
                 Database Session
                         |
                         |
                   SQLAlchemy
                         |
                         |
                      Engine
                         |
                         |
                    SQLite DB
                      test.db
```

---

## 11. Running the Application

Open the terminal inside the `sqlite_and_sqlalchemy` folder.

Execute:

```bash
python -m uvicorn main:app --reload
```

**Command Explanation:**

- `python -m uvicorn`: Runs Uvicorn using the active Python environment.
- `main`: Refers to the `main.py` file.
- `app`: Refers to the FastAPI application instance.
- `--reload`: Automatically restarts the application when code changes are detected.

The application runs at:

```text
http://127.0.0.1:8000
```

### Testing Through Swagger UI

Open the following URL:

```text
http://127.0.0.1:8000/docs
```

Swagger UI displays the available API endpoints.

1. Locate the GET `/home` endpoint.
2. Click **Try it out**.
3. Click **Execute**.
4. Observe the response.

Expected response:

```json
{
    "message": "DB Connection Successful"
}
```

---

## 12. SQLite vs SQLAlchemy

SQLite and SQLAlchemy are not the same technology.

| Feature | SQLite | SQLAlchemy |
|---|---|---|
| Type | Relational database management system | Python SQL toolkit and ORM |
| Purpose | Stores and manages data | Provides an interface to interact with databases |
| Data Storage | Stores data in a database file | Does not itself store data |
| Querying | Uses SQL statements | Supports ORM operations and SQL expressions |
| Database Support | SQLite only | Supports multiple database systems |
| Installation | Python provides the `sqlite3` module | Requires installing SQLAlchemy |
| Role | Database | Database interaction layer |

### Can SQLite and SQLAlchemy Work Together?

Yes.

In this implementation:

- SQLite is the actual database.
- SQLAlchemy provides the Python interface to communicate with SQLite.
- FastAPI exposes API endpoints.
- The SQLAlchemy session manages database operations.

Therefore, SQLAlchemy is not a replacement for SQLite. It is a tool that helps the application interact with SQLite and other supported databases.

---

## 13. Important Interview Questions

### 1. What is SQLAlchemy?

SQLAlchemy is a Python SQL toolkit and Object Relational Mapper that allows applications to interact with relational databases using Python objects and SQL expressions.

### 2. What is ORM?

ORM stands for Object Relational Mapping. It is a technique that maps Python classes to database tables and Python objects to database records.

### 3. Why is SQLAlchemy used with FastAPI?

SQLAlchemy is used to manage database operations through Python classes and objects. It provides database sessions, supports multiple databases, and helps organize database logic.

### 4. What is the purpose of create_engine()?

`create_engine()` creates the SQLAlchemy Engine, which manages database connectivity and provides connections for executing database operations.

### 5. What is an Engine in SQLAlchemy?

The Engine is the central component responsible for database connectivity. It manages connections between the application and the database.

### 6. What is sessionmaker()?

`sessionmaker()` creates a factory that generates SQLAlchemy database sessions. These sessions are used to perform database operations.

### 7. What is a database session?

A database session represents a unit of work with the database. It manages operations such as inserting, retrieving, updating, deleting, committing, and rolling back records.

### 8. What is declarative_base()?

`declarative_base()` creates a base class used for defining SQLAlchemy ORM models. Model classes inherit from this base class.

### 9. What is a model in SQLAlchemy?

A model is a Python class that represents a database table. Its attributes define the corresponding table columns.

### 10. What is __tablename__?

`__tablename__` is a special class attribute that specifies the name of the database table represented by an ORM model.

### 11. What is Base.metadata?

`Base.metadata` contains the structural information about the database tables defined using the declarative models.

### 12. What is the purpose of create_all()?

`Base.metadata.create_all()` creates the database tables defined in the metadata if they do not already exist.

### 13. What is the difference between create_all() and create_engine()?

`create_engine()` configures database connectivity, whereas `create_all()` creates the database tables using the model metadata.

### 14. What is Depends() in FastAPI?

`Depends()` is used for dependency injection. It allows FastAPI to provide required resources, such as database sessions, to endpoint functions.

### 15. Why is yield used in get_db()?

`yield` provides the database session to the endpoint while allowing the dependency function to resume after endpoint processing. This makes it possible to close the session in a cleanup section.

### 16. Why is db.close() used?

`db.close()` closes the SQLAlchemy session after its work is completed and releases its associated resources.

### 17. What is the difference between return and yield?

`return` ends a function and sends back a value. `yield` temporarily provides a value and pauses the function so that execution can resume later.

### 18. What is the purpose of check_same_thread=False?

It disables SQLite's default restriction that a connection must be used from the same thread in which it was created. It does not automatically make concurrent connection access safe.

### 19. Does SQLAlchemy support multiple databases?

Yes. SQLAlchemy supports relational databases such as SQLite, MySQL, PostgreSQL, Oracle, and Microsoft SQL Server.

### 20. Does create_all() update existing database tables?

No. `create_all()` creates missing tables but does not automatically modify existing tables when the model structure changes. Database migration tools such as Alembic are used for schema changes.

### 21. What is the difference between SQLite and SQLAlchemy?

SQLite is a relational database management system that stores data, whereas SQLAlchemy is a Python toolkit and ORM that allows applications to interact with databases.

### 22. Is the database session automatically closed in this implementation?

Yes. The `finally` block in `get_db()` executes after the dependency is no longer needed and calls `db.close()` to close the session.

### 23. Does the current `/home` endpoint execute a database query?

No. It receives a database session through dependency injection but does not use that session to execute a query. It only returns a JSON message.

---

## 14. Key Takeaways

- SQLAlchemy is a Python SQL toolkit and ORM.
- ORM maps Python classes to database tables.
- `create_engine()` creates the database Engine.
- `sessionmaker()` creates a database session factory.
- `Session` represents the database session type.
- `declarative_base()` creates the base class for ORM models.
- `Column`, `Integer`, and `String` define table columns and their data types.
- `__tablename__` specifies the database table name.
- `Base.metadata.create_all()` creates missing database tables.
- `get_db()` provides a database session to FastAPI.
- `yield` provides the session and allows cleanup after request processing.
- `Depends()` injects the database session into the endpoint.
- `db.close()` closes the session after the request.
- SQLite stores the data, while SQLAlchemy provides the interface to interact with it.

**Note:** This implementation covers SQLAlchemy installation, database configuration, model creation, table creation, and database session dependency injection. Actual CRUD operations using SQLAlchemy sessions will be covered separately.