import joblib
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent

FEATURE_NAMES = [
    "hours_studied", "previous_scores", "sleep_hours",
    "sample_papers_practiced", "extracurricular"
]

FEATURE_MEANS = {
    "hours_studied": 4.99, "previous_scores": 69.44,
    "sleep_hours": 6.53, "sample_papers_practiced": 4.58,
    "extracurricular": 0.49
}


class Predictor:

    def __init__(self):
        self.classifier = joblib.load(BASE / "model_classifier.pkl")
        self.regressor = joblib.load(BASE / "model_regressor.pkl")
        self.scaler = joblib.load(BASE / "scaler.pkl")
        self.threshold = 40.0

    def _to_array(self, features: dict) -> np.ndarray:
        return np.array([[features[f] for f in FEATURE_NAMES]])

    def _prepare(self, features: dict) -> np.ndarray:
        return self.scaler.transform(self._to_array(features))

    def predict_index(self, features: dict) -> float:
        X = self._prepare(features)
        pred = self.regressor.predict(X)[0]
        return round(float(np.clip(pred, 10, 100)), 2)

    def predict_risk(self, features: dict) -> tuple[bool, str, float]:
        X = self._prepare(features)
        is_low = bool(self.classifier.predict(X)[0])
        proba = self.classifier.predict_proba(X)[0]
        confidence = round(float(max(proba)), 4)
        label = "Bajo Rendimiento" if is_low else "Rendimiento Normal"
        return is_low, label, confidence

    def feature_contributions(self, features: dict) -> dict:
        """Desviacion de cada feature respecto a la media del dataset."""
        contributions = {}
        for f in FEATURE_NAMES:
            delta = features[f] - FEATURE_MEANS[f]
            direction = "above_avg" if delta > 0 else "below_avg" if delta < 0 else "at_avg"
            contributions[f] = {"value": features[f], "delta": round(delta, 2), "direction": direction}
        return contributions

    def full_prediction(self, features: dict) -> dict:
        pred_index = self.predict_index(features)
        is_low, label, confidence = self.predict_risk(features)
        contribs = self.feature_contributions(features)
        return {
            "predicted_performance_index": pred_index,
            "risk_classification": label,
            "is_low_performance": is_low,
            "confidence": confidence,
            "feature_contributions": contribs
        }


predictor = Predictor()
