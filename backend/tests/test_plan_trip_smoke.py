"""Smoke test for /plan-trip endpoint with LLM mocked.

Ensures the endpoint returns a success response structure without
making real OpenAI calls.
"""

from fastapi.testclient import TestClient

import backend.trip_planner_agent as agent
from backend.main import app


class DummyLLM:
    def invoke(self, _messages):  # noqa: D401
        class R:
            def __init__(self):
                self.content = "dummy response"

        return R()


def test_plan_trip_smoke(monkeypatch):
    def _dummy_get_llm():  # noqa: D401
        return DummyLLM()

    monkeypatch.setattr(agent, "get_llm", _dummy_get_llm)
    client = TestClient(app)

    payload = {
        "destination": "Paris",
        "duration": 3,
        "budget": 1500,
        "interests": ["art", "food"],
        "start_date": "2025-06-01",
        "end_date": "2025-06-04",
        "accommodation_type": "hotel",
        "transportation_type": "flight",
    }

    resp = client.post("/plan-trip", json=payload)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["success"] is True
    assert "data" in data
    assert data["data"]["destination"].lower() == "paris"
