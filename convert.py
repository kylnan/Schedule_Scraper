from ics import Calendar, Event
from datetime import datetime
import pytz

def json_to_ics(data):
    cal = Calendar()
    timezone = pytz.timezone("America/Los_Angeles")

    for item in data.get("events", []):
        event = Event()
        event.name = item.get("title", "Shift")
        start = timezone.localize(datetime.fromisoformat(item["start"]))
        end = timezone.localize(datetime.fromisoformat(item["end"]))
        event.begin = start
        event.end = end
        event.description = item.get("notes", "")
        cal.events.add(event)

    return cal
