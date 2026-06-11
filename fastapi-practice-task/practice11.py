# Practice Task
# Take your Product model from the Body Fields task and add:

# model_config with one full example
# Then try openapi_examples in Body() with 2 named examples — one valid, one invalid

# TASK 9 - CONTINUE . . . . . 

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

class Product(BaseModel):
    name: str = Field(..., min_length=2 , max_length=50 )
    price: float = Field(... , gt=0)
    stock: int = Field(0, ge=0 )
    description: str = Field(None, max_length=200)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Iphone16",
                "price": 999.99,
                "stock": 10,
                "description": "Best in the market"
            }
        }
    }   

@app.post("/products/")
def create_product(product: Annotated[Product, Body(
    openapi_examples={
        "valid_example": {
            "summary": "A correct product",
            "value":{
                "name": "TUFF",
                "price": 5555,
                "stock": 4545,
                "description": "Best for gaming"
            }
        },
        "invalid_example": {
            "summary": "An Invalid product",
            "value":{
                "name": "N",
                "price": -10,
                "stock": -5,
                "description": "Invalid product"
            }
            
        }
    }
)]):
    return {"product": product} 