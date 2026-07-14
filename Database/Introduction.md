SQL database with SQL Model 

What id SQL Model?
-- yo vaneko SQLAlchemy + Pydantic model ho 

SQLAlchemy -- talks to the database
Pydantic models --- yo ta validate garna vaihalyo 

SQL model --- combines both , it is made by FastAPI's creator 

What I will use in my learning ?
- SQL Model -- ORM (Object Relational Mapper)
- SQLite -- database(zero setup , and single file )
- paxi - I will change it to postgreSQL 


Why SQLModel:

Made by the same creator as FastAPI 
Built on SQLAlchemy + Pydantic 
<!-- I already know Pydantic — SQLModel might feels identical  -->
Less boilerplate than raw SQLAlchemy 


Why SQLite first:

Zero setup — no installation, no server 
Same SQLModel code works with PostgreSQL later 
Just change one line to switch to PostgreSQL 

# SQLite (learning)
DATABASE_URL = "sqlite:///./test.db"

# PostgreSQL (production) — just change this line
DATABASE_URL = "postgresql://user:password@localhost/dbname"