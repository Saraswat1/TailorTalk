import datetime
import json
import streamlit as st  # ✅ New for Streamlit secrets
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ✅ Read credentials from Streamlit secrets
SERVICE_ACCOUNT_INFO = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
SCOPES = ["https://www.googleapis.com/auth/calendar"]

credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES
)

# Google Calendar setup
calendar_id = SERVICE_ACCOUNT_INFO["client_email"]

service = build("calendar", "v3", credentials=credentials)


def get_free_slots(date: str):
    start_datetime = datetime.datetime.fromisoformat(date + "T00:00:00")
    end_datetime = datetime.datetime.fromisoformat(date + "T23:59:59.999999")

    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_datetime.isoformat() + "Z",
        timeMax=end_datetime.isoformat() + "Z",
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = events_result.get("items", [])
    booked_slots = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        booked_slots.append({"start": start, "end": end})
    return {"booked_slots": booked_slots}


def book_slot(date: str, time: str, summary: str):
    start_datetime = datetime.datetime.fromisoformat(f"{date}T{time}:00")
    end_datetime = start_datetime + datetime.timedelta(hours=1)

    event = {
        "summary": summary,
        "start": {
            "dateTime": start_datetime.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end_datetime.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
    }

    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()

    return {"status": "success", "event": created_event}
