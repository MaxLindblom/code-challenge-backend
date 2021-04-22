from fastapi.testclient import TestClient

from main import app

ENDPOINT = "/clients"
TEST_EMAIL = "test@email.se"
FAULTY_JSON = {"lat": 62, "lon": 17}

test_client = TestClient(app)


def test_register_client():
    response = test_client.post(
        ENDPOINT,
        json={"email": TEST_EMAIL, "lat": 62, "lon": 17}
    )
    assert response.status_code == 200
    assert response.json() == {"email": TEST_EMAIL, "phone": None,
                               "lat": 62, "lon": 17, "traffic_area": "Gävleborg"}
    faulty_response = test_client.post(
        ENDPOINT,
        json=FAULTY_JSON
    )
    assert faulty_response.status_code == 400


def test_update_geolocation():
    response = test_client.put(
        ENDPOINT,
        json={"email": TEST_EMAIL, "lat": 60, "lon": 18}
    )
    assert response.status_code == 200
    assert response.json() == {"email": TEST_EMAIL, "phone": None,
                               "lat": 60, "lon": 18, "traffic_area": "Uppland"}
    faulty_response = test_client.put(
        ENDPOINT,
        json=FAULTY_JSON
    )
    assert faulty_response.status_code == 400


def test_delete_client():
    response = test_client.delete(
        ENDPOINT,
        json={"email": TEST_EMAIL, "lat": 60, "lon": 18}
    )
    assert response.status_code == 200
    assert response.json() == {"email": TEST_EMAIL, "phone": None,
                               "lat": 60, "lon": 18, "traffic_area": "Uppland"}
    faulty_response = test_client.delete(
        ENDPOINT,
        json=FAULTY_JSON
    )
    assert faulty_response.status_code == 400
