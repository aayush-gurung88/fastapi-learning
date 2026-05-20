This is MY first FastAPI project . 

What I Have Built ....!! 
A fully working Task Manager REST API with:

Endpoint                           What it does 
POST/tasks/          ------     Create a task
GET/tasks/           ------     Get all tasks with filters 
GET/tasks/{id}       ------     Get one task
PUT/tasks/{id}       ------     Update a task
DELETE/tasks/{id}    ------     Delete a task

What are the terms and concepts that I have used from my learning ......!!!

- Pydantic models +Field validation
- Path + Query params
- Request Body
- UUID extra data type 
- HTTPException for errors
- In-memory database  fake_db = []
    meaning:
        Data disappears when server restarts
        No real database yet
