from flask import Flask, request, send_from_directory, jsonify
from convert import json_to_ics

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_schedule():
    try:
        schedule_json = request.get_json()
        cal = json_to_ics(schedule_json)

        with open("static/schedule.ics", "w") as f:
            f.writelines(cal.serialize_iter())

        return jsonify({"message": "Schedule converted", "ics_url": "/calendar.ics"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/calendar.ics", methods=["GET"])
def serve_calendar():
    return send_from_directory("static", "schedule.ics", mimetype="text/calendar")

@app.route("/", methods=["GET"])
def index():
    return "Schedule to ICS Converter running."

if __name__ == "__main__":
    app.run()
