from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_research_endpoint_missing_question():
    response = client.post("/api/research", json={})
    assert response.status_code == 422 # Validation Error

# We do not test the actual /api/research endpoint end-to-end here
# because that would trigger real LLM calls and burn rate limits.
# The end-to-end evaluation is handled by scripts/evaluate.py.
