"""Flask web app serving the academic advisor model (.pkl)."""
from flask import Flask, jsonify, render_template, request

from advisor.data import FEATURES
from advisor.predict import DEFAULT_MODEL, advise, load_model

FIELD_LABELS = {
    "gpa": ("Cumulative GPA (0-5)", "0.1"),
    "attendance_pct": ("Attendance % (0-100)", "1"),
    "study_hours_week": ("Study hours per week", "0.5"),
    "failed_courses": ("Failed / carryover courses", "1"),
    "credit_load": ("Credit units this semester", "1"),
    "assignment_pct": ("Assignment completion % (0-100)", "1"),
    "part_time_job_hrs": ("Paid work hours per week", "0.5"),
}


def create_app(model_path=DEFAULT_MODEL):
    app = Flask(__name__)
    app.config["MODEL"] = load_model(model_path)

    @app.get("/")
    def index():
        return render_template("index.html", fields=FIELD_LABELS)

    @app.get("/health")
    def health():
        return jsonify(status="ok", features=FEATURES)

    @app.post("/api/advise")
    def api_advise():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error="Send a JSON object"), 400
        try:
            return jsonify(advise(app.config["MODEL"], payload))
        except ValueError as e:
            return jsonify(error=str(e)), 422

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
