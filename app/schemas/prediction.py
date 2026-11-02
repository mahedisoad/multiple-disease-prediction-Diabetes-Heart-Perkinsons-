"""
Pydantic v2 request/response schemas for all disease prediction endpoints.
All field names, types, and validation ranges are derived from the original
training notebooks and datasets — never guessed.
"""
from pydantic import BaseModel, Field
from typing import Optional


# ─────────────────────────────────────────────
#  DIABETES  (8 features — PIMA dataset)
# ─────────────────────────────────────────────
class DiabetesPredictionRequest(BaseModel):
    """Request schema for diabetes prediction. Feature order matches the original SVM model."""

    Pregnancies: int = Field(
        ..., ge=0, le=20,
        description="Number of times pregnant",
        json_schema_extra={"example": 5},
    )
    Glucose: float = Field(
        ..., ge=0, le=300,
        description="Plasma glucose concentration (mg/dL)",
        json_schema_extra={"example": 166},
    )
    BloodPressure: float = Field(
        ..., ge=0, le=200,
        description="Diastolic blood pressure (mm Hg)",
        json_schema_extra={"example": 72},
    )
    SkinThickness: float = Field(
        ..., ge=0, le=110,
        description="Triceps skin fold thickness (mm)",
        json_schema_extra={"example": 19},
    )
    Insulin: float = Field(
        ..., ge=0, le=900,
        description="2-Hour serum insulin (mu U/ml)",
        json_schema_extra={"example": 175},
    )
    BMI: float = Field(
        ..., ge=0, le=80,
        description="Body mass index (kg/m²)",
        json_schema_extra={"example": 25.8},
    )
    DiabetesPedigreeFunction: float = Field(
        ..., ge=0, le=3.0,
        description="Diabetes pedigree function score",
        json_schema_extra={"example": 0.587},
    )
    Age: int = Field(
        ..., ge=1, le=120,
        description="Age in years",
        json_schema_extra={"example": 51},
    )


# ─────────────────────────────────────────────
#  HEART DISEASE  (13 features — Cleveland dataset)
# ─────────────────────────────────────────────
class HeartDiseasePredictionRequest(BaseModel):
    """Request schema for heart disease prediction. Feature order matches the original LogisticRegression model."""

    age: int = Field(
        ..., ge=1, le=120,
        description="Age in years",
        json_schema_extra={"example": 62},
    )
    sex: int = Field(
        ..., ge=0, le=1,
        description="Sex (1 = male, 0 = female)",
        json_schema_extra={"example": 0},
    )
    cp: int = Field(
        ..., ge=0, le=3,
        description="Chest pain type (0–3)",
        json_schema_extra={"example": 0},
    )
    trestbps: float = Field(
        ..., ge=0, le=300,
        description="Resting blood pressure (mm Hg)",
        json_schema_extra={"example": 140},
    )
    chol: float = Field(
        ..., ge=0, le=700,
        description="Serum cholesterol (mg/dl)",
        json_schema_extra={"example": 268},
    )
    fbs: int = Field(
        ..., ge=0, le=1,
        description="Fasting blood sugar > 120 mg/dl (1 = true, 0 = false)",
        json_schema_extra={"example": 0},
    )
    restecg: int = Field(
        ..., ge=0, le=2,
        description="Resting ECG results (0–2)",
        json_schema_extra={"example": 0},
    )
    thalach: float = Field(
        ..., ge=0, le=250,
        description="Maximum heart rate achieved",
        json_schema_extra={"example": 160},
    )
    exang: int = Field(
        ..., ge=0, le=1,
        description="Exercise induced angina (1 = yes, 0 = no)",
        json_schema_extra={"example": 0},
    )
    oldpeak: float = Field(
        ..., ge=0, le=10,
        description="ST depression induced by exercise relative to rest",
        json_schema_extra={"example": 3.6},
    )
    slope: int = Field(
        ..., ge=0, le=2,
        description="Slope of peak exercise ST segment (0–2)",
        json_schema_extra={"example": 0},
    )
    ca: int = Field(
        ..., ge=0, le=4,
        description="Number of major vessels colored by fluoroscopy (0–4)",
        json_schema_extra={"example": 2},
    )
    thal: int = Field(
        ..., ge=0, le=3,
        description="Thalassemia (0 = normal, 1 = fixed defect, 2 = reversible defect, 3 = other)",
        json_schema_extra={"example": 2},
    )


