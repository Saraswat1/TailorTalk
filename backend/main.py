from fastapi import FastAPI
from backend.calendar_utils import get_free_slots, book_slot

app = FastAPI()

@app.get("/slots")
def slots(date: str):
    return get_free_slots(date)

@app.post("/book")
def book(date: str, time: str, summary: str):
    return book_slot(date, time, summary)
