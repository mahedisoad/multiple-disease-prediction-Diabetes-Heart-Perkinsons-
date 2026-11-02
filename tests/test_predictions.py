"""
Comprehensive test suite for Disease Prediction endpoints.
Covers:
  - Diabetes prediction (normal, diabetic, validation errors, boundary cases)
  - Heart Disease prediction (normal, diseased, validation errors)
  - Parkinson's prediction (normal, diseased, validation errors)
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


# ---------------------------------------------------------------------------
# DIABETES TESTS
# ---------------------------------------------------------------------------

def test_predict_diabetes_healthy_sample(client):
    """Test diabetes endpoint with healthy profile."""
    payload = {
        "Pregnancies": 1,
        "Glucose": 85.0,
        "BloodPressure": 66.0,
        "SkinThickness": 29.0,
        "Insulin": 0.0,
        "BMI": 26.6,
        "DiabetesPedigreeFunction": 0.351,
        "Age": 31
    }
    response = client.post("/api/predict/diabetes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["disease"] == "Diabetes"
    assert data["prediction"] in [0, 1]
    assert "result" in data
    assert "message" in data


def test_predict_diabetes_high_risk_sample(client):
    """Test diabetes endpoint with high-risk diabetic profile."""
    payload = {
        "Pregnancies": 8,
        "Glucose": 183.0,
        "BloodPressure": 90.0,
        "SkinThickness": 35.0,
        "Insulin": 200.0,
        "BMI": 38.5,
        "DiabetesPedigreeFunction": 1.25,
        "Age": 55
    }
    response = client.post("/api/predict/diabetes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["disease"] == "Diabetes"
    assert data["prediction"] == 1


def test_predict_diabetes_missing_field(client):
    """Validation test: missing required field returns 422."""
    payload = {
        "Pregnancies": 1,
        "Glucose": 85.0,
        # missing BloodPressure
        "SkinThickness": 29.0,
        "Insulin": 0.0,
        "BMI": 26.6,
        "DiabetesPedigreeFunction": 0.351,
        "Age": 31
    }
    response = client.post("/api/predict/diabetes", json=payload)
    assert response.status_code == 422


def test_predict_diabetes_invalid_values(client):
    """Validation test: out-of-range negative values return 422."""
    payload = {
        "Pregnancies": -5,  # negative pregnancy not allowed
        "Glucose": 85.0,
        "BloodPressure": 66.0,
        "SkinThickness": 29.0,
        "Insulin": 0.0,
        "BMI": 26.6,
        "DiabetesPedigreeFunction": 0.351,
        "Age": 31
    }
    response = client.post("/api/predict/diabetes", json=payload)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# HEART DISEASE TESTS
# ---------------------------------------------------------------------------

def test_predict_heart_disease_normal_sample(client):
    """Test heart disease prediction with typical values."""
    payload = {
        "age": 45,
        "sex": 1,
        "cp": 0,
        "trestbps": 120.0,
        "chol": 190.0,
        "fbs": 0,
        "restecg": 0,
        "thalach": 165.0,
        "exang": 0,
        "oldpeak": 0.0,
        "slope": 2,
        "ca": 0,
        "thal": 2
    }
    response = client.post("/api/predict/heart", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["disease"] == "Heart Disease"
    assert data["prediction"] in [0, 1]
    assert 0.0 <= data["probability"] <= 1.0


def test_predict_heart_disease_alias_route(client):
    """Test heart disease alias route /api/predict/heart-disease."""
    payload = {
        "age": 45,
        "sex": 1,
        "cp": 0,
        "trestbps": 120.0,
        "chol": 190.0,
        "fbs": 0,
        "restecg": 0,
        "thalach": 165.0,
        "exang": 0,
        "oldpeak": 0.0,
        "slope": 2,
        "ca": 0,
        "thal": 2
    }
    response = client.post("/api/predict/heart-disease", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["disease"] == "Heart Disease"


def test_predict_heart_disease_invalid_sex(client):
    """Validation test: sex out of [0, 1] range returns 422."""
    payload = {
        "age": 45,
        "sex": 3,  # Invalid
        "cp": 0,
        "trestbps": 120.0,
        "chol": 190.0,
        "fbs": 0,
        "restecg": 0,
        "thalach": 165.0,
        "exang": 0,
        "oldpeak": 0.0,
        "slope": 2,
        "ca": 0,
        "thal": 2
    }
    response = client.post("/api/predict/heart", json=payload)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# PARKINSON'S DISEASE TESTS
# ---------------------------------------------------------------------------

def test_predict_parkinsons_valid_sample(client):
    """Test parkinson's endpoint with 22 acoustic features."""
    payload = {
        "fo": 119.992,
        "fhi": 157.302,
        "flo": 74.997,
        "jitter_percent": 0.00784,
        "jitter_abs": 0.00007,
        "rap": 0.00370,
        "ppq": 0.00554,
        "ddp": 0.01109,
        "shimmer": 0.04374,
        "shimmer_db": 0.426,
        "apq3": 0.02182,
        "apq5": 0.03130,
        "apq": 0.02971,
        "dda": 0.06545,
        "nhr": 0.02211,
        "hnr": 21.033,
        "rpde": 0.414783,
        "dfa": 0.815285,
        "spread1": -4.813031,
        "spread2": 0.266482,
        "d2": 2.301442,
        "ppe": 0.284654
    }
    response = client.post("/api/predict/parkinsons", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["disease"] == "Parkinson's Disease"
    assert data["prediction"] in [0, 1]


def test_predict_parkinsons_missing_param(client):
    """Validation test: missing any acoustic feature returns 422."""
    payload = {
        "fo": 119.992,
        # missing remaining 21 features
    }
    response = client.post("/api/predict/parkinsons", json=payload)
    assert response.status_code == 422
