# ====== Response Model - Return Type 

# Practice Task
# Create two models:

# UserIn → username, password, email, age
# UserOut → username, email, age (no password)

# Make POST /register/ that accepts UserIn but returns UserOut.
# Confirm in /docs that password is not in the response.

from fastapi import FastAPI
from pydantic import BaseModel,EmailStr


app = FastAPI()

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    age: int


class UserOut(BaseModel):
    username: str
    email: EmailStr
    age: int


@app.post("/register/", response_model=UserOut)
def register(user:UserIn):
    return user