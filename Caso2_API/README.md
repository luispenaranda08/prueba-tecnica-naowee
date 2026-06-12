# Student Performance API

Sistema de deteccion temprana de bajo rendimiento academico en matematicas. Predice el indice de rendimiento y clasifica estudiantes en riesgo a partir de 5 variables academicas.

## Arquitectura

```
Caso2_API/
├── app/
│   ├── main.py              # Entry point + middleware
│   ├── schemas.py           # Contratos de entrada/salida (Pydantic)
│   ├── models/
│   │   └── predictor.py     # Carga de modelos + inferencia
│   ├── repositories/
│   │   └── student.py       # CRUD en memoria (diccionarios)
│   ├── services/
│   │   └── student.py       # Orquestacion de logica de negocio
│   └── routers/
│       └── students.py      # Definicion de endpoints
├── model_classifier.pkl     # LogisticRegression (F1 = 0.943)
├── model_regressor.pkl      # LinearRegression (R2 = 0.988)
├── scaler.pkl               # StandardScaler entrenado
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

Principios SOLID:
- **Single Responsibility**: cada modulo tiene una unica funcion.
- **Open/Closed**: nuevos modelos se integran sin modificar endpoints.
- **Dependency Inversion**: routers dependen de servicios, no de implementaciones.

## Ejecucion

### Docker
```bash
docker compose up --build
```

### Sin Docker
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger UI: http://localhost:8000/docs

## Endpoints

### CRUD
| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| POST | `/students/` | Registrar estudiante (con prediccion) |
| GET | `/students/` | Listar todos |
| GET | `/students/{id}` | Obtener por ID |
| PUT | `/students/{id}` | Actualizar (recalcula prediccion) |
| DELETE | `/students/{id}` | Eliminar |

### Prediccion
| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| POST | `/predict/` | Prediccion individual con confianza |
| POST | `/predict/batch` | Prediccion masiva (hasta 500) |

### Analytics
| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/analytics/risk-distribution` | Distribucion de riesgo + factores |
| GET | `/analytics/cohorts` | Segmentacion por horas de estudio |
| GET | `/analytics/model-metadata` | Metadata del modelo en produccion |

## Ejemplos

### Estudiante en riesgo
```bash
curl -X POST http://localhost:8000/predict/ \
  -H "Content-Type: application/json" \
  -d '{"hours_studied":2,"previous_scores":42,"sleep_hours":5,"sample_papers_practiced":1,"extracurricular":0}'
```

### Prediccion batch
```bash
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{"students":[
    {"hours_studied":2,"previous_scores":42,"sleep_hours":5,"sample_papers_practiced":1,"extracurricular":0},
    {"hours_studied":8,"previous_scores":92,"sleep_hours":8,"sample_papers_practiced":7,"extracurricular":1},
    {"hours_studied":5,"previous_scores":65,"sleep_hours":6,"sample_papers_practiced":3,"extracurricular":1}
  ]}'
```
