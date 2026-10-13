"""Unit + integration tests. Run with:  python -m unittest -v   (or: pytest)"""
import unittest

from advisor.data import FEATURES, generate_students
from advisor.predict import advise, load_model, validate
from advisor.rules import build_advice
from app.main import create_app

STRONG = dict(gpa=4.6, attendance_pct=95, study_hours_week=20, failed_courses=0,
              credit_load=18, assignment_pct=95, part_time_job_hrs=2)
WEAK = dict(gpa=1.4, attendance_pct=40, study_hours_week=2, failed_courses=5,
            credit_load=24, assignment_pct=30, part_time_job_hrs=25)


class TestData(unittest.TestCase):
    def test_shape_and_classes(self):
        df = generate_students(500)
        self.assertEqual(len(df), 500)
        self.assertEqual(set(df.standing), {"At Risk", "Needs Support", "On Track", "Excellent"})


class TestRules(unittest.TestCase):
    def test_weak_student_gets_many_tips(self):
        self.assertGreaterEqual(len(build_advice(WEAK)), 4)

    def test_strong_student_gets_positive_tip(self):
        self.assertIn("Keep up", build_advice(STRONG)[0])


class TestModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = load_model()

    def test_strong_vs_weak(self):
        self.assertIn(advise(self.model, STRONG)["standing"], ("Excellent", "On Track"))
        self.assertEqual(advise(self.model, WEAK)["standing"], "At Risk")

    def test_probabilities_sum_to_one(self):
        p = advise(self.model, STRONG)["probabilities"]
        self.assertAlmostEqual(sum(p.values()), 1.0, places=2)

    def test_validation(self):
        with self.assertRaises(ValueError):
            validate({**STRONG, "gpa": 9})
        with self.assertRaises(ValueError):
            validate({k: v for k, v in STRONG.items() if k != "gpa"})
        with self.assertRaises(ValueError):
            validate({**STRONG, "gpa": "abc"})


class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_home_page(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"Academic Advisor", r.data)
        for f in FEATURES:
            self.assertIn(f.encode(), r.data)

    def test_health(self):
        self.assertEqual(self.client.get("/health").get_json()["status"], "ok")

    def test_api_success(self):
        r = self.client.post("/api/advise", json=WEAK)
        self.assertEqual(r.status_code, 200)
        body = r.get_json()
        self.assertEqual(body["standing"], "At Risk")
        self.assertTrue(body["advice"])

    def test_api_bad_input(self):
        self.assertEqual(self.client.post("/api/advise", json={**WEAK, "gpa": 10}).status_code, 422)
        self.assertEqual(self.client.post("/api/advise", data="nope").status_code, 400)


if __name__ == "__main__":
    unittest.main()
