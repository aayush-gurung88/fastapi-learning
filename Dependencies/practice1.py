# Practice Task
# Create a dependency pagination_params that takes:

# page: int = 1
# size: int = 10

# Use it in two routes:

# GET /products/
# GET /orders/

# Both return the pagination params.
# Then store it as a type alias PaginationDep and use that instead.



from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()

# THis is the dependency
def pagination_params(
    page: int = 1, 
    size: int = 10  
):
    return{
        "page": page,
        "size": size
    }


PaginationDep = Annotated[dict, Depends(pagination_params)]

@app.get("/products/")
def get_products(pagination: PaginationDep):
    return pagination


@app.get("/orders/")
def get_orders(pagination: PaginationDep):
    return pagination


# What we did in here 

# dependency function
# reused in two routes
# type alias with Annotated
# clean parameter naming