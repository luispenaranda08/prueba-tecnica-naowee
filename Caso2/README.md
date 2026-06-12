# Student Performance API

API para prediccion de rendimiento academico y deteccion temprana de bajo desempeno en estudiantes de matematicas.

## Arquitectura

```
api/
├── app/
│   ├── main.py              # Entry point
│   ├── schemas.py           # Pydantic models (Input/Output contracts)
│   ├── models/
│   │   └── predictor.py     # Model loading + inference
│   ├── repositories/
│   │   └── student.py       # CRUD (in-memory dictionary store)
│   ├── services/
│   │   └── student.py       # Business logic orchestration
│   └── routers/
│       └── students.py      # HTTP endpoints
├── model_classifier.pkl
├── model_regressor.pkl
├── scaler.pkl
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

Principios SOLID aplicados:
- **Single Responsibility**: cada modulo tiene una unica responsabilidad.
- **Open/Closed**: nuevos modelos se agregan sin modificar la logica existente.
- **Dependency Inversion**: los routers dependen de servicios, no de implementaciones.

## Ejecucion

### Con Docker

```bash
docker compose up --build
```

### Sin Docker

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload
```

La API estara disponible en `http://localhost:8000`.
Swagger UI: `http://localhost:8000/docs`

## Endpoints

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/` | Health check |
| POST | `/students/` | Registrar estudiante (con prediccion) |
| GET | `/students/` | Listar todos |
| GET | `/students/{id}` | Obtener por ID |
| PUT | `/students/{id}` | Actualizar (recalcula prediccion) |
| DELETE | `/students/{id}` | Eliminar |
| POST | `/students/predict` | Prediccion sin registro |

## Ejemplos de uso (curl)

### Crear estudiante
```bash
curl -X POST http://localhost:8000/students/ \
  -H "Content-Type: application/json" \
  -d '{"hours_studied": 7, "previous_scores": 85, "sleep_hours": 7, "sample_papers_practiced": 5, "extracurricular": 1}'
```

### Prediccion sin registro
```bash
curl -X POST http://localhost:8000/students/predict \
  -H "Content-Type: application/json" \
  -d '{"hours_studied": 2, "previous_scores": 42, "sleep_hours": 5, "sample_papers_practiced": 1, "extracurricular": 0}'
```

### Estudiante de alto rendimiento
```bash
curl -X POST http://localhost:8000/students/predict \
  -H "Content-Type: application/json" \
  -d '{"hours_studied": 9, "previous_scores": 95, "sleep_hours": 8, "sample_papers_practiced": 8, "extracurricular": 1}'
```

## Modelos

- **Regresion**: Linear Regression (R2 = 0.988)
- **Clasificacion**: Logistic Regression (F1 = 0.943)
- **Umbral de bajo rendimiento**: Performance Index < 40 (percentil 25)
