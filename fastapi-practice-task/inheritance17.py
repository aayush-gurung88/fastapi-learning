#  This is the redone of Practice17.py but using the concept of INHERITANCE


from pydantic import BaseModel,EmailStr
from fastapi import FastAPI

app = FastAPI()

class BaseUser(BaseModel):
    username: str
    email: EmailStr
    age: int

class UserIn(BaseUser):
    password: str
    
class UserOut(BaseUser):
    pass 


@app.post("/register/", response_model=UserOut)
def register(user:UserIn):
    return user