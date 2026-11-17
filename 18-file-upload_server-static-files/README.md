# File Upload & Static Files in FastAPI

## 1. Introduction

File handling is an important feature in web applications. Many applications allow users to upload files such as images, PDFs, documents, and other file formats.

FastAPI provides built-in support for receiving uploaded files and serving static files.

In this implementation, two major operations are performed:

1. **File Upload:** Accepting a file from the client and saving it inside a folder on the server.
2. **Serving Static Files:** Making uploaded files accessible through a URL.

For example, a user uploads an image named `demo.png`. The application saves it inside the `uploads` folder and provides a URL through which the image can be accessed.

### 1.1 What is File Upload?

File upload is the process of transferring a file from a client to a server.

For example:

- A user selects an image from their computer.
- The user sends the image to a FastAPI endpoint.
- FastAPI receives the uploaded file.
- The application saves the file inside a server-side directory.

### 1.2 What are Static Files?

Static files are files that are served directly to clients without being generated dynamically for each request.

Examples include:

- Images (`.png`, `.jpg`, `.jpeg`)
- CSS files
- JavaScript files
- PDFs
- Other documents

In this implementation, the `uploads` folder contains the files that are made accessible through FastAPI's static file handling.

---

# 2. Understanding the Imports

```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
import os
import shutil
```

### 2.1 FastAPI

```python
from fastapi import FastAPI
```

Imports the FastAPI class used to create the application and define API endpoints.

### 2.2 UploadFile

```python
from fastapi import UploadFile
```

`UploadFile` is used to receive files uploaded by clients.

It provides information about the uploaded file, including:

- Filename
- Content type
- File contents
- File object

Example:

```python
file: UploadFile
```

This tells FastAPI that the endpoint expects an uploaded file.

### 2.3 File

```python
from fastapi import File
```

`File` is used to declare that a parameter should be received as file data.

Example:

```python
file: UploadFile = File(...)
```

The `...` means that the file is required.

If the client does not provide a file, FastAPI returns a request validation error.

### 2.4 HTTPException

```python
from fastapi import HTTPException
```

Used to return HTTP error responses.

For example:

```python
raise HTTPException(
    status_code=404,
    detail="file not found"
)
```

This returns a 404 Not Found response when the requested file does not exist.

### 2.5 StaticFiles

```python
from fastapi.staticfiles import StaticFiles
```

`StaticFiles` is provided by Starlette and integrated into FastAPI.

It allows the application to serve files from a directory through a URL path.

For example:

```python
app.mount(
    "/files",
    StaticFiles(directory=UPLOAD_DIRECTORY),
    name="files"
)
```

This makes the contents of the configured directory accessible under the `/files` URL prefix.

### 2.6 os

```python
import os
```

The `os` module provides functions for interacting with the operating system and filesystem.

In this implementation, it is used for:

- Checking whether a directory exists.
- Creating a directory.
- Joining directory and filename paths.
- Checking whether a file exists.

Important methods:

| Method | Purpose |
|---|---|
| `os.path.exists()` | Checks whether a file or directory exists |
| `os.makedirs()` | Creates a directory |
| `os.path.join()` | Combines directory and filename into a path |

### 2.7 shutil

```python
import shutil
```

The `shutil` module provides high-level file operations.

In this implementation, it is used to copy the uploaded file contents into a file on the server.

The method used is:

```python
shutil.copyfileobj()
```

---

# 3. Step 1 – Create the Upload Directory

```python
UPLOAD_DIRECTORY = "uploads"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
```

Before uploading files, the application needs a directory where those files can be stored.

Here, the directory name is:

```text
uploads
```

### 3.1 Understanding UPLOAD_DIRECTORY

```python
UPLOAD_DIRECTORY = "uploads"
```

This variable stores the directory name where uploaded files will be saved.

For example, after uploading a file, the project structure will look like:

```text
project/
│
├── main.py
│
└── uploads/
    └── demo.png
```

### 3.2 Checking Whether the Directory Exists

