# YO CHAI MIDDLEWARE LEKHNE STANDARD FORMATE HO HAI 

from fastapi import FastAPI, Request

app = FastAPI() #yesko muni lekhna parxa hai 


# 1. Decorator
@app.middleware("http")
# 2. Async Function (request ra call_next linaiparchha)
async def my_middleware_name(request: Request, call_next):
    
    # 3. Request aauda garne kaam (Logic / Condition)
    # Jastai: check garne, print garne, mathi block garne
    
    # 4. Request lai agadi badhaune (Call Next)
    response = await call_next(request)
        
    # 5. Response farkida garne kaam (Optional)
    # Jastai: header thapne, timing check garne
    
    # 6. Return Response
    return response