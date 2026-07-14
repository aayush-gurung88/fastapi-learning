# ==== Dependencies with Yield ===

# Practice Task
# Create a get_db dependency that:

# Opens a fake DB connection → print("DB opened")
# Yields a fake db object {"connected": True}
# Closes it in finally → print("DB closed")

# Use it in GET /data/ and return the db object.
# Run it and watch the print order in your terminal — you'll see exactly when setup and cleanup happen.

from fastapi import FastAPI, Depends

app = FastAPI()

def get_db():
    try:
        print("DB Opened")
        yield {"connected": True}
    finally:
        print("DB Closed")

@app.get("/data/")
def get_data(db = Depends(get_db)):
    return db

# ✔ Used Depends(get_db) in function parameter
# ✔ Got the returned DB object ({"connected": True})
# ✔ Clean route (no duplication)
# ✔ Correct FastAPI pattern for value injection