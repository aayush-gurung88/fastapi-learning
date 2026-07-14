
from fastapi import FastAPI
from fastapi.middleware import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",    # React frontend
    "http://localhost:8080",    # Vue frontend
    "https://myapp.com",        # production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # who can talk to us
    allow_credentials=True,      # allow cookies + auth headers
    allow_methods=["*"],         # allow all HTTP methods
    allow_headers=["*"],         # allow all headers
)   


# Wildcard "*" — Allow Everyone
# allow_origins=["*"]   # anyone can talk to this API

# ⚠️ Can't use "*" with allow_credentials=True — must list origins explicitly then.
