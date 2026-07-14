
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Definite origins ko list clear dine!

origins = [
     "http://localhost:3000",    # React frontend
    "http://localhost:8080",    # Vue frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,       # who can talk to us
    allow_credentials=True,      # allow cookies + auth headers
    allow_methods=["*"],         # allow all HTTP methods
    allow_headers=["*"], 
)

@app.get("/")
def read_root():
    return {"message": "CORS Fixed & Secure!"}


@app.get("/greet/")
def greet_user(username: str):
    return {"message": f"Hello {username}, CORS is working!"}