from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'backend/credentials.json'
CALENDAR_ID = 'chakrabortysaraswat52@gmail.com'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('calendar', 'v3', credentials=credentials)

def get_free_slots(date_str):
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    start_datetime = datetime.datetime.combine(date, datetime.time.min).isoformat() + 'Z'
    end_datetime = datetime.datetime.combine(date, datetime.time.max).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_datetime,
        timeMax=end_datetime,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    return {"booked_slots": [(e['start']['dateTime'], e['end']['dateTime']) for e in events]}

def book_slot(date, time, summary):
    start_datetime = f"{date}T{time}:00"
    end_datetime = f"{date}T{int(time[:2])+1:02d}:{time[3:]}:00"

    event = {
        'summary': summary,
        'start': {'dateTime': start_datetime, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_datetime, 'timeZone': 'Asia/Kolkata'},
    }

    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return {"status": "success", "event": created_event}