```python
if not os.path.exists(UPLOAD_DIRECTORY):
```

`os.path.exists()` checks whether the specified path exists.

It returns:

- `True` if the path exists.
- `False` if the path does not exist.

The `not` operator reverses the result.

Therefore, the condition checks whether the `uploads` directory does not exist.

### 3.3 Creating the Directory

```python
os.makedirs(UPLOAD_DIRECTORY)
```

If the directory does not exist, `os.makedirs()` creates it.

This prevents the application from trying to save uploaded files into a directory that has not been created.

**Why is this necessary?**

If the application tries to save a file inside a nonexistent directory, the file operation can fail with a filesystem error.

By checking and creating the directory during application startup, the application ensures that the upload location is available.

---

# 4. Step 2 – Static File Setup

```python
app.mount(
    "/files",
    StaticFiles(directory=UPLOAD_DIRECTORY),
    name="files"
)
```

This step configures the application to serve files from the `uploads` directory.

### 4.1 What is app.mount()?

`app.mount()` attaches another ASGI application to the main FastAPI application under a particular URL path.

It is commonly used to serve static files.

The method receives three important arguments.

**1. `/files`**

```python
"/files"
```

This is the URL prefix through which the files will be accessed.

For example:

```text
http://127.0.0.1:8000/files/demo.png
```

**2. StaticFiles(directory=UPLOAD_DIRECTORY)**

```python
StaticFiles(directory=UPLOAD_DIRECTORY)
```

This tells FastAPI to serve files from the `uploads` directory.

When a client requests a file under `/files`, the static file application searches for the corresponding file inside the configured directory.

**3. name="files"**

```python
name="files"
```

This assigns a name to the mounted application.

It can be useful for URL generation and route identification.

### 4.2 Understanding the URL Mapping

Suppose the following file exists:

```text
uploads/demo.png
```

Because the application is mounted at `/files`, the file can be accessed using:

```text
http://127.0.0.1:8000/files/demo.png
```

The mapping is:

| Server-side location | URL |
|---|---|
| `uploads/demo.png` | `/files/demo.png` |
| `uploads/photo.jpg` | `/files/photo.jpg` |
| `uploads/document.pdf` | `/files/document.pdf` |

The application does not need to create a separate GET endpoint for every image or document.

The `StaticFiles` application handles file serving automatically.

---

# 5. Step 3 – File Upload API

## 5.1 What is an Upload API?

An upload API allows clients to send files to the server through an HTTP request.

In this implementation, the upload endpoint is:

```text
POST /upload
```

It receives a file and saves it inside the `uploads` directory.

## 5.2 Code

```python
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    file_name = file.filename
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)

    if not file_name:
        raise HTTPException(
            status_code=400,
            detail="file not selected"
        )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "file uploaded successfully",
        "filename": file_name,
        "file_url": f"http://127.0.0.1:8000/files/{file_name}"
    }
```

## 5.3 Understanding the Code Step by Step

### 1. Defining the Upload Endpoint

```python
@app.post("/upload")
```

Creates a POST endpoint.

The client sends the uploaded file to this endpoint.

### 2. Receiving the File

```python
def upload_file(file: UploadFile = File(...)):
```

This function receives the uploaded file.

Understanding the components:

- `file`: The parameter name.
- `UploadFile`: Specifies the uploaded file type.
- `File(...)`: Declares the parameter as required file data.

FastAPI reads the uploaded file from the incoming multipart form request and provides it as an `UploadFile` object.

### 3. Getting the Filename

```python
file_name = file.filename
```

The `filename` attribute provides the name of the uploaded file.

For example, if the user uploads:

```text
demo.png
```

Then:

```python
file_name = "demo.png"
```

### 4. Creating the File Path

```python
file_path = os.path.join(
    UPLOAD_DIRECTORY,
    file_name
)
```

This combines the upload directory and filename.

For example:

```text
UPLOAD_DIRECTORY = uploads
file_name = demo.png
```

