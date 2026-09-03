from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.api.models import SourceNode

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@patch("app.api.routes.rag_service")
def test_ask_endpoint(mock_rag_service):
    # Mock the RAG service response
    mock_rag_service.ask.return_value = (
        "This is a mock answer based on the context.",
        [
            SourceNode(filename="doc1.txt", page=1, type="text", snippet="Mock context snippet...")
        ]
    )

    response = client.post(
        "/api/v1/ask",
        json={"question": "What is the meaning of life?"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "This is a mock answer based on the context."
    assert len(data["sources"]) == 1
    assert data["sources"][0]["filename"] == "doc1.txt"
    
    mock_rag_service.ask.assert_called_once_with("What is the meaning of life?")
