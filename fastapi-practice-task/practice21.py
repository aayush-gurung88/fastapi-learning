# Practice Task
# Make two endpoints:

# POST /upload/ → accepts single UploadFile, returns filename and content_type
# POST /upload/multiple/ → accepts list[UploadFile], returns list of filenames

from fastapi import FastAPI, File , UploadFile
from typing import Annotated


app = FastAPI()

@app.post("/upload/")
def upload_file(file: UploadFile = File(...) ):
    return  { 
        "file name": file.filename,
        "file content_type": file.content_type }

@app.post("/upload/multiple/")
def upload_multiple(files: list[UploadFile] = File(...)):
    return {
        "files":
        [
            {
                "filename": file.filename,
                "content_type": file.content_type
            }
            for file in files
        ]
    }
