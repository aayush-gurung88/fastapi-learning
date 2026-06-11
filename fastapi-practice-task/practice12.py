# EXTRA DATA TYPES 
# Practice Task
# Make POST /events/ with a body containing:

# event_id → UUID (path param)
# start_date → datetime
# duration_seconds → timedelta
# reminder_at → time | None, optional

# Inside the function, calculate end_date = start_date + duration_seconds and return it along with all fields.

from fastapi import FastAPI, Body
from uuid import UUID
from datetime import datetime, timedelta , time
from pydantic import BaseModel
from typing import Annotated

class EventCreate(BaseModel):
    start_date: datetime
    duration_seconds: timedelta
    reminder_at: time | None = None


app = FastAPI()

@app.post("/events/{event_id}")
def create_events(
    event_id: UUID,event: EventCreate):
    return {
        "event_id" : event_id,
        "start_date" : event.start_date,
        "duration_seconds" : event.duration_seconds, 
        "end_date" : event.start_date + event.duration_seconds,
        "reminder_at" : event.reminder_at
    }
