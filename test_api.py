from fastapi.testclient import TestClient
from api import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["description"] == ('API для генерации summary на python код. '
                                              'Возможности: простое summary методом summarize, '
                                              'по ссылке на файл в github, по python коду в репозитории.')


def test_summarize_raw_link_no_data():
    response = client.post("/summarize/raw_url")
    assert response.status_code == 422
