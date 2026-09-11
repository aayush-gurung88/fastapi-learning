# Task 2 — Pydantic Model + POST

# Create a Product model with:

# name → str, min 3 chars
# price → float, must be > 0
# category → str
# in_stock → bool, default True

# Make POST /products/ that accepts the model and returns it with a 201 status code.



from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from typing import Annotated


app = FastAPI()


class Product(BaseModel):
    name : str = Field(min_length=3)
    price : float = Field(gt=0)
    category : str
    in_stock : bool = True  #vaneko default true 


app.post("/products/", status_code=201)
def create_product(product:Product):
    return {
        "product": product
    }

#  yo endpoint chai yesari kaam garxa !!

# POST /products/
#        ↓
# receives Product model
#        ↓
# Pydantic validates it
#        ↓
# successful → HTTP 201
#        ↓
# returns product