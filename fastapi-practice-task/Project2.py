from datetime import datetime
from pydantic import BaseModel , Field
from fastapi import FastAPI,HTTPException
from uuid import UUID , uuid4

app = FastAPI()

fake_db: list[dict] = []


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    title: str = Field(min_length=3 , max_length=100)

    description: str | None = Field(default=None, max_length=300)

    subject: str = Field(min_length=2 , max_length=50)

    priority: str = Field(default="medium")

    completed: bool = False

    due_date: datetime | None = None

    tags: list[str] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.utcnow)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None , min_length=3, max_length=100)
    
    description: str | None = Field(default=None, max_length=300)

    subject: str | None = Field(default=None, min_length=2, max_length=50)

    priority: str | None = None

    completed: bool | None = None

    due_date: datetime | None = None

    tags: list[str] | None = None


@app.post("/tasks/")
def create_task(task:Task):
    fake_db.append(task.model_dump())
    return task


@app.get("/tasks/")
def get_tasks(
    completed: bool | None = None,
    subject: str | None = None,
    priority: str | None = None
):
    result = fake_db

    if completed is not None:
        result = [ 
            t for t in result
                if t["completed"] == completed
        ]
        
    if subject: 
        result = [
            t for t in result
            if t["subject"].lower() == subject.lower()
        ]
    
    if priority: 
        result = [
            t for t in result
            if t["priority"].lower() == priority.lower()
        ]
    return result


# GET single task 
@app.get("/tasks/{task_id}")
def get_task(task_id:UUID):
    for task in fake_db:
        if task["id"] == task_id:
            return task
        
    raise HTTPException(status_code=404, detail="Task not Foound")


# Yo chai generic ho hai 
# @app.put("/tasks/{task_id}")
# def update_task(task_id: UUID, updated_task: TaskUpdate):
#     for task in fake_db:
#         if task["id"] == task_id:
#             return task
    
#     raise HTTPException(status_code=404, detail="Task not fouund")


@app.put("/tasks/{task_id}")
def update_task(task_id: UUID, updated_task: TaskUpdate):
    for task in fake_db:
        if task["id"] == task_id:

            if updated_task.title is not None:
                task["title"] = updated_task.title

            if updated_task.description is not None:
                task["description"] = updated_task.description

            if updated_task.subject is not None:
                task["subject"] = updated_task.subject
            
            if updated_task.priority is not None:
                task["priority"] = updated_task.priority

            if updated_task.due_date is not None:
                task["due_date"] =  updated_task.due_date

            if updated_task.tags is not None:
                task["tags"] = updated_task.tags

            
            return task
    
    raise HTTPException(status_code=404 , detail="Task NOt Found")

# Basic Structure

# @app.delete("/tasks/{task_id}")
# def delete_task(task_id: UUID):
#     for task in fake_db:
#         if task["id"] == task_id:
#             return {"message": "Task deleted"}

#     raise HTTPException(status_code=404, detail="Task not found")



@app.delete("/tasks/{task_id}")
def delete_task(task_id: UUID):
    for index, task in enumerate(fake_db):
        if task["id"] == task_id:
            fake_db.pop(index)
            return {"message": "Task deleted successfully"}

    raise HTTPException(status_code=404, detail="Task not found")