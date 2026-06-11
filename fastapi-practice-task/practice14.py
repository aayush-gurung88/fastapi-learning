#  ====== HEADER PARAMETERS ---- 

# Practice Task
# Make GET /dashboard/ that reads:

# user_agent → optional str header
# x_api_key → required str header
# x_roles → list[str] | None for duplicate headers, optional


from fastapi import FastAPI , Header
from typing import Annotated

app = FastAPI()

@app.get("/dashboard/")
def get_dashboard(
    x_api_key: Annotated[str, Header()],
    user_agent: Annotated[str , None, Header()] = None,
    x_roles: Annotated[list[str] | None, Header()] = None
):
    return{
        "user_agent": user_agent,
        "x_api_key": x_api_key,
        "x_roles": x_roles
    }