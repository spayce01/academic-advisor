"""Synthetic student data generator.

Real student records are private, so we simulate a realistic dataset.
Replace `generate_students` with a loader for real (anonymised) data later.
"""
import numpy as np
import pandas as pd

FEATURES = [
    "gpa",               # cumulative GPA on a 5.0 scale
    "attendance_pct",    # class attendance, 0-100
    "study_hours_week",  # self-study hours per week
    "failed_courses",    # number of failed/carryover courses
    "credit_load",       # credit units registered this semester
    "assignment_pct",    # assignment/CA completion rate, 0-100
    "part_time_job_hrs", # paid work hours per week
]
TARGET = "standing"
LABELS = ["At Risk", "Needs Support", "On Track", "Excellent"]


def generate_students(n: int = 3000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    attendance = np.clip(rng.normal(75, 15, n), 20, 100)
    study = np.clip(rng.normal(12, 6, n), 0, 40)
    assignment = np.clip(0.6 * attendance + rng.normal(25, 12, n), 0, 100)
    job = np.clip(rng.exponential(6, n), 0, 35)
    credit = rng.integers(12, 25, n)
    gpa = np.clip(
        1.2 + 0.018 * attendance + 0.045 * study + 0.012 * assignment
        - 0.02 * job + rng.normal(0, 0.35, n), 0.0, 5.0)
    failed = np.clip(np.round((3.2 - gpa) * 1.2 + rng.normal(0, 0.8, n)), 0, 8).astype(int)

    df = pd.DataFrame({
        "gpa": gpa.round(2), "attendance_pct": attendance.round(1),
        "study_hours_week": study.round(1), "failed_courses": failed,
        "credit_load": credit, "assignment_pct": assignment.round(1),
        "part_time_job_hrs": job.round(1),
    })
    score = (df.gpa * 1.0 + df.attendance_pct / 50 + df.assignment_pct / 60
             - df.failed_courses * 0.4 + rng.normal(0, 0.3, n))
    # quantile cut -> realistic class mix: ~12% At Risk, 23% Needs Support,
    # 40% On Track, 25% Excellent
    df[TARGET] = pd.qcut(score, q=[0, 0.12, 0.35, 0.75, 1.0],
                         labels=LABELS).astype(str)
    return df
