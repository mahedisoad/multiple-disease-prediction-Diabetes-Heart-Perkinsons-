"""
Prediction service — transforms validated input into numpy arrays,
runs the appropriate model, and returns structured results.

CRITICAL: Feature order must exactly match how each model was trained.
No scalers or encoders are applied because the original notebooks
trained all three models on raw feature values.
"""
import numpy as np

from app.core.logging_config import logger
from app.schemas.prediction import (
    DiabetesPredictionRequest,
    HeartDiseasePredictionRequest,
    ParkinsonsPredictionRequest,
    PredictionResponse,
)
from app.services.model_loader import model_store


def predict_diabetes(data: DiabetesPredictionRequest) -> PredictionResponse:
    """Run diabetes prediction using the SVM model.

    Feature order (8 features):
        Pregnancies, Glucose, BloodPressure, SkinThickness,
        Insulin, BMI, DiabetesPedigreeFunction, Age
    """
    model = model_store.get_model("diabetes")

    # Exact feature order from the training notebook
    features = np.array([[
        data.Pregnancies,
        data.Glucose,
        data.BloodPressure,
        data.SkinThickness,
        data.Insulin,
        data.BMI,
        data.DiabetesPedigreeFunction,
        data.Age,
    ]])

    prediction = int(model.predict(features)[0])

    # SVC without probability=True — cannot provide probabilities
    if prediction == 1:
        result = "Positive — Diabetic"
        message = "The model predicts that the person is likely diabetic based on the provided health parameters."
    else:
        result = "Negative — Non-Diabetic"
        message = "The model predicts that the person is not likely diabetic based on the provided health parameters."

    logger.info("Diabetes prediction: %d", prediction)

    return PredictionResponse(
        success=True,
        disease="Diabetes",
        prediction=prediction,
        result=result,
        probability=None,
        message=message,
    )


def predict_heart_disease(data: HeartDiseasePredictionRequest) -> PredictionResponse:
    """Run heart disease prediction using the Logistic Regression model.

    Feature order (13 features):
        age, sex, cp, trestbps, chol, fbs, restecg,
        thalach, exang, oldpeak, slope, ca, thal
    """
    model = model_store.get_model("heart")

    features = np.array([[
        data.age,
        data.sex,
        data.cp,
        data.trestbps,
        data.chol,
        data.fbs,
        data.restecg,
        data.thalach,
        data.exang,
        data.oldpeak,
        data.slope,
        data.ca,
        data.thal,
    ]])

    prediction = int(model.predict(features)[0])

    # LogisticRegression natively supports predict_proba
    probability = None
    try:
        proba = model.predict_proba(features)
        probability = round(float(proba[0][1]), 4)  # probability of class 1 (disease)
    except Exception:
        logger.warning("predict_proba not available for heart disease model")

    if prediction == 1:
        result = "Positive — Heart Disease Detected"
        message = "The model indicates a higher likelihood of heart disease based on the provided cardiac parameters."
    else:
        result = "Negative — Healthy Heart"
        message = "The model indicates a lower likelihood of heart disease based on the provided cardiac parameters."

    logger.info("Heart disease prediction: %d (proba=%.4f)", prediction, probability or 0.0)

    return PredictionResponse(
        success=True,
        disease="Heart Disease",
        prediction=prediction,
        result=result,
        probability=probability,
        message=message,
    )


def predict_parkinsons(data: ParkinsonsPredictionRequest) -> PredictionResponse:
    """Run Parkinson's prediction using the SVM model.

    Feature order (22 features — mapped from simplified schema field names
    to the original column names used during training):
        MDVP:Fo(Hz), MDVP:Fhi(Hz), MDVP:Flo(Hz), MDVP:Jitter(%),
        MDVP:Jitter(Abs), MDVP:RAP, MDVP:PPQ, Jitter:DDP,
        MDVP:Shimmer, MDVP:Shimmer(dB), Shimmer:APQ3, Shimmer:APQ5,
        MDVP:APQ, Shimmer:DDA, NHR, HNR, RPDE, DFA,
        spread1, spread2, D2, PPE
    """
    model = model_store.get_model("parkinsons")

    features = np.array([[
        data.fo,
        data.fhi,
        data.flo,
        data.jitter_percent,
        data.jitter_abs,
        data.rap,
        data.ppq,
        data.ddp,
        data.shimmer,
        data.shimmer_db,
        data.apq3,
        data.apq5,
        data.apq,
        data.dda,
        data.nhr,
        data.hnr,
        data.rpde,
        data.dfa,
        data.spread1,
        data.spread2,
        data.d2,
        data.ppe,
    ]])

    prediction = int(model.predict(features)[0])

    if prediction == 1:
        result = "Positive — Parkinson's Detected"
        message = "The model indicates a higher likelihood of Parkinson's disease based on the provided voice biomarkers."
    else:
        result = "Negative — No Parkinson's"
        message = "The model indicates a lower likelihood of Parkinson's disease based on the provided voice biomarkers."

    logger.info("Parkinson's prediction: %d", prediction)

    return PredictionResponse(
        success=True,
        disease="Parkinson's Disease",
        prediction=prediction,
        result=result,
        probability=None,
        message=message,
    )
