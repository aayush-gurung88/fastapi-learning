import time 
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request , call_next):
# call_next is a special function provided by FastAPI 
#  is is a function which is used to continue processing the request 
    start_time = time.perf_counter()  #this line runs before the route is executed 
    # and it returns the current high - precision timer value .

    response = await call_next(request) #most important line in the middleware 
    # it tells the fastapi to go and run the endpoint 


    process_time = time.perf_counter() - start_time

    response.headers["X-Process-Time"] = str(process_time)

    return response


@app.get("/")
def home():
    return {
        "message": "hello"
    }
