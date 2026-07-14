# Practice Task
# Build a complete Student API with SQLModel:
# Models:

# StudentBase → name (str, indexed), grade (int, indexed)
# Student(table=True) → adds id, email
# StudentPublic → id (int), name, grade (no email)
# StudentCreate → name, grade, email
# StudentUpdate → all optional

# Routes:

# POST /students/ → create, return StudentPublic
# GET /students/ → list with offset + limit
# GET /students/{id} → get one, return StudentPublic
# PATCH /students/{id} → partial update
# DELETE /students/{id} → delete

# Run it, test in /docs, confirm email never appears in responses! 

from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import SQLModel , Field, create_engine, Session, select
from typing import Annotated

app = FastAPI()

# you chai engine create gareko
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)
    

# Table create gareko 

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Database session dependency banako 

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

class StudentBase(SQLModel):
    name: str = Field(index=True)
    grade: int = Field(index=True)


class Student(StudentBase, table=True):
    id: int |None = Field(default=None, primary_key=True)
    email: str = Field(...)


class StudentPublic(StudentBase):
    id: int 


class StudentCreate(StudentBase):
    email: str


class StudentUpdate(SQLModel): 
    name: str | None = None
    email: str | None = None
    grade: int | None = None



# Routes haru 

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/students/", response_model=StudentPublic)
def create_student(student:StudentCreate,
                   session: SessionDep):

    db_student = Student.model_validate(student)
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student   

@app.get("/students/", response_model=list[StudentPublic])
def get_students(
    session: SessionDep,
    offset: int = 0,
    limit: int = 10
):
    #  query banako student table bata 
    query = select(Student).offset(offset).limit(limit)

    # Session bata query execute gareko ani list ma convert gareko 
    students = session.exec(query).all()
    
    return students


@app.get("/students/{id}")
def get_student(id: int , session: Session = SessionDep):
    query = select(Student).where((Student.id == id))

    student = session.exec(query).first()
    if(student is None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    return student


@app.patch("/students/{id}")
def update_students(id: int , studentupdate:StudentUpdate, session: SessionDep):

    db_student = session.exec(select(Student).where(Student.id == id)).first()

    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    update_data = studentupdate.model_dump(exclude_unset=True)

    for key , value in update_data.items():
        setattr(db_student, key, value)

    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    
    return db_student


@app.delete("/students/{id}")
def delete_students(id: int , session : Session = SessionDep):
    db_student = session.exec(select(Student).where(Student.id == id)).first()

    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    session.delete(db_student)
    session.commit()

    return db_student 


# A perfect mini project for several reasons:

# Full CRUD (POST, GET, PATCH, DELETE)
# Uses SQLModel / SQLAlchemy for DB
# FastAPI routes with proper response models
# Error handling (404 for missing students)
# Data hiding (email not in public responses)
# Includes pagination (offset + limit)


# Schema separation (important concept)

# तिमीले 3 type बनायौ:

# StudentBase → shared fields
# StudentCreate → input validation
# StudentPublic → output filtering (email hide)
# StudentUpdate → partial update


# Session system (DB connection handling)
# Session(engine) use भयो
# Depends(get_session) → automatic DB connection injection

# Normal CRUD:

# no connection management

# यहाँ:

# proper request-wise DB session


# Python CRUD होइन, real backend system with database + API design

