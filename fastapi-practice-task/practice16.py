# ==== Header Parameter Models =======

# Practice Task
# Create a CommonHeaders model with:

# x_api_key → required str
# accept_language → optional str, default "en"
# x_roles → list[str], default []

# Add extra: forbid and use it in GET /data/.

from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

class CommonHeaders(BaseModel):
    model_config = {"extra": "ignore"}

    x_api_key: str
    accept_language: str = "en"
    x_roles: list[str] = []

@app.get("/data/")
def get_headers(headers: Annotated[CommonHeaders, Header()]):
    return {
        "headers": headers
    }