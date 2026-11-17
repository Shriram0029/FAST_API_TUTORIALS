from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
import os
import shutil

app = FastAPI()

# step 1 - ensure upload folder exists
UPLOAD_DIRECTORY = "uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# step 2 - static file setup
# eg url:  http://127.0.0.1:8000/FILES/<filename>
app.mount("/files",StaticFiles(directory=UPLOAD_DIRECTORY), name="files")

# step 3 - Upload file API
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

# step 4 - get fileURL API
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

@app.get("/")
def home():
    return{
        "message": "File upload api running"
    }
                             