The resulting path is:

```text
uploads/demo.png
```

`os.path.join()` constructs the path using the appropriate path separator for the operating system.

### 5. Checking Whether a File Was Selected

```python
if not file_name:
    raise HTTPException(
        status_code=400,
        detail="file not selected"
    )
```

This checks whether a filename is available.

If the filename is missing, the application raises a 400 Bad Request error.

**Important:** In the current code, `os.path.join()` is executed before this check. For safer handling, validate `file_name` before constructing `file_path`.

### 6. Opening the File

```python
with open(file_path, "wb") as buffer:
```

This opens the destination file in write-binary mode.

Understanding the arguments:

- `file_path`: Location where the file will be saved.
- `"wb"`: Opens the file in write-binary mode.
- `buffer`: Variable representing the opened destination file.

**What is binary mode?**

Images, PDFs, and many other file formats contain binary data rather than ordinary text.

Therefore, files should be saved using binary mode.

The modes are:

| Mode | Purpose |
|---|---|
| `r` | Read text |
| `w` | Write text |
| `rb` | Read binary |
| `wb` | Write binary |

The `with` statement automatically closes the destination file after the block finishes, including when an exception occurs.

### 7. Copying the Uploaded File

```python
shutil.copyfileobj(file.file, buffer)
```

This copies the contents of the uploaded file into the destination file.

Understanding the arguments:

- `file.file`: The underlying file object containing the uploaded data.
- `buffer`: The destination file opened using `open()`.

The operation transfers the uploaded file contents into:

```text
uploads/demo.png
```

### 8. Returning the Response

```python
return {
    "message": "file uploaded successfully",
    "filename": file_name,
    "file_url": f"http://127.0.0.1:8000/files/{file_name}"
}
```

After successfully saving the file, the endpoint returns a JSON response.

It contains:

- `message`: Indicates that the upload was successful.
- `filename`: The name of the uploaded file.
- `file_url`: The URL through which the uploaded file can be accessed.

Example response:

```json
{
    "message": "file uploaded successfully",
    "filename": "demo.png",
    "file_url": "http://127.0.0.1:8000/files/demo.png"
}
```

---

# 6. Step 4 – Accessing the Uploaded File

Once a file is uploaded, it should be accessible through a URL.

The static file configuration already provides this functionality.

For example:

```text
http://127.0.0.1:8000/files/demo.png
```

When this URL is opened:

1. The request reaches the application mounted at `/files`.
2. `StaticFiles` identifies the requested filename.
3. It searches for the corresponding file inside the `uploads` directory.
4. If the file exists, it serves the file to the client.
5. If the file does not exist, the static file application returns a 404 response.

### 6.1 Understanding the GET File URL API in the Code

The code also contains:

```python
@app.get("/files/{file_name}")
def get_file(file_name: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="file not found"
        )

    return {
        "file_url": f"http://127.0.0.1:8000/files/{file_name}"
    }
```

This function is intended to:

1. Receive a filename through a path parameter.
2. Construct the corresponding file path.
3. Check whether the file exists.
4. Return the file URL if it exists.
5. Return 404 if it does not exist.

For example:

```text
GET /files/demo.png
```

If the file exists, the intended JSON response is:

```json
{
    "file_url": "http://127.0.0.1:8000/files/demo.png"
}
```

**Important routing detail:** In your current code, `app.mount("/files", ...)` is registered before `@app.get("/files/{file_name}")`. The mount handles requests under `/files`, so the later GET route is shadowed and will not normally execute. The actual file is served directly by `StaticFiles`.

Therefore, you do not need the separate GET endpoint to display or download uploaded files. The static file mount already handles that job.

The direct URL is the important part:

```text
http://127.0.0.1:8000/files/demo.png
```

---

# 7. Complete File Upload Flow

The complete process can be understood in the following stages.

### Stage 1 – Application Startup

1. FastAPI application is created.
2. The application checks whether the `uploads` directory exists.
3. If the directory does not exist, it is created.
4. Static file handling is configured using `app.mount()`.

