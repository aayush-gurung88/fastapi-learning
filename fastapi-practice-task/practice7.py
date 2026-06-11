#  Practice Task
# Create a FilterParams model with:

# page → int, default 1, must be >= 1
# size → int, default 10, must be between 1 and 50
# sort_by → Literal["name", "price", "date"], default "name"
# in_stock → bool, default True

# Use it in GET /products/ and add extra = "forbid"



from typing import Annotated, Literal # typing tools (for rules + fixed choices)

from fastapi import FastAPI, Query 
from pydantic import BaseModel, Field # Pydantic = data validation engine


app = FastAPI()

# DATA MODEL (input structure)
class FilterParams(BaseModel):
     # page number in API (?page=1)
    page: int = Field(1, ge=1)
    size: int = Field(10, gt=1, le=50)

        # sorting option (?sort_by=name) 
    sort_by: Literal["name","price","date"] = "name"
    in_stock: bool = True    # default True (no validation needed)

#  ==== API Endpoint ====
@app.get("/products")
def products(
    filters: Annotated[
        FilterParams, 
        Query(extra="forbid")
        ],
    ):

    # response (what API returns)
    return{
        "filters": filters
    }


# What I just learned (big concept)

# I combined:

# Pydantic model validation
# Query parameter binding
# Literal constraints
# Field constraints
# API input structuring

# This is real backend API design level