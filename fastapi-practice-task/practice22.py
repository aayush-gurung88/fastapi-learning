# Request Forms and Files ============

# Practice Task
# Make POST /profile/ that accepts:

# username → Form() str
# age → Form() int
# avatar → UploadFile

# Return all three fields + content_type of the avatar.

from fastapi import FastAPI, File, Form, UploadFile
from typing import Annotated


app = FastAPI()

@app.post("/profile/")
def create_profile(
    username: Annotated[str, Form()],
    age: Annotated[int, Form()],
    avatar: Annotated[UploadFile , File(...)]
):
    return {
        "username": username,
        "age": age,
        "avatar_filename": avatar.filename,
        "avatar_content_type": avatar.content_type
    }