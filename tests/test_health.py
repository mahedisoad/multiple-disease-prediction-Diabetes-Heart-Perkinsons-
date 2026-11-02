"""
Tests for health check, metadata, and static root endpoints.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_serve_frontend(client):
    """Verify that root URL returns the HTML dashboard."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Multiple Disease Prediction System" in response.text
    assert "<!DOCTYPE html>" in response.text


def test_health_endpoint(client):
    """Verify health endpoint returns UP status and model load states."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["models_loaded"] is True
    assert "available_diseases" in data
    assert "diabetes" in data["available_diseases"]
    assert "heart" in data["available_diseases"]
    assert "parkinsons" in data["available_diseases"]


def test_diseases_metadata_endpoint(client):
    """Verify list of supported diseases and feature metadata."""
    response = client.get("/api/diseases")
    assert response.status_code == 200
    diseases = response.json()
    assert isinstance(diseases, list)
    disease_ids = [d["id"] for d in diseases]
    assert "diabetes" in disease_ids
    assert "heart" in disease_ids
    assert "parkinsons" in disease_ids

    for d in diseases:
        assert "name" in d
        assert "description" in d
        assert "features_count" in d
        assert "model_type" in d
        assert "icon" in d


def test_serve_robots_txt(client):
    """Verify that robots.txt is served with correct content."""
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert "User-agent:" in response.text
    assert "Disallow: /api/predict/" in response.text


def test_serve_sitemap_xml(client):
    """Verify that sitemap.xml is served with valid XML."""
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert "<?xml" in response.text
    assert "<urlset" in response.text
