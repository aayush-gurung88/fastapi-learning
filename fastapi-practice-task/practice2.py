        # ============ Query parameter exmaple gareko ===============

from fastapi import FastAPI

app = FastAPI()


@app.get("/search/{category}")
def search_product(category: str, keyword:str,page:int = 1, active:bool = True):
    # why keyword here - kinanki ? paxi aauxa query
    #  like /search/books?keyword=python
    return {"category":category,
            "keyword":keyword,
            "page":page,
            "active":active}

