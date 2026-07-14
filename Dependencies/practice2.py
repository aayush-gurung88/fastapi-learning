# ============== Classes as Dependencies =======

# Practice Task
# Convert your previous pagination_params function dependency into a class PaginationParams with:

# page: int = 1
# size: int = 10

# Use it in GET /products/ and GET /orders/ with the Depends() shortcut.
# Access params as pagination.page and pagination.size

from fastapi import FastAPI , Depends
from typing import Annotated

app = FastAPI()

class PaginationParams:
    def __init__(self, page: int = 1 , size: int = 10):
        self.page = page
        self.size = size

@app.get("/products/")
def get_products(pagination: Annotated[PaginationParams, Depends(PaginationParams)]):
    return pagination


@app.get("/orders/")
def get_orders(pagination: Annotated[PaginationParams, Depends(PaginationParams)]):
    return pagination   
