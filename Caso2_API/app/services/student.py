from app.repositories.student import student_repo
from app.models.predictor import predictor, FEATURE_NAMES
from typing import Optional
import numpy as np


class StudentService:

    def __init__(self):
        self.repo = student_repo
        self.model = predictor

    def register(self, data: dict) -> dict:
        record = self.repo.create(data)
        prediction = self.model.full_prediction(data)
        record["predicted_index"] = prediction["predicted_performance_index"]
        record["predicted_risk"] = prediction["risk_classification"]
        self.repo.update(record["id"], record)
        return record

    def predict(self, data: dict, student_id: str = "sin_registro") -> dict:
        result = self.model.full_prediction(data)
        return {"student_id": student_id, **result}

    def predict_batch(self, students: list[dict]) -> dict:
        predictions = []
        for i, s in enumerate(students):
            pred = self.predict(s, student_id=f"batch_{i:03d}")
            predictions.append(pred)

        at_risk = sum(1 for p in predictions if p["is_low_performance"])
        return {
            "total": len(predictions),
            "at_risk": at_risk,
            "risk_rate": round(at_risk / len(predictions), 4) if predictions else 0,
            "predictions": predictions
        }

    def get_student(self, student_id: str) -> Optional[dict]:
        return self.repo.get(student_id)

    def get_all(self) -> list[dict]:
        return self.repo.get_all()

    def update_student(self, student_id: str, data: dict) -> Optional[dict]:
        existing = self.repo.get(student_id)
        if not existing:
            return None
        existing.update(data)
        pred_index = self.model.predict_index(existing)
        is_low, label, _ = self.model.predict_risk(existing)
        existing["predicted_index"] = pred_index
        existing["predicted_risk"] = label
        return self.repo.update(student_id, existing)

    def delete_student(self, student_id: str) -> bool:
        return self.repo.delete(student_id)

    # --- Analytics ---

    def risk_distribution(self) -> dict:
        all_students = self.repo.get_all()
        if not all_students:
            return {"total_registered": 0, "at_risk_count": 0, "normal_count": 0,
                    "risk_rate": 0, "avg_performance_index": 0, "performance_std": 0,
                    "risk_by_extracurricular": {}, "top_risk_factors": []}

        at_risk = self.repo.filter_by_risk("Bajo Rendimiento")
        normal = self.repo.filter_by_risk("Rendimiento Normal")
        indices = [s.get("predicted_index", 0) for s in all_students]

        risk_extra = {}
        for label in [0, 1]:
            group = [s for s in all_students if s.get("extracurricular") == label]
            if group:
                risk_in_group = sum(1 for s in group if s.get("predicted_risk") == "Bajo Rendimiento")
                key = "Con Extracurricular" if label == 1 else "Sin Extracurricular"
                risk_extra[key] = {"n": len(group), "at_risk": risk_in_group,
                                   "risk_rate": round(risk_in_group / len(group), 4)}

        at_risk_students = at_risk
        factors = []
        if at_risk_students:
            avg_hours = np.mean([s["hours_studied"] for s in at_risk_students])
            avg_scores = np.mean([s["previous_scores"] for s in at_risk_students])
            factors = [
                {"factor": "previous_scores", "avg_in_risk_group": round(avg_scores, 2),
                 "population_avg": 69.44, "interpretation": "Principal predictor de riesgo"},
                {"factor": "hours_studied", "avg_in_risk_group": round(avg_hours, 2),
                 "population_avg": 4.99, "interpretation": "Segundo predictor relevante"}
            ]

        return {
            "total_registered": len(all_students),
            "at_risk_count": len(at_risk),
            "normal_count": len(normal),
            "risk_rate": round(len(at_risk) / len(all_students), 4),
            "avg_performance_index": round(np.mean(indices), 2),
            "performance_std": round(np.std(indices), 2),
            "risk_by_extracurricular": risk_extra,
            "top_risk_factors": factors
        }

    def cohort_analysis(self) -> list[dict]:
        all_students = self.repo.get_all()
        if not all_students:
            return []

        def bucket(hours):
            if hours <= 3: return "1-3h (bajo)"
            if hours <= 6: return "4-6h (medio)"
            return "7-9h (alto)"

        cohorts = {}
        for s in all_students:
            key = bucket(s["hours_studied"])
            if key not in cohorts:
                cohorts[key] = []
            cohorts[key].append(s)

        result = []
        for cohort_name, students in sorted(cohorts.items()):
            at_risk = sum(1 for s in students if s.get("predicted_risk") == "Bajo Rendimiento")
            result.append({
                "cohort": cohort_name,
                "n": len(students),
                "avg_predicted_index": round(np.mean([s.get("predicted_index", 0) for s in students]), 2),
                "risk_rate": round(at_risk / len(students), 4),
                "avg_hours_studied": round(np.mean([s["hours_studied"] for s in students]), 2),
                "avg_previous_scores": round(np.mean([s["previous_scores"] for s in students]), 2)
            })
        return result


student_service = StudentService()
