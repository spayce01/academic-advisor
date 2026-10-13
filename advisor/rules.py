"""Rule-based advice layer (the 'standard software' half of the hybrid system).

The ML model predicts the student's standing; these transparent rules turn the
student's raw numbers into specific, explainable recommendations.
"""


def build_advice(s: dict) -> list[str]:
    tips = []
    if s["attendance_pct"] < 70:
        tips.append("Attendance is below 70%. Aim for at least 80%, since missed classes are the strongest predictor of falling behind.")
    if s["study_hours_week"] < 8:
        tips.append("Increase self-study to at least 10 hours per week, using a fixed weekly timetable.")
    if s["failed_courses"] >= 2:
        tips.append("You have multiple carryovers. Meet your course adviser to plan a recovery schedule.")
    if s["credit_load"] > 21 and s["gpa"] < 3.0:
        tips.append("Your credit load is heavy for your current GPA. Consider reducing it if the regulations allow.")
    if s["part_time_job_hrs"] > 20:
        tips.append("Paid work exceeds 20 hours a week and may be hurting your studies. Discuss options with the student affairs office.")
    if s["assignment_pct"] < 60:
        tips.append("Submit more assignments and continuous-assessment tasks; they are easy marks.")
    if not tips:
        tips.append("Keep up the current habits. Consider peer tutoring, research or leadership roles.")
    return tips


STANDING_MESSAGE = {
    "At Risk": "Urgent: book a meeting with your academic adviser this week.",
    "Needs Support": "You are slipping in some areas; a few changes now will prevent problems later.",
    "On Track": "You are doing well and are on course to graduate on time.",
    "Excellent": "Outstanding performance. Keep it up.",
}
