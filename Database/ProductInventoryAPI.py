# Task 2 — Product Inventory API 🛒
# Build a Product API:
# Models:

# ProductBase → name (str), price (float, gt=0), in_stock (bool, default=True)
# Product(table=True) → adds id, secret_cost (float)
# ProductPublic → no secret_cost
# ProductCreate → includes secret_cost
# ProductUpdate → all optional

# Routes:

# POST /products/ → create
# GET /products/ → list, filter by in_stock (bool, optional)
# GET /products/{id} → get one
# PATCH /products/{id} → partial update
# DELETE /products/{id} → delete

# Extra:

# Global dependency verify_api_key → header x_api_key == "inventory123"
# All routes protected automatically

from sqlmodel import SQLModel, Field, create_engine, Session, select
from fastapi import FastAPI , Header,HTTPException,status, Depends
from typing import Annotated
from contextlib import asynccontextmanager


def verify_api_key(x_api_key: str | None = Header(default=None)):
    if x_api_key != "inventory123":
        raise HTTPException(
            status_code=401, detail="Invalid API Key"
        )
    return None

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, dependencies=[Depends(verify_api_key)])

sqlite_file_name = "Inventory.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

class ProductBase(SQLModel):
    name: str
    price: float = Field(gt=0)
    in_stock: bool = Field(default=True)

class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_cost: float

class ProductPublic(ProductBase):
    id: int

class ProductCreate(ProductBase):
    secret_cost: float

class ProductUpdate(SQLModel):
    name: str | None = None
    price: float | None = None
    in_stock: bool | None = None
    secret_cost: float | None = None


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


@app.post("/products/", response_model=ProductPublic)
def create_product(product: ProductCreate, session: SessionDep):
    db_product = Product(**product.model_dump())
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@app.get("/products/")
def get_products(session: SessionDep, in_stock: bool | None = None ):
    query = select(Product)
    if in_stock is not None:
        query = query.where(Product.in_stock == in_stock)
    products = session.exec(query).all()
    return products

@app.get("/products/{id}", response_model=ProductPublic)
def get_product(id: int, session: SessionDep):
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404 , detail="Product not found")
    return product

@app.patch("/products/{id}", response_model=ProductPublic)
def update_product(id: int , product: ProductUpdate, session: SessionDep):
# Database ma patch update garna direct override garna mildaina

    db_product = session.get(Product, id)

    # product = session.exec(select(product).where(Product.id == id)).first()

    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product Vetena"
        )
    
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key , value)
    
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@app.delete("/products/{id}", tags=["Products"], summary="Delete Book")
def delete_book(id:int , session:SessionDep):

    # Product fetch garne, check garne, ani database bata delete garera commit garne logic


    db_product = session.get(Product, id)

    if db_product is None: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Kae vaye po delete garna lai"
        )
    
    session.delete(db_product)
    session.commit()

    return db_product

