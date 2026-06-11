
#  ============ Body Fields ======

#  First what Filed is --> Query , Path , Body ley chai function parameters ma validation add garxa and 
# Fields ley chai Pydantic model ma validation add garxa ....

# Practice Task
# Create a Product Pydantic model with Field validations:

# name → str, min length 2, max length 50
# price → float, must be > 0
# stock → int, ge=0, default 0
# description → optional str, max 200 chars, default None

# Use it in POST /products/ and test in /docs

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Product(BaseModel):
    name: str = Field(..., min_length=2 , max_length=50 )
    price: float = Field(... , gt=0)
    stock: int = Field(0, ge=0 )
    description: str = Field(None, max_length=200)


@app.post("/products/")
def create_product(product:Product):
    return{     
        "product": product
    }