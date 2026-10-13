"""Local training script (mirrors notebooks/train_model_colab.ipynb)."""
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from advisor.data import FEATURES, TARGET, generate_students

df = generate_students()
X_tr, X_te, y_tr, y_te = train_test_split(
    df[FEATURES], df[TARGET], test_size=0.2, stratify=df[TARGET], random_state=42)
model = Pipeline([
    ("scale", StandardScaler()),
    ("clf", LogisticRegression(max_iter=2000, class_weight="balanced")),
]).fit(X_tr, y_tr)
print(classification_report(y_te, model.predict(X_te)))
joblib.dump(model, "models/advisor_model.pkl")
print("Saved models/advisor_model.pkl")