### Stage 2 – File Selection and Upload

1. The client opens the API documentation.
2. The client selects a file.
3. The client sends a POST request to `/upload`.
4. FastAPI receives the file through `UploadFile`.
5. The application obtains the filename.

### Stage 3 – Saving the File

1. The destination file path is constructed using `os.path.join()`.
2. The destination file is opened in binary write mode.
3. `shutil.copyfileobj()` copies the uploaded file contents.
4. The file is saved inside the `uploads` directory.
5. The API returns the filename and file URL.

### Stage 4 – Serving the File

1. The client opens the returned file URL.
2. The request reaches the `/files` static file mount.
3. `StaticFiles` searches for the requested file inside `uploads`.
4. The file is returned to the client.

---

# 8. Testing with Swagger UI

FastAPI automatically generates interactive API documentation.

### 8.1 Start the Server

Run:

```bash
python -m uvicorn main:app --reload
```

Open the following URL:

```text
http://127.0.0.1:8000/docs
```

### 8.2 Test the Upload API

Endpoint:

```text
POST /upload
```

Steps:

1. Expand POST `/upload`.
2. Click **Try it out**.
3. Click **Choose File**.
4. Select an image such as `demo.png`.
5. Click **Execute**.

FastAPI sends the file using multipart form data.

Expected response:

```json
{
    "message": "file uploaded successfully",
    "filename": "demo.png",
    "file_url": "http://127.0.0.1:8000/files/demo.png"
}
```

### 8.3 Verify the Uploaded File

Open the project directory.

The folder structure should now look like:

```text
project/
│
├── main.py
│
└── uploads/
    └── demo.png
```

This confirms that the file has been saved on the server.

### 8.4 Open the Uploaded Image

Copy the `file_url` returned by the upload API.

Open it in the browser:

```text
http://127.0.0.1:8000/files/demo.png
```

The browser should display the uploaded image.

For a PDF, the browser may display the PDF directly or download it, depending on the browser and response handling.

### 8.5 Test a Nonexistent File

Try opening:

```text
http://127.0.0.1:8000/files/unknown.png
```

If that file does not exist inside `uploads`, the static file application returns:

```text
404 Not Found
```

---

# 9. Important Concepts to Remember

| Concept | Purpose |
|---|---|
| `UploadFile` | Receives uploaded file data |
| `File(...)` | Declares a required file parameter |
| `StaticFiles` | Serves files from a directory |
| `app.mount()` | Mounts an application under a URL prefix |
| `os.path.exists()` | Checks whether a path exists |
| `os.makedirs()` | Creates a directory |
| `os.path.join()` | Combines directory and filename |
| `shutil.copyfileobj()` | Copies file contents |
| `open()` | Opens a file |
| `"wb"` | Opens a file for writing binary data |
| `HTTPException` | Returns an HTTP error response |
| `file.filename` | Retrieves the uploaded filename |
| `file.file` | Accesses the underlying uploaded file object |

---

# 10. Important Interview Questions

### 1. How does file uploading work in FastAPI?

FastAPI provides `UploadFile` and `File` to receive files from clients. The uploaded file can then be saved on the server using Python file operations.

### 2. What is UploadFile?

`UploadFile` is a FastAPI class used to represent an uploaded file. It provides attributes such as filename, content type, and the underlying file object.

### 3. What is the difference between UploadFile and bytes?

`UploadFile` provides a file-like interface and uses a spooled temporary file, which is useful for larger uploads. `bytes` reads the entire uploaded content into memory.

### 4. What is File(...)?

`File(...)` declares a request parameter as file data. The ellipsis indicates that the parameter is required.

### 5. What is multipart/form-data?

It is an HTTP request content type used to send form fields and file data together in one request.

File uploads in FastAPI commonly use multipart form data.

### 6. What is StaticFiles?

`StaticFiles` is a utility used to serve files directly from a directory through a URL path.

