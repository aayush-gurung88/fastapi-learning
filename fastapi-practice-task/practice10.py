# Practice Task
# Build these models:

# Author → name (str), email (str) (use EmailStr from pydantic)
# Comment → text (str), likes (int, ge=0)
# BlogPost → title (str), tags (set[str]), author (Author), comments (list[Comment] | None)

# Make POST /posts/ that accepts a BlogPost and returns it.

from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

class Author(BaseModel):
    name: str
    email: EmailStr 

class Comment(BaseModel):
    text: str
    likes: int = Field(ge=0)

class BlogPost(BaseModel):
    title: str
    tags: set[str] = Field(default_factory=set)
    author: Author
    comments: list[Comment] | None = None
    # comments: list[Comment] | None = Field(default=None)


@app.post("/posts/")
def create_post(post:BlogPost):
    return{
        "post":post
    }

#  Just Bulid 
# A nested validated schema system
# Author is reusable object -- Comment is reusable object -- 
# BlogPost is composed object - is an obj that is built using other obj inside it