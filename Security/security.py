# Create a new file security.py:

# Set up OAuth2PasswordBearer
# Make two protected routes GET /items/ and GET /users/me
# Both just return the token for now

# Run it → open /docs → click the lock icon → see the Authorize button.


from fastapi import FastAPI,Depends
from fastapi.security import OAuth2PasswordBearer

from typing import Annotated

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def get_items(token:str = Depends(oauth2_scheme)):
    return {
        "token":token
    }


@app.get("/users/me/")
async def get_user_me(token:Annotated[str, Depends(oauth2_scheme)]):
    return{
        "token":token
    }