
import logging
from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# -- CORS --
origins = [
     "http://localhost:3000",    # React frontend
    "http://localhost:8080",    # Vue frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"],         
)


# --- MIDDLEWARES ---

# 1. Error Handler (Outermost layer ma bascha , muni ko j crash bhaye ni catch garchha)
@app.middleware("http")
async def safe_exception_middleware(request:Request, call_next):
    try:
        return await call_next(request)
    except Exception as e: 
        return JSONResponse(
            status_code=500, 
            content={"detail":"Internal server Error"}
        )


# 2. Security Check ( Innermost layer, route ma pugnu vanda paila key check garcha )
@app.middleware("http")
async def check_api_key_middleware(request: Request, call_next):

    # this line does is - it bypass the docs (vaneko that xaina malai aailey)
    if request.url.path in ["/docs", "/openapi.json", "/broken-route/"]:
        return await call_next(request)

    # Request header bata key nikalera check gara 
    api_key = request.headers.get("X-API-Key")
    # check K garne ta vanda 
    # yedi  api_key clear chaina vane return gara JSONResponse (status_code=401)and detail
    if api_key != "super-seceret-token-123":
        return JSONResponse(
            status_code=401, 
            content={"detail": "Invalid or missing API Header ('X-API-Key)"}
        )
    # saab thik xa vane you garne i.e request aagadi badaune
    return await call_next(request)


# We will build a third middleware layer that logs every incoming request's Method (GET/POST) and URL Path to your console before passing it to the route.

# aarko middleware hai yo chai 
@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    print(f"Incoming Request:{request.method} {request.url.path}")
    response = await call_next(request)
    return response


# ---- ROUTES ---- 

@app.get("/tasks/")
def get_tasks():
    return {
        "message":"Here are your private tasks!"
    }

@app.get("/broken-route/")
def break_things():
    result = 1 / 0 
    return {"result":result}


# What I built in here 

# Error catching middleware 
# API key security middleware 
# Docs bypass 
# Early return on invalid key



# FastAPI already has its own exception handler — so your safe_exception_middleware catching 1/0 might not always work as expected because FastAPI catches errors before they bubble up to middleware in some cases.
# For proper error handling → use what you learned before:
# pythonfrom fastapi.exceptions import RequestValidationError
# @app.exception_handler(Exception)



# ah error aayo but aayeko error crash huda browser ma dekhauna ko sato internal json mai matra aayo , yesle garda real world ma pani crash yae way ma handle garna milyo