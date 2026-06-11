# Practicing

# Testing:

# Integer path parameters
# Route ordering
# Validation errors
# Enum validation
# Swagger docs testing

# That’s core FastAPI routing knowledge.


from fastapi import FastAPI
from enum import Enum

app = FastAPI()

@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {"product_id": product_id}

@app.get("/users/admin")
def get_admin():
    return {"message": "Admin page"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}


# Enum is like fixed allowed choices
# Enum vaneko chai Html ma <select> dropdown with fixed allowed options
class Color(str, Enum):
    red = "red"
    green = "green"
    blue = "blue"

# Enum ko route ko example
# jsatai /clolors/red is valid
# colors/yellow is not valid is doesnot shows anything
@app.get("/colors/{color}")
def get_color(color: Color):
    return {"color": color}