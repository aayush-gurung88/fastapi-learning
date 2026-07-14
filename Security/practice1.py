# Practice Task
# Add to your security.py:

# Create User model with username, email, disabled
# Create fake_decode_token function
# Create get_current_user dependency
# Add two routes:

# GET /users/me → returns current user
# GET /items/ → returns items + current user's username


# Test in /docs — authorize with any token and see the fake decoded user. 

from typing import Annotated
from fastapi import FastAPI,Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Step 1 - User model create gareko 

class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None


# step 2 - fake token decoder (real ones I will read later in JWT hai)
def fake_decode_token(token: str):
    return User(username=token + "_user",
                # (Yesle k garchha bhane, yedi user le token ma abc pathayo bhane user ko username automatic abc_user banchha).
                email="test@example.com",
                disabled=False )
     


# Step 3 - dependency that returns current user 
# we now create a dependency function 

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

#  Step 4 - Routes haru yo chai
@app.get("/users/me/")
async def get_user_me(current_user:Annotated[User, Depends(get_current_user)]):
    return current_user

@app.get("/items/")
async def get_items(current_user:Annotated[User,Depends(get_current_user)]):
    return{"items": ["item1","item2"], "owner": current_user.username}