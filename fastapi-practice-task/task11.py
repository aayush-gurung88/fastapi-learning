#  =========== FASTAPI REQUEST BODY DOCUMENTATION WITH PYDANTIC EXAMPLES =====



# Task
# Create a UserProfile Pydantic model with these fields:

# username (str)
# email (str)
# age (int)
# bio (str | None)

# Then:

# Add model_config with one full example
# Make a POST /users/ route using openapi_examples in Body() with 3 named examples:

# "valid" → all fields filled correctly
# "minimal" → only required fields
# "invalid" → age as a string like "twenty five"

# Open /docs and check the dropdown — you should see all 3 examples.

from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserProfile(BaseModel):
    username: str
    email: str
    age: int
    bio: str | None = None  

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "Sugam",
                "email": "Sugam@example.com",
                "age": 22,
                "bio": "Gamer vaisab"
            }
        }
    }


@app.post("/users/")
def create_user(userprofile: Annotated[UserProfile, Body(
    openapi_examples= {
        "valid": {
            "summary": "Valid Examples",
            "value":{
                "username": "Sugam",
                "email": "sugam@example.com",
                "age": 25,
                "bio": "Loves coding"
            }
        },
        "minimal": {
            "summary": "Minimal Example",
            "value":{
                "username": "Druv",
                "email": "druv@example.com",
                "age": 35,
            }
        },
        "invalid": {
            "summary": "Invalid Example",
            "value":{
                "username": "Lucifer",
                "email": "lucifer@example.com",
                "age": "twenty five",
                "bio": "Loves gaming"
            }
        }
    }
)]):
    return {"UserProfile": userprofile}


# what are the concepts that I used here 
# Pydantic model - optional fields - model_config - openapi_examples 

# dropdown example in Swagger docs
# Swagger is an API documentation and testing UI

