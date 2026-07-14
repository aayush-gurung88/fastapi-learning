# ======== Dependencies in Path Operation Decorators

# Practice Task
# Create two dependencies:

# verify_token → checks header x_token == "mytoken123" → raises 401 if wrong
# verify_admin → checks header x_role == "admin" → raises 403 if wrong

# Apply both to GET /admin/dashboard/ using dependencies=[].
# Route just returns {"message": "Welcome Admin"} — no params needed. 
from fastapi import FastAPI, Depends, Header, HTTPException, status
from typing import Annotated

app = FastAPI()

def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "mytoken123":
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                    )

def verify_admin(x_role: Annotated[str, Header()]):
    if x_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You donot have access to this resource")
    


@app.get("/admin/dashboard/", dependencies=[Depends(verify_token), Depends(verify_admin)])
def get_admin():
    return {"message": "Welcome Admin"}