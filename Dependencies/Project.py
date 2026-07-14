#  A simple task to understand the following concept clearly
# yield dependencies
# setup/cleanup lifecycle
# exception handling
# shared dependency injection

from fastapi import FastAPI,Depends, Query, HTTPException

app = FastAPI()

rate_limit_store = {}

def get_rate_limiter(user_id: str = Query(...)):
    print(f"[{user_id}] Request started — checking rate limit")

    if user_id not in rate_limit_store:
        rate_limit_store[user_id] = 5

    if rate_limit_store[user_id] <= 0:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    rate_limit_store[user_id] = rate_limit_store[user_id] - 1        

    try:
        yield {"user_id": user_id, 
               "requests_remaining":rate_limit_store[user_id]}


        print(f"[{user_id}] Request finished - decrementing count")

    except Exception:
        print(f"[{user_id}] Request failed - count NOT decremented")
        raise


@app.post("/send-message/")
def send_message(txt:str, rate_limit= Depends(get_rate_limiter)):
    if not txt.strip():
        raise HTTPException(status_code=400, detail="Empty message not allowed")
    return{
        "user_id": rate_limit["user_id"],
        "txt": txt,
        "requests_remaining": rate_limit["requests_remaining"]
    }


@app.get("/status/")
def get_status(rate_limit = Depends(get_rate_limiter)):
    return{
        "user_id": rate_limit["user_id"],
        "requests_remaining": rate_limit["requests_remaining"],
        "api_status": "ok"
    }


@app.put("/update-profile/")
def update_profile(username: str, rate_limit = Depends(get_rate_limiter)):
     return{
          "user_id": rate_limit["user_id"],
          "requests_remaining": rate_limit["requests_remaining"],
          "updated_username": username
     }


