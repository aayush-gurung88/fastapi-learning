
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

class User(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    email: EmailStr
    is_active: bool = True

class Item(BaseModel):
    product_name: str
    price: float = Field(gt= 0)
    quantity: int = Field(ge=1)

class Order(BaseModel):
    user: User
    items: list[Item]
    total_price: float = Field( gt=0)
    notes: str | None = Field(None,max_length=200) 


@app.post("/orders/")
def create_order(order:Order):
    return{
        "order": order
    }