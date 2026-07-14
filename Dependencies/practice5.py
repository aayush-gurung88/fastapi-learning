# ====== Global Dependencies   ===========

# Practice Task
# Create verify_api_key dependency that checks header x_api_key == "supersecret" → raises 401 if wrong.
# Apply it globally to the whole app.
# Make two routes GET /products/ and GET /orders/ — both should be protected automatically.
# Test with correct and wrong API key.

from fastapi import FastAPI, Header, Depends, HTTPException, status
from typing import Annotated


def verify_api_key(x_api_key: Annotated[str, Header()]):
    if x_api_key !="supersecret":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid API key",)
    
    return None

app = FastAPI(dependencies=[Depends(verify_api_key),])


@app.get("/products/")
def get_products():
    return {}


@app.get("/orders/")
def get_orders():
    return {}