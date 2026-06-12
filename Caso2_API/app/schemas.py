from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StudentInput(BaseModel):
    hours_studied: int = Field(..., ge=1, le=9)
    previous_scores: int = Field(..., ge=40, le=99)
    sleep_hours: int = Field(..., ge=4, le=9)
    sample_papers_practiced: int = Field(..., ge=0, le=9)
    extracurricular: int = Field(..., ge=0, le=1)

    model_config = {"json_schema_extra": {
        "examples": [{"hours_studied": 7, "previous_scores": 85,
                       "sleep_hours": 7, "sample_papers_practiced": 5, "extracurricular": 1}]
    }}


class StudentRecord(StudentInput):
    id: str
    predicted_index: Optional[float] = None
    predicted_risk: Optional[str] = None
    created_at: Optional[str] = None


class PredictionResponse(BaseModel):
    student_id: str
    predicted_performance_index: float
    risk_classification: str
    is_low_performance: bool
    confidence: float
    feature_contributions: dict


class BatchInput(BaseModel):
    students: list[StudentInput]


class BatchResponse(BaseModel):
    total: int
    at_risk: int
    risk_rate: float
    predictions: list[PredictionResponse]


class CohortAnalysis(BaseModel):
    cohort: str
    n: int
    avg_predicted_index: float
    risk_rate: float
    avg_hours_studied: float
    avg_previous_scores: float


class RiskDistribution(BaseModel):
    total_registered: int
    at_risk_count: int
    normal_count: int
    risk_rate: float
    avg_performance_index: float
    performance_std: float
    risk_by_extracurricular: dict
    top_risk_factors: list[dict]


class ModelMetadata(BaseModel):
    regressor: str
    classifier: str
    regressor_r2: float
    classifier_f1: float
    low_performance_threshold: float
    features: list[str]
    trained_on_n_samples: int


class MessageResponse(BaseModel):
    message: str
    student_id: str
