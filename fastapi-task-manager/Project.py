# part 1 - steups , imports , app create , database create

from fastapi import FastAPI, HTTPException , status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

    
app = FastAPI()

# this is temporary in-memory database
fake_db: list[dict] = []


#  Part 2 ==== Create Task Model 
class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(min_length=3 , max_length=100)
    description: str | None = Field(default=None , max_length=300)
    completed: bool = False
    tags: list[str] = []

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3 , max_length=100)
    description: str | None = Field(default=None ,max_length=300)
    completed: bool | None = None
    tags: list[str] | None = None

# Part 3 === Endpoint banaune

@app.post("/tasks/",tags=["tasks"], summary="Create a task", status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    fake_db.append(task.model_dump())
    return task


@app.get("/tasks/",tags=["tasks"], summary="Get all tasks", status_code=status.HTTP_200_OK)
def get_tasks(
    completed: bool | None = None,
    search: str | None = None,
):
    result = fake_db

    if completed is not None: 
        result = [t for t in result if t["completed"] == completed] 

    if search: 
        result = [t for t in result if search.lower() in t["title"].lower()]

    return result



# single task line

@app.get("/tasks/{task_id}",tags=["tasks"], summary="Get a task by ID", status_code=status.HTTP_200_OK)
def get_task(task_id: UUID):
    for task in fake_db:
        if task["id"] == task_id:
            return task
        
    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/tasks/{task_id}",tags=["tasks"], summary="Update a task", status_code=status.HTTP_200_OK)
def update_task(task_id: UUID, updated_task: TaskUpdate):
    for task in fake_db: 
        if task["id"] == task_id:
            if updated_task.title is not None:
                task["title"] = updated_task.title
            if updated_task.description is not None:
                task["description"] = updated_task.description
            if updated_task.completed is not None:
                task["completed"] = updated_task.completed
            if updated_task.tags is not None:
                task["tags"] = updated_task.tags
            return task
    raise HTTPException(status_code=404 , detail="Task payena Babu!!")


@app.delete("/tasks/{task_id}",tags=["tasks"], summary="Delete a task", status_code=204, status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID):
    for index, task in enumerate(fake_db):
        if task["id"] == task_id:
            fake_db.pop(index)
            return {"Message": "Task deleted successfully"}
    raise HTTPException( status_code=404, 
                        detail=" Delete Garna Task Payena")


# Did this part later
@app.patch("/tasks/{task_id}")
def patch_task(task_id: UUID, task_update: TaskUpdate):
    for index, task in enumerate(fake_db):
        if task["id"] == task_id:
            # Step 1 — convert stored dict to Pydantic model
            stored_task_model = Task(**task)

            # Step 2 — get only sent fields
            update_data = task_update.model_dump(exclude_unset=True)

            # Step 3 — merge old + new
            updated_task = stored_task_model.model_copy(update=update_data)

            # Step 4 — save back
            fake_db[index] = jsonable_encoder(updated_task)

            return updated_task

    raise HTTPException(status_code=404, detail="Task not found")