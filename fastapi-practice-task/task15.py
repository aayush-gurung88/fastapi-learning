
from fastapi import Cookie, FastAPI
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

class Cookies(BaseModel):
    model_config = {"extra": "forbid"}

    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None


@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
            return {
                "cookies": cookies
                }