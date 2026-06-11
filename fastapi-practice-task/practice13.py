#  ======== COOKIE PARAMETER ======

# Practice Task
# Make GET /profile/ that reads two cookies:

# session_id → required str
# theme → optional str, default "light"

# Test it using curl or Postman by passing the cookies manually.



from fastapi import FastAPI , Cookie
from typing import Annotated
 
app = FastAPI()

@app.get("/profile/")
def get_profile(
    session_id: Annotated[str, Cookie],
    theme: Annotated[str, Cookie] = "light"
):
    return{
        "session_id": session_id,
        "theme": theme
    }