"""Loads the .pkl model and produces a full advising report."""
from pathlib import Path
import joblib
import pandas as pd

from .data import FEATURES
from .rules import STANDING_MESSAGE, build_advice

DEFAULT_MODEL = Path(__file__).resolve().parent.parent / "models" / "advisor_model.pkl"

# (min, max) sanity limits for input validation
LIMITS = {
    "gpa": (0, 5), "attendance_pct": (0, 100), "study_hours_week": (0, 80),
    "failed_courses": (0, 20), "credit_load": (0, 40),
    "assignment_pct": (0, 100), "part_time_job_hrs": (0, 80),
}


def load_model(path=DEFAULT_MODEL):
    return joblib.load(path)


def validate(payload: dict) -> dict:
    clean = {}
    for f in FEATURES:
        if f not in payload or payload[f] in ("", None):
            raise ValueError(f"Missing field: {f}")
        try:
            v = float(payload[f])
        except (TypeError, ValueError):
            raise ValueError(f"{f} must be a number")
        lo, hi = LIMITS[f]
        if not lo <= v <= hi:
            raise ValueError(f"{f} must be between {lo} and {hi}")
        clean[f] = v
    return clean


def advise(model, payload: dict) -> dict:
    student = validate(payload)
    X = pd.DataFrame([student], columns=FEATURES)
    standing = str(model.predict(X)[0])
    probs = model.predict_proba(X)[0]
    return {
        "standing": standing,
        "confidence": round(float(max(probs)), 3),
        "probabilities": {c: round(float(p), 3) for c, p in zip(model.classes_, probs)},
        "message": STANDING_MESSAGE[standing],
        "advice": build_advice(student),
    }
