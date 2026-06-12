from fastapi import APIRouter, HTTPException
from app.schemas import (
    StudentInput, StudentRecord, PredictionResponse, MessageResponse,
    BatchInput, BatchResponse, CohortAnalysis, RiskDistribution, ModelMetadata
)
from app.services.student import student_service

# =========================================================================
# CRUD — Operaciones base
# =========================================================================

router = APIRouter(prefix="/students", tags=["CRUD — Estudiantes"])


@router.post("/", response_model=StudentRecord, status_code=201)
def create_student(student: StudentInput):
    """Registra un estudiante y genera prediccion automatica."""
    return student_service.register(student.model_dump())


@router.get("/", response_model=list[StudentRecord])
def list_students():
    """Retorna todos los estudiantes registrados."""
    return student_service.get_all()


@router.get("/{student_id}", response_model=StudentRecord)
def get_student(student_id: str):
    """Retorna un estudiante por ID."""
    record = student_service.get_student(student_id)
    if not record:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return record


@router.put("/{student_id}", response_model=StudentRecord)
def update_student(student_id: str, student: StudentInput):
    """Actualiza datos y recalcula prediccion."""
    record = student_service.update_student(student_id, student.model_dump())
    if not record:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return record


@router.delete("/{student_id}", response_model=MessageResponse)
def delete_student(student_id: str):
    """Elimina un estudiante."""
    if not student_service.delete_student(student_id):
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"message": "Estudiante eliminado", "student_id": student_id}


# =========================================================================
# PREDICCION — Inferencia individual y batch
# =========================================================================

predict_router = APIRouter(prefix="/predict", tags=["Prediccion"])


@predict_router.post("/", response_model=PredictionResponse)
def predict_single(student: StudentInput):
    """Prediccion individual sin registro. Incluye confianza y contribucion de features."""
    return student_service.predict(student.model_dump())


@predict_router.post("/batch", response_model=BatchResponse)
def predict_batch(batch: BatchInput):
    """Prediccion masiva. Recibe N estudiantes, retorna predicciones y tasa de riesgo agregada."""
    if len(batch.students) > 500:
        raise HTTPException(status_code=400, detail="Maximo 500 estudiantes por batch")
    return student_service.predict_batch([s.model_dump() for s in batch.students])


# =========================================================================
# ANALYTICS — Inteligencia sobre la poblacion registrada
# =========================================================================

analytics_router = APIRouter(prefix="/analytics", tags=["Analytics — Inteligencia Operativa"])


@analytics_router.get("/risk-distribution", response_model=RiskDistribution)
def risk_distribution():
    """Distribucion de riesgo sobre la poblacion registrada.
    Incluye segmentacion por actividades extracurriculares y factores de riesgo dominantes."""
    return student_service.risk_distribution()


@analytics_router.get("/cohorts", response_model=list[CohortAnalysis])
def cohort_analysis():
    """Segmenta la poblacion registrada en cohortes por horas de estudio (bajo/medio/alto)
    y calcula la tasa de riesgo y el rendimiento promedio por cohorte."""
    return student_service.cohort_analysis()


@analytics_router.get("/model-metadata", response_model=ModelMetadata)
def model_metadata():
    """Metadata del modelo en produccion: tipo, metricas de entrenamiento, umbral y features."""
    return {
        "regressor": "LinearRegression",
        "classifier": "LogisticRegression",
        "regressor_r2": 0.9884,
        "classifier_f1": 0.9427,
        "low_performance_threshold": 40.0,
        "features": ["hours_studied", "previous_scores", "sleep_hours",
                      "sample_papers_practiced", "extracurricular"],
        "trained_on_n_samples": 7898
    }
