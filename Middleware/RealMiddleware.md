if request.url.path in ["/docs", "/openapi.json"]:
    return await call_next(request)  # skip API key check, go straight to route

    Here is what this piece of code does 

It's called whitelisting public routes. Which is important and common pattern in real projects 

In plain english : 
- Every request goes through the API key middleware 
- But /docs and /openapi.json are FASTAPI's built-in pages 
- They don't send and X-API-Key header 
- So without this bypass - docs would return 401 unauthorized 
- with this bypass - docs load fine , everything else still needs the key 
