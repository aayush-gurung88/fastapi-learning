from fastapi import FastAPI,Body
from TodoModel import Todo
from datetime import datetime
from TodoRequest import TodoRequest
app = FastAPI(
    title= "aayushFASTApi Tutorial",
    version= "0.0.1",
    description= "This is the chapter 2 and project 2",
)

TODOS = [
    Todo(1, 'task1',"My task one ",False,2),
    Todo(2, 'task2',"My task one ",True,3),
    Todo(3, 'task3',"My task one ",True,2),
    Todo(4, 'task4',"My task one ",False,1),
    Todo(5, 'task5',"My task one ",True,2)
    ]

@app.get('/todos/all')
async def get():
    return TODOS

@app.post('/todos/create')
async def create_todo(todo : TodoRequest):
    print(type(todo))
    t = Todo(**todo.dict())
    TODOS.append(get_todo_id(t))
    # TODOS.append(todo)
    # return todo
    return t


def get_todo_id(todo):
    if len(TODOS) == 0:
        todo.id = 1
    else:
        todo.id = TODOS[-1].id + 1
    return todo