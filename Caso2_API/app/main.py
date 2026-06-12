from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers.students import router, predict_router, analytics_router
import time

DESCRIPTION = """
## Student Performance Intelligence API

Sistema de deteccion temprana de bajo rendimiento academico en estudiantes de matematicas.

### Arquitectura

La API sigue principios **SOLID** con separacion en capas:

| Capa | Responsabilidad |
|------|----------------|
| `routers/` | Endpoints HTTP |
| `services/` | Logica de negocio |
| `repositories/` | Persistencia (diccionarios en memoria) |
| `models/` | Inferencia ML |

### Modelos en produccion

- **Regresion:** LinearRegression (R² = 0.988)
- **Clasificacion:** LogisticRegression (F1 = 0.943)
- **Umbral de bajo rendimiento:** Performance Index < 40 (percentil 25)

### Secciones

- **CRUD** — Alta, consulta, actualizacion y baja de estudiantes
- **Prediccion** — Inferencia individual y batch con confianza
- **Analytics** — Distribucion de riesgo, cohortes y metadata del modelo
"""

app = FastAPI(
    title="Student Performance API",
    description=DESCRIPTION,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = round((time.perf_counter() - start) * 1000, 2)
    response.headers["X-Process-Time-Ms"] = str(elapsed)
    return response


app.include_router(router)
app.include_router(predict_router)
app.include_router(analytics_router)


@app.get("/", tags=["Health"])
def health():
    return {
        "status": "operational",
        "service": "student-performance-api",
        "version": "1.0.0",
        "models_loaded": True
    }
