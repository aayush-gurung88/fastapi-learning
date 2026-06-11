# ===== Query params with validation using Pydantic Annotated + FastAPI Query=======

# Make a GET /search/ route with:

# q → optional str, min 2 chars, max 30 chars
# tags → list of strings, optional, default []
# sort_by → required str, alias "sort-by"
# A custom validator that ensures sort_by is either "price" or "date" (use AfterValidator)



from fastapi import FastAPI, Query
from typing import Annotated    
from pydantic import AfterValidator

app = FastAPI()


def validate_sort(value):
    # if value is None:
    #     raise ValueError("NO value")
    # elif value == "price":
    #     return value
    # elif value == "date":
    #     return value
    # else:
        
    if value in ["price","date"]:
        return value
    else:
        raise ValueError("Invalid Value")
   

@app.get("/search")
def search(
    q: Annotated[str | None, Query(min_length=2 , max_length=30)] = None ,
    tags: list[str] = [],
    sort_by:Annotated[str , AfterValidator(validate_sort), Query(alias="sort-by")] = ...
):
    return{
        "q": q,
        "tags": tags,
        "sort_by": sort_by
        }



# # FastAPI /search Route Practice

# ## Overview
# This project demonstrates a FastAPI GET endpoint with query parameter validation using `Annotated`, `Query`, and `AfterValidator`.

# ---

# ## Endpoint
# GET /search

# ---

# ## Query Parameters

# ### q (optional)
# - Type: `str | None`
# - Constraints:
#   - min length: 2
#   - max length: 30
# - Default: `None`

# Example:
# /search?q=phone

# ---

# ### tags (optional)
# - Type: `list[str]`
# - Default: `[]`

# Example:
# /search?tags=tech&tags=mobile

# ---

# ### sort-by (required)
# - Type: `str`
# - Alias: `sort-by`
# - Allowed values:
#   - `price`
#   - `date`
# - Validation: custom validator using `AfterValidator`

# Example:
# /search?sort-by=price

# ---

# ## Validation Function

# ```python
# def validate_sort(value):
#     if value in ["price", "date"]:
#         return value
#     raise ValueError("Invalid Value")