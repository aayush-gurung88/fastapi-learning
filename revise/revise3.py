# Task 3 — Database CRUD

# Build a complete Category API with SQLModel:

# CategoryBase → name (str, indexed), description (str | None)
# Category(table=True) → adds id
# CategoryPublic → id + all base fields
# CategoryCreate → same as base
# CategoryUpdate → all optional

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name : str | None
    description : str | None

