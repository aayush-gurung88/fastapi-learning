from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/")
async def read_items():
    return {"message": "hello users"}

@router.get("/{user_id}")
async def user_profile(user_id:str):
    return {
        "user_id": user_id
    }