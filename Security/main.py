from fastapi import FastAPI, Depends
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token:Annotated[str, Depends(oauth2_scheme)]):
    return {
        "token":token
    }


# so this is the basic setup when doing security 
# OAuth2PasswordBearer(tokenUrl="token") → tells FastAPI where the login endpoint will be (/token)
# Depends(oauth2_scheme) → extracts Bearer token from Authorization header automatically
# token: str → you get the raw token string in your route

# tokenUrl="token" → doesn't create the endpoint, just tells FastAPI where it will be.

