#  ======= FastAPI Data Modeling with Pydantic (Request/Response Schemas) ======
# Object transformation (UserIn → UserInDB → UserOut)


# Practice Task
# Create:

# UserBase → username, email (EmailStr)
# UserIn(UserBase) → adds password
# UserOut(UserBase) → just pass
# UserInDB(UserBase) → adds hashed_password

# Make POST /register/:

# Takes UserIn
# Hashes password → "hashed_" + password
# Creates UserInDB using **user.model_dump()
# Returns UserOut (no password, no hash)

# Check in /docs — only username and email in response.

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserBase(BaseModel):
    username: str
    email: EmailStr
    
class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str


@app.post("/register/", response_model=UserOut)
def register(user: UserIn):
    hashed_password = "hashed_" + user.password
    db_user = UserInDB(
        **user.model_dump(exclude={"password"}),
        hashed_password=hashed_password
    )
    
    return db_user
