from fastapi import Header, HTTPException,status
from typing import Annotated

def verify_api_key(x_api_key: Annotated[str, Header()]):
    if x_api_key != "secret123":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid API Key")
