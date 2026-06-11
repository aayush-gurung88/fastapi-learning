#  ======== COOKIE PARAMETER MODELS(CLASS) -----

# Practice Task
# Create a Cookies model with:

# auth_token → required str
# language → optional str, default "en"

# Add extra: forbid and use it in GET /settings/


from fastapi import FastAPI, Cookie
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

class Cookies(BaseModel):
    model_config = {"extra": "forbid"}
    auth_token: str
    language: str = "en"

@app.get("/settings/")
def get_settings(cookies: Annotated[Cookies, Cookie()]):  
    return cookies