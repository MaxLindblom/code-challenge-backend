from fastapi.testclient import TestClient

from main import app

test_client = TestClient(app)


def test_init():
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "hello world"}
