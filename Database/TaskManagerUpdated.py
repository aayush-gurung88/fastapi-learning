# part 1 - steups , imports , app create , database create

from fastapi import FastAPI, HTTPException , status, Depends,Request
from sqlmodel import SQLModel, create_engine, Session, select,Field
from typing import Annotated
import time
import uuid

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


origins = [
    "http://localhost:3000",  # React frontend
    "http://localhost:8080",  # Vue frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Allowed list thapiyo 
    allow_credentials=True,      # Credentials true safely set 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Another Middleware

# yo chai security middleware
@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]

    print(f"Request_ID: {request_id}")

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    return response


# Another Middlerware 

# yo chai error middleware hai 
@app.middleware("http")
async def block_bad_header_middleware(request: Request, call_next):

    if request.headers.get("x-blocked") == "true":
        return JSONResponse(status_code=403, 
                            content={"detail": "Blocked request"})
    

    response = await call_next(request)

    return response

# Middleware 1 - logging
@app.middleware("http")
async def logging_middleware(request: Request , call_next):
    print(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"Response: {response.status_code}")
    return response

# Middleware 2 - timing 
@app.middleware("http")
async def timing_middleware(request: Request, call_next ):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
        

sqlite_file_name = "taskdatabase.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


# table create gareko 

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Session dependency banako 
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

class TaskBase(SQLModel):
    title: str = Field(min_length=3 , max_length=100)
    description: str | None = Field(default=None , max_length=300)
    completed: bool = False
    tags: str | None = None

class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

# Response model so no primarykey needed 
class TaskPublic(TaskBase):
    id: int 

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=3 , max_length=100)
    description: str | None = Field(default=None ,max_length=300)
    completed: bool | None = None
    tags: str | None = None  # store as "tag1,tag2,tag3"


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/tasks/", response_model=TaskPublic)
def create_task(task:TaskCreate, session: SessionDep ):
    db_task = Task.model_validate(task)
    session.add(db_task )
    session.commit()
    session.refresh(db_task)
    return db_task


@app.get("/tasks/",response_model=list[TaskPublic])
def get_tasks(session: SessionDep):
    query = select(Task)
    tasks = session.exec(query).all()
    return tasks

# single task line
@app.get("/tasks/{task_id}", response_model=TaskPublic)
def get_task(task_id:int , session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: int,task_update: TaskUpdate, session: SessionDep):
    # DB bata purano data lyayo
    task = session.get(Task, task_id)
    if not task: 
        raise HTTPException(status_code=404, detail="Task Payena ni Kancha")
    
    # userley deko field matra nikalyo
    update_data = task_update.model_dump(exclude_unset=True)

    for key , value in update_data.items():
        # purano task update garyo
        setattr(task,key,value)

    session.add(task)
    # database ma save gareko 
    session.commit()
    session.refresh(task)

    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id:int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Temle vaneko task xaina")
    
    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}



@app.patch("/tasks/{task_id}")
def patch_task(task_id: int ,task_update: TaskUpdate, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Paudai payena")
    
    patch_data = task_update.model_dump(exclude_unset=True)

    for key , value in patch_data.items():
        # purano task update garyo
        setattr(task,key,value)

    session.commit()
    session.refresh(task)
    return task
