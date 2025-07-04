from flask import Flask, request, Response
from datetime import datetime, timedelta
import json
from ics import Calendar, Event

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert_json_to_ics():
    data = request.get_json()
    cal = Calendar()

    for person in data:
        name = person["name"]
        for shift in person["shifts"]:
            date_str = shift["date"]
            time_str = shift["time"].split("–")
            start = datetime.strptime(f"{date_str} {time_str[0].strip()}", "%Y-%m-%d %I:%M %p")
            end = datetime.strptime(f"{date_str} {time_str[1].strip()}", "%Y-%m-%d %I:%M %p")
            e = Event()
            e.name = f"{name} Shift"
            e.begin = start
            e.end = end
            cal.events.add(e)

    return Response(str(cal), mimetype="text/calendar")

if __name__ == "__main__":
    app.run(debug=True)
