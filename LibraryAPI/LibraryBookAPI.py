# Task 1 — Library Book API 📚
# Build a complete Book Management API with SQLModel:
# Models:

# BookBase → title (str, indexed), author (str, indexed), year (int)
# Book(table=True) → adds id, isbn (str)
# BookPublic → id, title, author, year (no isbn)
# BookCreate → all base fields + isbn
# BookUpdate → all optional

# Routes:

# POST /books/ → create, return BookPublic
# GET /books/ → list with offset + limit + filter by author (optional query param)
# GET /books/{id} → get one
# PATCH /books/{id} → partial update
# DELETE /books/{id} → delete

# Extra:

# Proper status codes
# Tags ["books"] on all routes
# 404 with clear messages


from sqlmodel import SQLModel, Field , create_engine, Session, select
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated

app = FastAPI()

# Database setup 

# 1. Database banako 
sqlite_file_name = "Librarydatabase.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# 2. Engine Create gareko 
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# 3. Table create garne 

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 4. Session dependency banako
def get_session():
    with Session(engine) as session:
        yield session

# 5. Session lai globally user gareko or k lekhum
SessionDep = Annotated[Session, Depends(get_session)]

#6. table banako function lai startup mai call garna parxa  
# else table create hudaina

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


class BookBase(SQLModel):
    title: str = Field(index=True)
    author: str = Field(index=True)
    year: int   

class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    isbn: str

class BookPublic(SQLModel):
    id: int
    title: str
    author: str
    year: int

class BookCreate(BookBase):
    isbn: str

class BookUpdate(SQLModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None
    isbn: str | None = None


@app.post("/books/",tags=["books"], summary="Post a Book", status_code=status.HTTP_201_CREATED, response_model=BookPublic)
def create_book(book: BookCreate, session: SessionDep):  
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@app.get("/books/", tags=["books"], summary="Get all book", status_code=status.HTTP_200_OK, response_model=list[BookPublic] )
def get_books(session: SessionDep, offset: int = 0 , limit: int = 100, author: str | None = None):
    
    query = select(Book)
    if author:
        query = query.where(Book.author == author)
    query = query.offset(offset).limit(limit)
    books = session.exec(query).all()
    return books

        #  SELECT * FROM book
        # WHERE author = 'Ram';

        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Books Payena Babu")

@app.get("/books/{id}", tags=["books"], summary="Get Book By ID",response_model=BookPublic)
def get_book(id: int , session: SessionDep):
    query = select(Book).where(Book.id == id)
    book = session.exec(query).first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book Payena babu"
        )
    return book


@app.patch("/books/{id}",tags=["books"], summary="Update specific Book", response_model=BookPublic)
def update_book(id:int ,book_update:BookUpdate, session: SessionDep):
    
    book = session.exec(select(Book).where(Book.id == id)).first()

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Yah pani book payena"
        )
    
    update_data = book_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(book, key, value)
    
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@app.delete("/books/{id}", tags=["books"], summary="Delete Book")
def delete_book(id:int , session:SessionDep):
    db_book = session.exec(select(Book).where(Book.id == id)).first()

    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Delete Garna Book Payena"
        )
    
    session.delete(db_book)
    session.commit()

    return db_book