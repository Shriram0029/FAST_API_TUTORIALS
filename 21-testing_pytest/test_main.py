from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# test HOME API
def test_home():
    response = client.get("/")
    # status code check
    assert response.status_code == 200
    # response body check
    assert response.json() == {"message": "hello world"}

def test_add():
    response = client.get("/add?a=3&b=4")

    assert response.status_code == 200
    assert response.json() == {"result" : 7}
