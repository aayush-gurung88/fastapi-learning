# Practice Task

# Make PUT /orders/{order_id} with:

# order_id → path param, int, ge=1
# Item model → name (str), quantity (int), price (float)
# User model → username (str), address (str | None)
# priority → singular int in the body, must be ge=1, le=5
# q → optional query string

# Send the full JSON body in /docs and test it.

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

class Item(BaseModel):
    name: str 
    quantity: int
    price: float


class User(BaseModel):
    username: str
    address: str | None = None # Yo chai optional banako hai (address lai optional banako)

class Order(BaseModel):
    item: Item
    user: User
    priority: int = Field(ge=1, le=5)


@app.put("/orders/{order_id}")
def update_order(
    order_id: Annotated[int , Path(ge=1)],
    # Using a Pydantic model parameter automatically makes FastAPI read it from the request body, so explicit Body() is often unnecessary.
    order: Order, 
    q: Annotated[str | None, Query()] = None
):
    return{
        "order": order,
        "q":q
    }


# =========== Request handling + validation in FastAPI ======

# Path + Query + Nested Body Validation using Pydantic models

