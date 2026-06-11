#  ==== FORM DATA AND FORM MODELS (EXAMPLE) ====

# Practice Task
# Make POST /login/ that accepts:

# username → required str, min 3 chars
# password → required str, min 6 chars

# Return {"message": "Login successful", "username": username}.
# Test in /docs — notice it shows a form instead of JSON input.


# Upgrade your previous /login/ to use a LoginForm Pydantic model with:

# username → str, min 3 chars
# password → str, min 6 chars
# extra: forbid

# Same result, cleaner code



from fastapi import FastAPI, Form
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI()

class LoginForm(BaseModel):
    username: str = Field(min_length=3)
    passowrd: str = Field(min_length=6)
    model_config = {"extra":"forbid"}



@app.post("/login/")
# def create_profile(
#     username: Annotated[str, Form(min_length=3)],
#     password: Annotated[str, Form(min_length=6)]
# ):
#     return {
#         "message": "Login successful",
#         "username": username
#     }


def login(data: Annotated[LoginForm, Form()]):
    return{
        "message": "Login Successful",
        "username": data.username
    }

