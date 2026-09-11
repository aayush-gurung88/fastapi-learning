# Task 1 — Basic Routes + Validation

# Build GET /products/{product_id} with:

# product_id → path param, int, must be >= 1
# category → optional query param, str
# in_stock → optional query param, bool, default True



from fastapi import FastAPI, Query, Path
from typing import Annotated

app = FastAPI()

@app.get("/products/{product_id}")
def get_product(
    product_id: Annotated[int, Path(ge=1)],
    category: Annotated[str | None, Query],
    in_stock: bool = True
):
    return {
       "product_id" : product_id,
       "category": category,
       "in_stock": in_stock
    }