from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_compare_endpoint():
    response = client.post("/api/compare", json={
        "language": "python",
        "source_a": "def add(a, b): return a + b",
        "source_b": "def sum_values(x, y): return x + y",
    })
    assert response.status_code == 200
    assert "similarity_percent" in response.json()


def test_unsupported_language_is_rejected():
    response = client.post("/api/compare", json={
        "language": "java", "source_a": "class A {}", "source_b": "class B {}"
    })
    assert response.status_code == 400
