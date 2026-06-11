# Handling Errors=========

#  Practice Task

# Make GET /users/{user_id} — raise 404 if user_id not in a fake dict
# Create a custom exception InvalidAgeException — raise it if age < 0 in POST /users/
# Register a global handler for InvalidAgeException that returns status 400 with a clear message

# Test all error cases in /docs

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

fake_db = {
    "1": {"name": "Alice"},
    "2": {"name": "Bob"}
}

class InvalidAgeException(Exception):
     pass


class UsernameTooShort(Exception):
    pass

@app.exception_handler(InvalidAgeException)
def invalidAge_exception_handler(
    request: Request, exc: InvalidAgeException):
    return JSONResponse (
        status_code= 400,
        content= {"message":str(exc)})


@app.exception_handler(UsernameTooShort)
def username_exception_handler(
    request:Request,
    exc: UsernameTooShort
):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )

@app.get("/users/{user_id}")
def get_user(user_id: str):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    return fake_db[user_id]


@app.post("/users/")
def create_user(username:str, age: int):
    if age < 0: 
        raise InvalidAgeException("Age cannot be less than 0")
    if len(username) < 3:
        raise UsernameTooShort("Username must be at least 3 characters long")

    return {
    "username": username,
    "age": age
}