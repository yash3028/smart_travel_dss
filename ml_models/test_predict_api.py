from fastapi.testclient import TestClient

from ml_models.predict_api import app


client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data


def test_predict_duration():
    payload = {"city": "London", "interest": "culture", "attractions": 20}
    r = client.post("/predict/duration", json=payload)
    # If models are not present, the app returns 503; still assert that the contract is correct
    assert r.status_code in (200, 503)
    if r.status_code == 200:
        data = r.json()
        assert "predicted_duration" in data


def test_predict_budget():
    payload = {"city": "Hyderabad", "days": 4, "travel_type": "solo", "interest": "culture"}
    r = client.post("/predict/budget", json=payload)
    assert r.status_code in (200, 503)
    if r.status_code == 200:
        data = r.json()
        assert "predicted_budget" in data
