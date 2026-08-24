from fastapi import FastAPI,Depends
from .routers import products, users
from .dependencies import verify_api_key

app = FastAPI(dependencies=[Depends(verify_api_key)])

app.include_router(products.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {
        "message" : "Hello Bigger App!"
    }