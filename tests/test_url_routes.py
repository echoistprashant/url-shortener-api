from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_route():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "Healthy"
    }


def test_shorten_url():
    response = client.post(
        "/shorten",
        json={
            "url": "https://youtube.com"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert "original_url" in data
    assert "short_url" in data    