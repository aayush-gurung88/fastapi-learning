# Task
# Build a fake "transaction" system:

# Create a get_transaction dependency that:

# Opens a transaction → print("Transaction started")
# Yields {"transaction_id": "txn_123", "active": True}
# On success → print("Transaction committed")
# On error → print("Transaction rolled back") then re-raise


# Use it in two routes:

# POST /payment/ → accepts amount: float as query param, returns transaction + amount
# GET /balance/ → returns transaction + {"balance": 1000}


# Watch terminal for print order on each request

# Bonus → in /payment/ raise an HTTPException if amount <= 0 and confirm "rolled back" prints in terminal. 

from fastapi import FastAPI, Depends, HTTPException, status

app = FastAPI()

def get_transaction():
    try:
        print("Transaction started")
        yield {"transaction_id": "txn_123", "active": True}
        print("Transaction committed")
    except Exception:
        print("Transaction Rolled Back")
        raise 


@app.post("/payment/")
def create_payment(amount:float, 
                   transaction = Depends(get_transaction)):  
    if amount <= 0:
            raise HTTPException(
                status_code= 400,
                detail= "Invalid amount")
    return {
        "transaction": transaction,
        "amount": amount
    }

@app.get("/balance/")
def get_balance(transaction= Depends(get_transaction)):
    return {
         "transaction": transaction,
         "balance": 1000
    }