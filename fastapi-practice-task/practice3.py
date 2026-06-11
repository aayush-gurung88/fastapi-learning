# Request Body - vaneko client sending data to API 
# Response body - API sends data back to client 

#  Practice Task
# Create a POST /products/{store_id} route with:

# store_id → path param (int)
# in_stock → query param, bool, default True
# A Product Pydantic model with: name (str), price (float), discount (float | None)

# Return the product dict + store_id + a calculated final_price if discount exists. 

from fastapi import FastAPI
from pydantic import BaseModel, validator
 

app = FastAPI()

class Product(BaseModel):
    name: str
    price: float
    discount: float|None = None

    @validator("price")
    def check_price(cls,value):
        if value <= 0:
            raise ValueError("Price must be > 0")
        return value
    
    @validator("discount")
    def check_discount(cls, value , values):
        if value is not None and value < 0: 
            raise ValueError("Discount must be >=0")

@app.post("/products/{store_id}")
def create_product(store_id: int, product: Product,  in_stock: bool = True, ):
    final_price = product.price
    if product.discount is not None:
        final_price -= product.discount
    return {
        "store_id":store_id,
        "in_stock":in_stock,
        **product.dict(),
        "final_price":final_price
    }
    


 