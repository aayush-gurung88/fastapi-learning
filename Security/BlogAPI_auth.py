# Fresh Task — Blog API Auth
# Build a simple auth system for a blog:
# Fake DB — 2 users:

# john → password john123, active
# banned → password ban123, disabled

# Models:

# Author → username, email, disabled
# AuthorInDB → adds hashed_password

# Functions:

# fake_hash_password → "hashed_" + password
# get_author → finds user in DB by username
# get_current_author → extracts token, finds user, 401 if not found
# get_current_active_author → checks disabled, 400 if disabled

# Routes:

# POST /token → login
# GET /profile/ → returns current active author
# GET /posts/ → returns {"posts": ["post1", "post2"], "author": username}

from typing import Annotated
from fastapi import FastAPI,Depends, HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

app = FastAPI()

fake_authors_db = {
    "john": {
        "username": "john",
        "email": "john@gmail.com",
        "hashed_password": "hashed_john123",
        "disabled": False
    },
    "banned": {
        "username": "banned",
        "email": "ban@gmail.com",
        "hashed_password": "hashed_ban123",
        "disabled": True
    }
}

class Author(BaseModel):
    username: str
    email: str
    disabled: bool

class AuthorInDB(Author):
    hashed_password: str

def fake_hash_password(password:str):
    return "hashed_" + password
# this fucntion takes normal password and converts into a fake "secured" version

# like 
# input: john123
# output: hashed_john123
# and why we need this thing is real apps don't store password directly , it is stored as hashed version



# yah chai database bata username find gareko 
def get_author(username: str):
    user = fake_authors_db.get(username)

    if not user:
        return None
    
    return AuthorInDB(**user)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# now these are dependencies hai (vaneko reusable logic hai )

# yesko parameter vitra - what we do is (Get token from request)
def get_current_author(token: Annotated[str, Depends(oauth2_scheme) ]):
    # then find user in fake DB
    author = get_author(token)
    # handling missing user
    if not author:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")
    
    # # convert dict --> model 
    # author = AuthorInDB(**author) #sayad mathi gari sakyo convert tae vayera chaidaina yah 

    return author

def get_current_active_author(current_user :Annotated[AuthorInDB,Depends(get_current_author)]):
    if current_user.disabled:
        raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    
    return current_user


# --- ROUTES ---

@app.post("/token")
def login(user_data:Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = user_data.username
    password = user_data.password

    user = get_author(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="user not found")
    
    if fake_hash_password(password) != user.hashed_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")
    
    return {
        "access_token": user.username,
        "token_type": "bearer"
  
    }



@app.get("/profile/",response_model=Author)
def get_profile(current_user: Annotated[AuthorInDB, Depends(get_current_active_author)]):
    return current_user

@app.get("/posts/")
def get_posts(current_user: Annotated[AuthorInDB, Depends(get_current_active_author)]):
    return {
        "posts": ["post1","post2"],
        "author": current_user.username
        }