# ─────────────────────────────────────────────
#  PARKINSON'S DISEASE  (22 features — Oxford dataset)
# ─────────────────────────────────────────────
class ParkinsonsPredictionRequest(BaseModel):
    """Request schema for Parkinson's prediction. Feature order matches the original SVM model.
    All 22 voice biomarker features — 'name' and 'status' columns excluded."""

    fo: float = Field(
        ..., gt=0, description="MDVP:Fo(Hz) — Average vocal fundamental frequency",
        json_schema_extra={"example": 119.992},
    )
    fhi: float = Field(
        ..., gt=0, description="MDVP:Fhi(Hz) — Maximum vocal fundamental frequency",
        json_schema_extra={"example": 157.302},
    )
    flo: float = Field(
        ..., gt=0, description="MDVP:Flo(Hz) — Minimum vocal fundamental frequency",
        json_schema_extra={"example": 74.997},
    )
    jitter_percent: float = Field(
        ..., ge=0, description="MDVP:Jitter(%) — Jitter as percentage",
        json_schema_extra={"example": 0.00784},
    )
    jitter_abs: float = Field(
        ..., ge=0, description="MDVP:Jitter(Abs) — Absolute jitter in microseconds",
        json_schema_extra={"example": 0.00007},
    )
    rap: float = Field(
        ..., ge=0, description="MDVP:RAP — Relative amplitude perturbation",
        json_schema_extra={"example": 0.00370},
    )
    ppq: float = Field(
        ..., ge=0, description="MDVP:PPQ — Five-point period perturbation quotient",
        json_schema_extra={"example": 0.00554},
    )
    ddp: float = Field(
        ..., ge=0, description="Jitter:DDP — Average absolute difference of differences between jitter cycles",
        json_schema_extra={"example": 0.01109},
    )
    shimmer: float = Field(
        ..., ge=0, description="MDVP:Shimmer — Local shimmer",
        json_schema_extra={"example": 0.04374},
    )
    shimmer_db: float = Field(
        ..., ge=0, description="MDVP:Shimmer(dB) — Local shimmer in decibels",
        json_schema_extra={"example": 0.426},
    )
    apq3: float = Field(
        ..., ge=0, description="Shimmer:APQ3 — Three-point amplitude perturbation quotient",
        json_schema_extra={"example": 0.02182},
    )
    apq5: float = Field(
        ..., ge=0, description="Shimmer:APQ5 — Five-point amplitude perturbation quotient",
        json_schema_extra={"example": 0.03130},
    )
    apq: float = Field(
        ..., ge=0, description="MDVP:APQ — Amplitude perturbation quotient",
        json_schema_extra={"example": 0.02971},
    )
    dda: float = Field(
        ..., ge=0, description="Shimmer:DDA — Average absolute differences between shimmer cycles",
        json_schema_extra={"example": 0.06545},
    )
    nhr: float = Field(
        ..., ge=0, description="NHR — Noise-to-harmonics ratio",
        json_schema_extra={"example": 0.02211},
    )
    hnr: float = Field(
        ..., description="HNR — Harmonics-to-noise ratio",
        json_schema_extra={"example": 21.033},
    )
    rpde: float = Field(
        ..., ge=0, le=1, description="RPDE — Recurrence period density entropy",
        json_schema_extra={"example": 0.414783},
    )
    dfa: float = Field(
        ..., ge=0, le=1, description="DFA — Detrended fluctuation analysis signal fractal scaling exponent",
        json_schema_extra={"example": 0.815285},
    )
    spread1: float = Field(
        ..., description="spread1 — Nonlinear measure of fundamental frequency variation",
        json_schema_extra={"example": -4.813031},
    )
    spread2: float = Field(
        ..., ge=0, description="spread2 — Nonlinear measure of fundamental frequency variation",
        json_schema_extra={"example": 0.266482},
    )
    d2: float = Field(
        ..., gt=0, description="D2 — Correlation dimension (nonlinear dynamical complexity)",
        json_schema_extra={"example": 2.301442},
    )
    ppe: float = Field(
        ..., ge=0, description="PPE — Pitch period entropy",
        json_schema_extra={"example": 0.284654},
    )


# ─────────────────────────────────────────────
#  UNIFIED RESPONSE
# ─────────────────────────────────────────────
class PredictionResponse(BaseModel):
    """Unified response schema returned by all prediction endpoints."""

    success: bool = Field(..., description="Whether the prediction was successful")
    disease: str = Field(..., description="Name of the disease being predicted")
    prediction: int = Field(..., description="Raw model prediction (0 or 1)")
    result: str = Field(..., description="Human-readable result string")
    probability: Optional[float] = Field(
        None, description="Prediction probability (only for models that support predict_proba)"
    )
    message: str = Field(..., description="Detailed explanation message")


class ErrorResponse(BaseModel):
    """Standard error response."""

    success: bool = False
    detail: str = Field(..., description="Error details")
