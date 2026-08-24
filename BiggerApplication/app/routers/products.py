from fastapi import APIRouter

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/")
async def read_items():
    return {"message": "Hellow Items"}

@router.get("/{product_id}")
async def read_item(product_id:str):
    return {
        "product_id":product_id
    }