"""
API routes for disease prediction endpoints.
"""
from fastapi import APIRouter, HTTPException, status

from app.core.logging_config import logger
from app.schemas.prediction import (
    DiabetesPredictionRequest,
    HeartDiseasePredictionRequest,
    ParkinsonsPredictionRequest,
    PredictionResponse,
    ErrorResponse,
)
from app.services.model_loader import model_store, ModelLoadError
from app.services.prediction_service import (
    predict_diabetes,
    predict_heart_disease,
    predict_parkinsons,
)


router = APIRouter(prefix="/api", tags=["Predictions"])


# ──────────────── Health Check ────────────────
@router.get(
    "/health",
    summary="Health check",
    response_model=dict,
)
async def health_check():
    """Returns application health status and loaded model information."""
    return {
        "status": "healthy",
        "models_loaded": model_store.is_loaded,
        "available_diseases": model_store.available_diseases(),
    }


# ──────────────── Disease List ────────────────
DISEASE_INFO = {
    "diabetes": {
        "id": "diabetes",
        "name": "Diabetes",
        "description": "Predict the likelihood of diabetes using key health indicators like glucose levels, BMI, blood pressure, and more.",
        "features_count": 8,
        "model_type": "Support Vector Machine (Linear Kernel)",
        "accuracy": "77.27%",
        "icon": "🩸",
    },
    "heart": {
        "id": "heart",
        "name": "Heart Disease",
        "description": "Assess cardiovascular risk using clinical parameters including cholesterol, resting ECG, exercise test results, and more.",
        "features_count": 13,
        "model_type": "Logistic Regression",
        "accuracy": "81.97%",
        "icon": "❤️",
    },
    "parkinsons": {
        "id": "parkinsons",
        "name": "Parkinson's Disease",
        "description": "Detect Parkinson's disease through voice biomarker analysis including jitter, shimmer, pitch, and nonlinear measures.",
        "features_count": 22,
        "model_type": "Support Vector Machine (Linear Kernel)",
        "accuracy": "87.18%",
        "icon": "🧠",
    },
}


@router.get(
    "/diseases",
    summary="List available diseases",
    response_model=list[dict],
)
async def list_diseases():
    """Returns metadata for all diseases with loaded models."""
    available = model_store.available_diseases()
    return [
        DISEASE_INFO[key]
        for key in available
        if key in DISEASE_INFO
    ]


# ──────────────── Prediction Endpoints ────────────────
@router.post(
    "/predict/diabetes",
    summary="Predict Diabetes",
    response_model=PredictionResponse,
    responses={
        422: {"model": ErrorResponse, "description": "Validation error"},
        503: {"model": ErrorResponse, "description": "Model not available"},
    },
)
async def diabetes_prediction(data: DiabetesPredictionRequest):
    """Predict diabetes using the trained SVM model (8 features)."""
    try:
        result = predict_diabetes(data)
        return result
    except ModelLoadError as e:
        logger.error("Diabetes model unavailable: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )
    except Exception as e:
        logger.exception("Unexpected error in diabetes prediction")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}",
        )


@router.post(
    "/predict/heart",
    summary="Predict Heart Disease",
    response_model=PredictionResponse,
    responses={
        422: {"model": ErrorResponse, "description": "Validation error"},
        503: {"model": ErrorResponse, "description": "Model not available"},
    },
)
@router.post(
    "/predict/heart-disease",
    summary="Predict Heart Disease (Alias)",
    response_model=PredictionResponse,
    include_in_schema=False,
)
async def heart_disease_prediction(data: HeartDiseasePredictionRequest):
    """Predict heart disease using the trained Logistic Regression model (13 features)."""
    try:
        result = predict_heart_disease(data)
        return result
    except ModelLoadError as e:
        logger.error("Heart disease model unavailable: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )
    except Exception as e:
        logger.exception("Unexpected error in heart disease prediction")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}",
        )


@router.post(
    "/predict/parkinsons",
    summary="Predict Parkinson's Disease",
    response_model=PredictionResponse,
    responses={
        422: {"model": ErrorResponse, "description": "Validation error"},
        503: {"model": ErrorResponse, "description": "Model not available"},
    },
)
async def parkinsons_prediction(data: ParkinsonsPredictionRequest):
    """Predict Parkinson's disease using the trained SVM model (22 voice biomarker features)."""
    try:
        result = predict_parkinsons(data)
        return result
    except ModelLoadError as e:
        logger.error("Parkinson's model unavailable: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )
    except Exception as e:
        logger.exception("Unexpected error in Parkinson's prediction")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}",
        )