### 7. What is app.mount()?

`app.mount()` attaches another ASGI application to the FastAPI application under a specified URL prefix. It is commonly used for static file serving.

### 8. What is the difference between an API endpoint and static file serving?

An API endpoint executes application logic and generally returns data such as JSON.

Static file serving returns files directly from a configured directory without requiring a separate endpoint for every file.

### 9. Why do we use os.makedirs()?

It creates the upload directory if it does not already exist, ensuring that the application has a location in which to save uploaded files.

### 10. Why do we use os.path.join()?

It combines directory names and filenames into a valid filesystem path using the operating system's path separator.

### 11. Why is shutil.copyfileobj() used?

It copies data from the uploaded file object into the destination file.

### 12. Why do we use binary write mode (`wb`)?

Images, PDFs, and other non-text files contain binary data. Binary write mode saves these contents without treating them as text.

### 13. What happens if an uploaded file is not found?

The application can return a 404 Not Found response when the requested file does not exist.

### 14. Can FastAPI upload multiple files?

Yes. FastAPI supports multiple file uploads using `list[UploadFile]` with `File(...)`.

### 15. What is the purpose of file.filename?

It provides the original filename supplied with the uploaded file.

### 16. Does StaticFiles automatically save uploaded files?

No. `StaticFiles` only serves files from a directory. The application must first receive and save uploaded files.

### 17. What is the difference between UploadFile and StaticFiles?

`UploadFile` is used to receive files from clients, whereas `StaticFiles` is used to serve files from the server to clients.

### 18. What is the purpose of HTTPException?

It allows the application to return HTTP error responses with appropriate status codes and details.

---

# 11. Important Practical Considerations

The current implementation is suitable for learning the basic file upload and static file concepts. Real applications should also consider the following points.

### 11.1 Validate the Filename Before Creating the Path

In the current code, the destination path is created before checking whether a filename exists.

The validation should happen first to avoid errors when the filename is missing.

### 11.2 Prevent Unsafe Filenames

Do not blindly trust filenames supplied by clients.

A malicious filename may contain path traversal components or unexpected paths.

Production applications should validate filenames and use safe server-generated filenames where appropriate.

### 11.3 Validate File Types

The application currently accepts uploaded files without restricting their types.

A real application should validate allowed file extensions and content types. For security-sensitive uploads, it should also inspect the actual file content rather than relying only on the filename or declared MIME type.

### 11.4 Set File Size Limits

Large files can consume significant storage and memory resources.

Production applications should enforce upload size limits.

### 11.5 Avoid Overwriting Existing Files Accidentally

If two users upload files with the same filename, the current implementation opens the destination in `"wb"` mode, which overwrites the existing file.

A real application should generate unique filenames or otherwise handle duplicate names.

### 11.6 Protect Sensitive Files

Not every uploaded file should be publicly accessible.

Files containing private information should be stored outside publicly served directories and delivered only after authorization checks.

### 11.7 Install the Required Dependency

FastAPI file uploads require `python-multipart`.

Install it using:

```bash
pip install python-multipart
```

---

# 12. Key Takeaways

- File upload allows clients to transfer files to the server.
- `UploadFile` receives the uploaded file.
- `File(...)` declares a required file parameter.
- `os.path.exists()` checks whether the upload directory exists.
- `os.makedirs()` creates the directory when needed.
- `os.path.join()` constructs the destination file path.
- `open(..., "wb")` opens the destination in binary write mode.
- `shutil.copyfileobj()` copies the uploaded file contents.
- `StaticFiles` serves files from a configured directory.
- `app.mount("/files", ...)` makes the directory accessible through the `/files` URL prefix.
- The uploaded file can be accessed directly through its URL.
- File validation, size limits, safe filenames, and access control are important for production applications.

**Final Understanding:** File upload and static file serving are two separate operations. `UploadFile` receives the file from the client, Python file operations save it inside the `uploads` directory, and `StaticFiles` makes the saved file accessible through a URL.