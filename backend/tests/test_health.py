"""Basic FastAPI health endpoint tests."""

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.json()
    assert "Trip Planner" in body.get("message", "")


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "healthy"
    assert body["service"] == "trip-planner-agent"
