# Shop API Auth
# Build auth for a shop from scratch:
# Fake DB — 3 users:

# admin → password admin123, active
# customer → password customer123, active
# suspended → password suspended123, disabled

# Models:

# ShopUser → username, email, role (str), disabled
# ShopUserInDB → adds hashed_password

# Functions:

# fake_hash_password → "shop_hashed_" + password
# get_user → finds + converts to ShopUserInDB
# get_current_user dependency
# get_current_active_user dependency

# Routes:

# POST /token → login
# GET /shop/me → returns current user
# GET /shop/products/ → returns products + sold_by: username
# GET /shop/admin/ → accessible only if current_user.role == "admin", else 403

from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException,status, Depends

app = FastAPI()

fake_users_db = {
    "admin": {
        "username": "admin",
        "email":"admin@gmail.com",
        "hashed_password": "shop_hashed_admin123",
        "role": "admin",
        "disabled": False
    },

    "customer": {
        "username": "customer",
        "email":"customer@gmail.com",
        "hashed_password": "shop_hashed_customer123",
        "role": "customer",
        "disabled": False
    },
    "suspended": {
        "username": "suspended",
        "email":"suspended@gmail.com",
        "hashed_password": "shop_hashed_suspended123",
        "role": "customer",
        "disabled": True
    }
}

class ShopUser(BaseModel):
    username: str
    email: str
    role: str
    disabled: bool

class ShopUserInDB(ShopUser):
    hashed_password: str

def fake_hash_password(password: str):
    return "shop_hashed_" + password


def get_user(fake_user_db, username):
    # username: str ; type hint vanxa , telling the parameter to reveice has to be string
    user = fake_user_db.get(username)

    if not user:
        return None
    
    return ShopUserInDB(**user)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token:Annotated[str, Depends(oauth2_scheme)]):  
    user = get_user(fake_users_db, token)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication!",headers={"WWW-Authenticate": "Bearer"} )
        
    return user


def get_current_active_user(current_user: Annotated[ShopUserInDB, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive User")
    return current_user

@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = form_data.username
    password = form_data.password

    user = get_user(fake_users_db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    if fake_hash_password(password) != user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentails"
        )
    
    return {
        "access_token": user.username,
        "token_type": "bearer"
    }

# username = token 
# token is taken by oauth2_scheme
# get_current_user() uses that token to find the user 

@app.get("/shop/me")
def read_current_user(current_user: Annotated[ShopUserInDB,Depends(get_current_active_user)]):
    return current_user

# /shop/me request 
# gets token 
# get_current_user() finds current user 
# get_current_active_user() checks disabled user
# and this route returns the user


@app.get("/shop/products/")
def read_current_product(current_user: Annotated[ShopUserInDB, Depends(get_current_active_user)]):
    return [
        {
            "name": "laptop",
            "price": 1000,  
            "sold_by": current_user.username
        }
    ]


@app.get("/shop/admin/")
def get_admin(current_user: Annotated[ShopUserInDB, Depends(get_current_active_user)]):

    if current_user.role == "admin":
        
        return {
            "message": "Welcome Admin"
        }
    
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    



#  === COMPLETED A FULL AUTHENTICATION FLOW IN HERE 

# fake DB , models , password hashing , get_user , current user dependency , active user check , login route , protected routes , admin role check