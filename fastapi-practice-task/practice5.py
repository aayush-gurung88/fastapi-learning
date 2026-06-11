# ============ Concept: FastAPI Query Parameter Validation + Type Reuse
# what i learned here 
# query parameter handling 
# input validation 
# alias mapping (search-term --> keyword)
# ----> API contarct design (frontend --- backend mapping)
# type alias reuse (kasari vand KeywordQuery = Annotated garera )

from fastapi import FastAPI, Query
from typing import Annotated


app = FastAPI()


# create a reusable Query type
KeywordQuery = Annotated[
        str , 
        Query(min_length=3, 
        max_length=30, 
        alias="search-term", 
        title="Search Keyword", 
        description="Keyword used to search items, must be 3-30 characters long")]


# This is the endpoint and we use the above query in this endpoint
@app.get("/search")
def search(keyword: KeywordQuery):
    return {
        "keyword": keyword
    }