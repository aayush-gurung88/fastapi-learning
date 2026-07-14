#  == CreateModels === 

# Create a Student SQLModel table with:

# id → primary key, auto-generated
# name → str, indexed
# grade → int, indexed
# email → str, required, no index

# Just define the class — no routes yet.

from sqlmodel import SQLModel , Field

class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    grade: int = Field(index=True)
    email: str = Field(...)

