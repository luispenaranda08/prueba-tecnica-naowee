# Prueba Técnica — Científico de Datos | Naowee

Análisis de datos y desarrollo de producto de datos para el proceso de selección de **Naowee**.

## Estructura del repositorio

    PruebaTecnica_Naowee/
    ├── Caso1/
    │   └── Caso1_Copa_Mundial_Femenina.ipynb
    ├── Caso2/
    │   ├── Caso2_Desempeño_Matematicas.ipynb
    │   ├── diccionario_datos.csv
    │   ├── 01_distribuciones.png
    │   ├── 02_correlacion.png
    │   ├── 03_scatter_principales.png
    │   ├── 04_extracurricular_vs_performance.png
    │   ├── 05_elbow_method.png
    │   └── 06_clusters.png
    └── Caso2_API/
        ├── app/
        │   ├── main.py
        │   ├── schemas.py
        │   ├── models/
        │   ├── repositories/
        │   ├── services/
        │   └── routers/
        ├── model_classifier.pkl
        ├── model_regressor.pkl
        ├── scaler.pkl
        ├── Dockerfile
        ├── docker-compose.yml
        └── requirements.txt

---

## Caso 1 — Copa Mundial Femenina FIFA

Análisis de 348 partidos a través de 9 ediciones del torneo (1991–2023). Incluye:

- Reporte de calidad de datos y validación cruzada entre datasets
- Tabla de posiciones del mundial 1991 (puntos, diferencia de goles, juego limpio)
- Tabla de goleadoras del mundial 2023 (incluye goles de penal)
- Tabla resumen histórica por equipo y edición (168 filas)
- Análisis de tendencias: caída del promedio de goles por partido de 3.81 a 2.56 (1991→2023), evidenciando la democratización competitiva del torneo

**Notebook:** `Caso1/Caso1_Copa_Mundial_Femenina.ipynb`

---

## Caso 2 — Desempeño Académico en Matemáticas

Análisis exploratorio, prueba de hipótesis y modelado predictivo sobre 10,000 estudiantes.

**Hallazgos principales:**
- `Previous Scores` correlaciona con `Performance Index` (r = 0.915) — predictor dominante
- Las actividades extracurriculares muestran diferencia estadísticamente significativa (p = 0.01) pero efecto despreciable (Cohen's d = 0.052)
- Clustering (k=3) revela que estudiantes con historial similar logran rendimientos muy distintos según horas de estudio (2.6h → Performance Index 35.9 vs 7.2h → 48.4)

**Modelos:**

| Tipo | Modelo | Métrica |
|---|---|---|
| Regresión | Linear Regression | R² = 0.988 |
| Clasificación | Logistic Regression | F1 = 0.943 |

**Notebook:** `Caso2/Caso2_Desempeño_Matematicas.ipynb`

---

## API — Student Performance Intelligence

API REST en FastAPI que expone los modelos entrenados como producto de datos.

**Arquitectura (SOLID, por capas):**

    app/
    ├── routers/       → endpoints HTTP
    ├── services/      → lógica de negocio
    ├── repositories/  → persistencia (in-memory)
    └── models/        → inferencia ML

**Secciones:**
- **CRUD** — alta, consulta, actualización y baja de estudiantes
- **Predicción** — inferencia individual y batch con score de confianza
- **Analytics** — distribución de riesgo, segmentación por cohortes, metadata del modelo

### Ejecución

Con Docker:

    cd Caso2_API
    docker compose up --build

Sin Docker:

    cd Caso2_API
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload

Documentación interactiva: `http://localhost:8000/docs`

---

## Stack

Python · pandas · scikit-learn · FastAPI · Docker · matplotlib/seaborn

---

**Autor:** Luis David Peñaranda Pérez
Científico de Datos — Universidad del Norte
