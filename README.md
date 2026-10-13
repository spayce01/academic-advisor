# 🎓 Academic Advisor

A hybrid **AI + software-engineering** advising system. A machine-learning model predicts a
student's academic standing (**At Risk / Needs Support / On Track / Excellent**) and a transparent
rule engine turns the student's numbers into specific recommendations. Served through a Flask web app.

| Layer | Technique |
|---|---|
| AI | scikit-learn pipeline (StandardScaler + Logistic Regression), picked by 5-fold CV over 3 candidates |
| Rules | Explainable if-then advice (`advisor/rules.py`) |
| Serving | Flask + `.pkl` loaded with joblib; JSON API + HTML form |
| Engineering | Git/GitHub, modular package, input validation, unit + integration tests, CI (GitHub Actions), pinned dependencies |

## Project layout
```
academic-advisor/
├── advisor/            # core package: data, rules, prediction
├── app/                # Flask app + HTML template
├── models/             # advisor_model.pkl (trained in Colab)
├── notebooks/          # train_model_colab.ipynb
├── tests/              # unittest / pytest suite
├── .github/workflows/  # CI pipeline
├── .vscode/            # Python-optimised VS Code config
├── train.py            # local re-training script
└── requirements*.txt
```

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python -m flask --app "app.main:create_app" run
# open http://127.0.0.1:5000
pytest -v                          # run tests
```

## API
`POST /api/advise` with JSON:
```json
{"gpa":2.1,"attendance_pct":55,"study_hours_week":5,"failed_courses":3,
 "credit_load":22,"assignment_pct":50,"part_time_job_hrs":18}
```
Returns `standing`, `confidence`, `probabilities`, `message`, `advice[]`. Bad input → HTTP 422.

## Retraining
Open `notebooks/train_model_colab.ipynb` in Google Colab → *Runtime ▸ Run all* → download
`advisor_model.pkl` → put it in `models/` → `pytest` → commit.
> ⚠️ A `.pkl` only loads reliably with the **same scikit-learn version** that saved it (pinned in `requirements.txt`).

## Limitations (please read)
* Training data is **synthetic**; accuracy figures (~79%) describe the simulation, not real students.
  Replace `advisor/data.py` with real anonymised records before any real use.
* The tool is **decision support**, not a replacement for a human academic adviser.
