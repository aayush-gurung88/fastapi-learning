#  Practice Task
# Build a complete JWT auth system in jwt_auth.py:

# Generate your own SECRET_KEY using openssl rand -hex 32
# Add one user to fake_users_db with a real hashed password — generate it like:

# pythonfrom pwdlib import PasswordHash
# ph = PasswordHash.recommended()
# print(ph.hash("yourpassword"))  # copy this into fake_users_db

# Implement all functions:

# verify_password
# get_password_hash
# authenticate_user
# create_access_token
# get_current_user
# get_current_active_user


# Routes:

# POST /token → returns real JWT
# GET /users/me → returns current user
# GET /users/me/items → returns items with owner



# Test in /docs:

# Login → copy the JWT token
# Go to https://jwt.io → paste token → see the payload inside

from pwdlib import PasswordHash
from typing import Annotated
from pydantic import BaseModel
import jwt 
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError


app = FastAPI()

SECRET_KEY = "594c28d8d4b521c4657f50c34dd926be6e1645aeed04432e1ddc9ab3fb9f18ef"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  #vaneko token expire hune time 

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$lAvsn34izgwI4nvLxwNdrg$d94IjCzRfZYWsRpO5Y6erGDZnEwDeFcaxNppqwe9GTw",
        "disabled": False,
    }
}

class Token(BaseModel):
    access_token : str 
    token_type : str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str



password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_user(fake_users_db ,username):
    # username: str ; type hint vanxa , telling the parameter to reveice has to be string
    user = fake_users_db.get(username)

    if not user:
        return None
    
    return UserInDB(**user)


def authenticate_user(fake_users_db , username, password):
    user = get_user(fake_users_db , username)

    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    
    return user

def create_access_token(data: dict , expires_delta: timedelta | None = None):
    # parameter: type = default_value
    # after function header , copy the data why - because we don't want to modify the original dictionary that was passed in 
    # so inside the funciton we create a new varaible 

    to_encode = data.copy()
    # after the copy of data , we will be adding the expiry time 

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        # 
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

# aaba yo line le chai stores the expiry time inside the JWT payload.
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encoded(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt


# its like telling fastapi that token comes from the /token login route
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# get_current_user function le chai k garxa vane JWT bata username nikaelra database ma khojxa ani valid user farkauxa 
def get_current_user(token: Annotated[str,Depends(oauth2_scheme)]):
    # user le pathayeko JWT token like oauth2_scheme le request header bata nikalera token variable ma rakhidinxa
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Couldnot validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    # header ma chai its like telling ki "AUTHENTICATION garna JWT Bearer Token chainxa"
    # and Bearer vaneko chai token pathaune authentication scheme ho 

    try:
        # JWT token → verify गर्छ → payload निकाल्छ
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 

        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User")
    return current_user


    
@app.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm,Depends()]):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401,detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    
    # token kati samaya samma valid hune vanera expiry time ko duration rakxa !
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # username ra expiry time use garera actual JWT token banaudai ho
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )   

    return Token(access_token=access_token, token_type="bearer")



# secret key , algorithm , access token expire minutes , passwordhash(Argon2) , 
# verify password, get password hash , fake_usersdb,authenticate user , create access token , get current user , get current active user , post / token REAL JWT return
