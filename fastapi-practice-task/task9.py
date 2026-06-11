from fastapi import Body, FastAPI, Path
from pydantic import BaseModel, Field
from typing import Annotated

app  = FastAPI()

class Product(BaseModel):
    name: str = Field(..., min_length=3 , max_length=40)
    price: float = Field(..., gt= 0)
    quantity: int = Field(1, ge=0)
    description: str | None = Field(None, max_length=150)


@app.put("/products/{product_id}")
def create_product(
    product_id: int,
    product: Annotated[Product, Body(embed=True)]
):
    return{
        "product_id": product_id,
        "product": product
    }