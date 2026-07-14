# Practice Task
# Build this complete simple auth system in a new file simple_auth.py:

# fake_users_db with 2 users — one active, one disabled
# User and UserInDB models
# fake_hash_password function
# get_current_user dependency with 401 if not found
# get_current_active_user dependency with 400 if disabled
# POST /token → login endpoint
# GET /users/me → returns current active user
# GET /items/ → returns items + owner: current_user.username

# Test all 3 cases in /docs:

# Active user login 
# Inactive user → error 
# Wrong password → error 

from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()

# created a fake user db with 2 user information
fake_users_db = {
    "active_user": {
        "id": 1,
        "username": "active_user",
        "email": "user1@example.com",
        "hashed_password": "fakehashed_secret1",
        "disabled": False
    },
    "disabled_user": {
        "id": 2,
        "username": "disabled_user",
        "email": "user2@example.com",
        "hashed_password": "fakehashed_secret2",
        "disabled": True
    }
}


class User(BaseModel):
    id: int
    username: str
    email: str
    disabled: bool

class UserInDB(User):
    hashed_password: str

def fake_hash_password(password):
    return "fakehashed_" + password



@app.post("/token")
def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = form_data.username
    password = form_data.password 


# find user in DB
    user = fake_users_db.get(username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect Username or password!")

# yah chai we check password !

    # user = UserInDB(**user)

    if fake_hash_password(password) != user["hashed_password"]:
        raise HTTPException(status_code=400, detail="Incorrect Username or password!")

    return {
        "access_token": user["username"],
        "token_type": "bearer"
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token:Annotated[str, Depends(oauth2_scheme)]):
    user = fake_users_db.get(token)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials", headers= {"WWW-Authenticate":"Bearer"})

    return user 

def get_current_active_user(current_user = Depends(get_current_user)):
    if current_user["disabled"] == True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is inactive")
    
    return current_user

@app.get("/users/me")
def read_user_me(current_user = Depends(get_current_active_user)):
    return User(**current_user)



@app.get("/items/")
def read_items(current_user = Depends(get_current_active_user)):
    return {
        "items": ["item1","item2"],
        "owner": current_user["username"]
    }


# Final check (what you built)

# You now have:

# login (/token) 
# OAuth2 bearer auth 
# dependency chain 
# get_current_user
# get_current_active_user
# protected routes 
# /users/me
# /items/
# active vs disabled user logic 
# error handling 