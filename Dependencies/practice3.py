#  ======== Sub-dependencies=========

# Practice Task
# Create this chain:

# extract_token(token: str | None = None) → returns token
# validate_token(token: Annotated[str | None, Depends(extract_token)]) → if token is "secret123" return {"valid": True, "token": token}, else return {"valid": False}
# Use validate_token in GET /dashboard/

# Test with ?token=secret123 and ?token=wrongtoken


from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()

def extract_token (token:str | None = None):
    return token

def validate_token (
        token: Annotated[str, Depends(extract_token)]
):
    if token == "secret123":
        return {"valid":True, "token":token}
    
    else:
        return {"valid":False}


@app.get("/dashboard/")
def get_dashboard(token: Annotated[dict, Depends(validate_token)]):
    return token


# so what we did here is sub - dependencies ko example ho 
# # पहिलो dependency (extract_token)
# User बाट query parameter token extract गर्छ।
# केवल value return गर्छ।
# दोश्रो dependency (validate_token)
# Depends(extract_token) प्रयोग गरेर पहिला function बाट token पाउँछ।
# Token validate गर्छ: "secret123" भए valid True, नभए False।
# Route (/dashboard/)
# केवल validate_token use गर्छ।
# Route लाई extract_token थाहा छैन। FastAPI automatically sub-dependency handle गर्छ।