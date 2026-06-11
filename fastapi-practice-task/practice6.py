#  ==== Path Parameters & Numeric Validations ====

# 📝 Practice Task
# Make GET /products/{product_id} with:

# product_id → int, must be between 1 and 999 (inclusive)
# rating → float query param, must be greater than 0, less than 5
# q → optional string, max 20 chars

# Test with invalid numbers in /docs and see the errors.

from fastapi import FastAPI, Path, Query
from typing import Annotated

app = FastAPI()


@app.get("/products/{product_id}")
def get_product(
    product_id: Annotated[int, Path(ge=1, le= 999)],
    rating: Annotated[float, Query(gt=0,lt=5),],
    q: Annotated[str | None, Query(max_length=20)] = None
):
    return{
        "product_id": product_id,
        "rating": rating,
        "q": q
    }

#  Above I just used all 3 :

# Path param validation
# Query param validation
# Optional query param