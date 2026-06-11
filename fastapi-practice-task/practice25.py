#  JSON Compatible Encoder ========

# Practice Task
# Create an Event model with title: str and start_time: datetime.
# In POST /events/ use jsonable_encoder to convert it and store in fake_db, then return the converted data.
# Check that start_time comes back as a string not a datetime object. 

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from pydantic import BaseModel

fake_db = {}


class Event(BaseModel):
    title: str
    start_time: datetime

app = FastAPI()


@app.post("/events/")
def post_event(event: Event):
    encoded_event = jsonable_encoder(event)
    fake_db[event.title] = encoded_event

    print(fake_db[event.title]["start_time"])
    return {
        "encoded_event": encoded_event
    }


#  what I actually did learn in this task


# jsonable_encoder(event) converts the entire object, not just what you “return”
# fake_db is not just “temporary storage”, it’s an in-memory dict (correct idea, but more precise wording)

# Pydantic model usage for request validation
# Raw datetime cannot be directly stored/returned in JSON
# Solution: jsonable_encoder(event) converts model → JSON-safe dict
# In-memory DB (fake_db) stores encoded data (lost on server restart)
# Verified that start_time becomes a string (ISO format)